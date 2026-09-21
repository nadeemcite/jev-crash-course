"""Eval: measure the capstone pipeline's *quality* against a hand-labeled
golden set — Jev's triage AND the LLM's draft, end to end.

Run: uv run evals/run_eval.py

This is NOT a unit test, on purpose:
  - It calls the real Jev API and the real LLM — costs time/money, needs
    TYPESAFE_API_KEY and a working CHAT_MODEL + provider key.
  - It's non-deterministic — the same ticket can score slightly differently
    run to run, since both models are probabilistic, not lookup tables.
  - It doesn't assert pass/fail. It prints an accuracy score you track over
    time — a change to a prompt, a question's `instructions`, or either
    model itself should move this number, and you want to *see* that, not
    have CI turn red on every run.

`tests/test_pipeline.py` is the other half of the picture: it checks that
the *code* around Jev/LLM answers is correct (parsing, thresholds, wiring),
with everything mocked so it's free and instant. This script checks that
the answers themselves are actually good, against real inputs with
known-correct labels. A real project needs both, and they run at different
times for different reasons — units on every commit, evals when you touch
a prompt, a question, or a model.

We log which model answered each part, because an eval score by itself is
ambiguous: if accuracy drops next week, was that your prompt change, or did
a provider quietly ship a new model version underneath you? Jev's resolved
model comes back in every response (see TriageResult.jev_model); the LLM's
model is whatever CHAT_MODEL resolves to, since LiteLLM doesn't have a
Jev-style "alias vs. resolved version" distinction — the string you set is
the string that runs.
"""

import json
import sys
from pathlib import Path

# Running this file directly (`uv run evals/run_eval.py`) puts `evals/` on
# sys.path, not the repo root — same reason examples/10_capstone_ticket_triage.py
# needs this. Add the repo root so `capstone` is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from capstone.client import DEFAULT_CHAT_MODEL
from capstone.pipeline import process_ticket

GOLDEN_SET_PATH = Path(__file__).parent / "golden_tickets.jsonl"


def load_golden_set() -> list[dict]:
    with GOLDEN_SET_PATH.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> None:
    examples = load_golden_set()
    department_correct = 0
    urgency_correct = 0
    jev_models_seen: set[str] = set()

    print(f"LLM model (drafting step): {DEFAULT_CHAT_MODEL} (set CHAT_MODEL in .env to try another)")
    print(f"Running the full pipeline (triage -> draft -> verify) against "
          f"{len(examples)} golden examples...\n")

    for example in examples:
        outcome = process_ticket(example["message"])
        triage_result = outcome.triage
        jev_models_seen.add(triage_result.jev_model)

        department_ok = triage_result.department == example["expected_department"]
        urgency_ok = triage_result.is_urgent == example["expected_urgent"]
        department_correct += department_ok
        urgency_correct += urgency_ok

        status = "OK" if (department_ok and urgency_ok) else "MISS"
        print(f"[{status}] jev={triage_result.jev_model} llm={DEFAULT_CHAT_MODEL} "
              f"{example['message'][:50]!r}")
        print(
            f"         department: got={triage_result.department!r} "
            f"expected={example['expected_department']!r}"
        )
        print(
            f"         urgent:     got={triage_result.is_urgent} "
            f"expected={example['expected_urgent']}"
        )

    total = len(examples)
    print("\n" + "=" * 60)
    print(f"Jev model(s) this run: {', '.join(sorted(jev_models_seen))}")
    print(f"LLM model this run:    {DEFAULT_CHAT_MODEL}")
    print(f"Department accuracy: {department_correct}/{total} "
          f"({department_correct / total:.0%})")
    print(f"Urgency accuracy:    {urgency_correct}/{total} "
          f"({urgency_correct / total:.0%})")
    if len(jev_models_seen) > 1:
        print(
            "\n⚠️  More than one Jev model version answered during this run — "
            "Jev likely upgraded mid-run. Treat this run's accuracy as noisy "
            "and re-run before comparing it to a previous baseline."
        )
    print(
        "\nThese numbers are a baseline to track, not a bar to pass. Re-run "
        "this after changing a question's instructions, its criteria, or "
        "either model, and compare — and note both model versions alongside "
        "the score, since either one changing can move accuracy on its own. "
        "(This eval only scores triage's department/urgency; the drafted "
        "reply and verification step run too, for a realistic end-to-end "
        "cost/latency picture, but aren't graded here — there's no "
        "objective ground truth for reply quality in golden_tickets.jsonl.)"
    )


if __name__ == "__main__":
    main()
