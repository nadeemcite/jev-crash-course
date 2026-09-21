"""Eval: measure Jev's triage *quality* against a hand-labeled golden set.

Run: uv run evals/run_eval.py

This is NOT a unit test, on purpose:
  - It calls the real Jev API — costs time/money, needs TYPESAFE_API_KEY.
  - It's non-deterministic — the same ticket can score slightly differently
    run to run, since Jev is a probabilistic model, not a lookup table.
  - It doesn't assert pass/fail. It prints an accuracy score you track over
    time — a change to a prompt, a question's `instructions`, or the model
    itself should move this number, and you want to *see* that, not have
    CI turn red on every run.

`tests/test_pipeline.py` is the other half of the picture: it checks that
the *code* around Jev's answers is correct (parsing, thresholds, wiring),
with everything mocked so it's free and instant. This script checks that
Jev's *answers* are actually good, against real inputs with known-correct
labels. A real project needs both, and they run at different times for
different reasons — units on every commit, evals when you touch a prompt,
a question, or a model.
"""

import json
import sys
from pathlib import Path

# Running this file directly (`uv run evals/run_eval.py`) puts `evals/` on
# sys.path, not the repo root — same reason examples/10_capstone_ticket_triage.py
# needs this. Add the repo root so `capstone` is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from capstone.pipeline import triage

GOLDEN_SET_PATH = Path(__file__).parent / "golden_tickets.jsonl"


def load_golden_set() -> list[dict]:
    with GOLDEN_SET_PATH.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> None:
    examples = load_golden_set()
    department_correct = 0
    urgency_correct = 0

    print(f"Running triage() against {len(examples)} golden examples...\n")

    for example in examples:
        result = triage(example["message"])

        department_ok = result.department == example["expected_department"]
        urgency_ok = result.is_urgent == example["expected_urgent"]
        department_correct += department_ok
        urgency_correct += urgency_ok

        status = "OK" if (department_ok and urgency_ok) else "MISS"
        print(f"[{status}] {example['message'][:60]!r}")
        print(
            f"         department: got={result.department!r} "
            f"expected={example['expected_department']!r}"
        )
        print(
            f"         urgent:     got={result.is_urgent} "
            f"expected={example['expected_urgent']}"
        )

    total = len(examples)
    print("\n" + "=" * 60)
    print(f"Department accuracy: {department_correct}/{total} "
          f"({department_correct / total:.0%})")
    print(f"Urgency accuracy:    {urgency_correct}/{total} "
          f"({urgency_correct / total:.0%})")
    print(
        "\nThese numbers are a baseline to track, not a bar to pass. Re-run "
        "this after changing a question's instructions, its criteria, or "
        "the model, and compare."
    )


if __name__ == "__main__":
    main()
