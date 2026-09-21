"""The demo runner: prints the pipeline's decisions for a handful of sample
tickets. This is the "look at it work" layer — all the logic worth testing
lives in `pipeline.py`, not here.
"""

from __future__ import annotations

from .client import DEFAULT_CHAT_MODEL
from .pipeline import process_ticket

SAMPLE_TICKETS = [
    "Help! My payouts have been failing for 3 days and I'm losing money every hour.",
    "Hi, just wondering if you offer an annual discount on the Pro plan?",
    "This is the third time I've emailed about my broken API key and NOBODY has replied. Fix this now.",
]


def main() -> None:
    print(f"Using CHAT_MODEL={DEFAULT_CHAT_MODEL} (set this in .env to try another provider)\n")

    for message in SAMPLE_TICKETS:
        print("=" * 80)
        print(f"TICKET: {message}\n")

        outcome = process_ticket(message)

        print(f"[Jev triage]   urgent={outcome.triage.is_urgent} "
              f"department={outcome.triage.department} "
              f"frustration={outcome.triage.frustration}")
        print(f"[LLM draft]    {outcome.reply}")
        print(f"[Jev verify]   on_topic={outcome.verification.on_topic} "
              f"verdict={outcome.verification.verdict} "
              f"(confidence {outcome.verification.confidence:.0%})")

        if outcome.auto_send:
            print("[Decision]     -> AUTO-SEND\n")
        else:
            print("[Decision]     -> HOLD FOR HUMAN REVIEW\n")


if __name__ == "__main__":
    main()
