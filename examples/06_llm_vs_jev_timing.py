"""Level 6 — the same routing/urgency task, run through GPT and through Jev.

Run: uv run examples/06_llm_vs_jev_timing.py

Not a rigorous benchmark (one request per message, no warmup, no retries) —
just enough to *see* the latency and reliability gap discussed in
levels/06_jev_vs_llm_hands_on.md with your own eyes and your own keys.
"""

import json
import time

from common import call_jev, openai_client

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

GPT_PROMPT = f"""Classify the support message below.
Return ONLY a JSON object with exactly these keys:
- "is_urgent": true or false
- "department": one of {list(DEPARTMENTS)}

Message: {{message}}"""


def classify_with_gpt(client, message: str) -> tuple[dict | None, float, bool]:
    started = time.perf_counter()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": GPT_PROMPT.format(message=message)}],
        response_format={"type": "json_object"},
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    raw = resp.choices[0].message.content
    try:
        return json.loads(raw), elapsed_ms, True
    except json.JSONDecodeError:
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
    client = openai_client()

    print(f"{'message':<55} {'gpt ms':>8} {'jev ms':>8}   gpt -> jev")
    print("-" * 100)

    for message in MESSAGES:
        gpt_answer, gpt_ms, gpt_valid = classify_with_gpt(client, message)
        jev_answer, jev_ms = classify_with_jev(message)

        gpt_str = json.dumps(gpt_answer) if gpt_valid else "MALFORMED JSON"
        jev_str = f"urgent={jev_answer['is_urgent']} dept={jev_answer['department']} (conf {jev_answer['confidence']:.0%})"

        label = message[:52] + ("..." if len(message) > 52 else "")
        print(f"{label:<55} {gpt_ms:>8.0f} {jev_ms:>8.0f}   {gpt_str} -> {jev_str}")

    print("\nNote: this is one request per message with no retries — a small,")
    print("illustrative sample, not a rigorous benchmark.")


if __name__ == "__main__":
    main()
