"""Level 5 — a raw, minimal call to the real Jev API.

Run: uv run examples/05_raw_jev_call.py

Asks Jev one `noul` question and one `choice` question about the same
support-message `state`, then prints the full response so you can see the
exact shape and the real round-trip latency.
"""

import json

from common import call_jev

STATE = "Help! My payouts have been failing for 3 days and I'm losing money every hour."

QUESTIONS = {
    "is_urgent": {
        "type": "noul",
        "instructions": "Does the message convey urgency?",
    },
    "department": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": {
            "billing": "Payments, invoicing, refunds",
            "technical": "Bugs, outages, integrations",
            "sales": "Pricing, upgrades, new accounts",
        },
    },
}


def main() -> None:
    result = call_jev(STATE, QUESTIONS)
    elapsed = result.pop("_elapsed_ms")

    print(f"state: {STATE!r}\n")
    print(json.dumps(result, indent=2))
    print(f"\nround-trip latency: {elapsed}ms")
    print(
        f"is_urgent -> {result['answers']['is_urgent']['noul']:.0%} likely urgent"
    )
    print(
        "department -> "
        f"{result['answers']['department']['choice']} "
        f"(confidence {result['answers']['department']['confidence']:.0%})"
    )


if __name__ == "__main__":
    main()
