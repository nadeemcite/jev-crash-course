"""Level 6 — the same routing/urgency task, run through an LLM and through Jev.

Run: uv run examples/06_llm_vs_jev_timing.py

The LLM side goes through `chat_complete()` (LiteLLM), so it works with
whatever CHAT_MODEL you have a key for — not just OpenAI. See README
"Bring Your Own Model" if you don't have one yet.

Not a rigorous benchmark (one request per message, no warmup, no retries) —
just enough to *see* the latency and reliability gap discussed in
levels/06_jev_vs_llm_hands_on.md with your own eyes and your own keys.
"""

import json
import time

from common import DEFAULT_CHAT_MODEL, call_jev, chat_complete

MESSAGES = [
    "Help! My payouts have been failing for 3 days and I'm losing money every hour.",
    "Just wondering if you offer an annual discount on the Pro plan.",
    "The dashboard chart colors look slightly off in dark mode, no rush.",
]

DEPARTMENTS = {
    "billing": "Payments, invoicing, refunds",
    "technical": "Bugs, outages, integrations",
    "sales": "Pricing, upgrades, new accounts",
}

JEV_QUESTIONS = {
    "is_urgent": {"type": "noul", "instructions": "Does the message convey urgency?"},
    "department": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": DEPARTMENTS,
    },
}

LLM_PROMPT = f"""Classify the support message below.
Return ONLY a JSON object, no other text, with exactly these keys:
- "is_urgent": true or false
- "department": one of {list(DEPARTMENTS)}

Message: {{message}}"""


def classify_with_llm(message: str) -> tuple[dict | None, float, bool]:
    started = time.perf_counter()
    raw = chat_complete(LLM_PROMPT.format(message=message))
    elapsed_ms = (time.perf_counter() - started) * 1000
    # Not every provider honors "return only JSON" — strip code fences and
    # any leading/trailing chatter before the first { and after the last }.
    cleaned = raw.strip().strip("`")
    start, end = cleaned.find("{"), cleaned.rfind("}")
    try:
        return json.loads(cleaned[start : end + 1]), elapsed_ms, True
    except (json.JSONDecodeError, ValueError):
        return None, elapsed_ms, False


def classify_with_jev(message: str) -> tuple[dict, float]:
    result = call_jev(message, JEV_QUESTIONS)
    elapsed_ms = result.pop("_elapsed_ms")
    answers = result["answers"]
    parsed = {
        "is_urgent": answers["is_urgent"]["noul"] > 0.5,
        "department": answers["department"]["choice"],
        "confidence": answers["department"]["confidence"],
    }
    return parsed, elapsed_ms


def main() -> None:
    print(f"Using CHAT_MODEL={DEFAULT_CHAT_MODEL} (set this in .env to try another provider)\n")
    print(f"{'message':<55} {'llm ms':>8} {'jev ms':>8}   llm -> jev")
    print("-" * 100)

    for message in MESSAGES:
        llm_answer, llm_ms, llm_valid = classify_with_llm(message)
        jev_answer, jev_ms = classify_with_jev(message)

        llm_str = json.dumps(llm_answer) if llm_valid else "MALFORMED JSON"
        jev_str = f"urgent={jev_answer['is_urgent']} dept={jev_answer['department']} (conf {jev_answer['confidence']:.0%})"

        label = message[:52] + ("..." if len(message) > 52 else "")
        print(f"{label:<55} {llm_ms:>8.0f} {jev_ms:>8.0f}   {llm_str} -> {jev_str}")

    print("\nNote: this is one request per message with no retries — a small,")
    print("illustrative sample, not a rigorous benchmark.")


if __name__ == "__main__":
    main()
