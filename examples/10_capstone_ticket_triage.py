"""Level 10 — capstone: GPT drafts, Jev triages and gates, end to end.

Run: uv run examples/10_capstone_ticket_triage.py

Pipeline per ticket:
  1. Jev triages the incoming message (urgent? department? frustration?)
  2. GPT drafts a reply, informed by Jev's triage
  3. Jev verifies the draft is on-topic and safe to auto-send
  4. Code decides: auto-send, or hold for human review
"""

from common import call_jev, openai_client

DEPARTMENTS = {
    "billing": "Payments, invoicing, refunds",
    "technical": "Bugs, outages, integrations",
    "sales": "Pricing, upgrades, new accounts",
}

TRIAGE_QUESTIONS = {
    "is_urgent": {"type": "noul", "instructions": "Does the message convey urgency?"},
    "department": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": DEPARTMENTS,
    },
    "frustration": {
        "type": "score",
        "instructions": "How frustrated does the customer sound?",
        "criteria": ["calm", "mildly annoyed", "annoyed", "angry", "furious"],
    },
}

TICKETS = [
    "Help! My payouts have been failing for 3 days and I'm losing money every hour.",
    "Hi, just wondering if you offer an annual discount on the Pro plan?",
    "This is the third time I've emailed about my broken API key and NOBODY has replied. Fix this now.",
]


def triage(message: str) -> dict:
    result = call_jev(message, TRIAGE_QUESTIONS)
    answers = result["answers"]
    return {
        "is_urgent": answers["is_urgent"]["noul"] > 0.5,
        "department": answers["department"]["choice"],
        "frustration": answers["frustration"]["legend"][
            str(round(answers["frustration"]["score"]))
        ],
    }


def draft_reply(client, message: str, triage_result: dict) -> str:
    prompt = (
        "You are a support agent. Write a short, warm, 2-3 sentence reply to "
        f"this customer message. The message has been routed to the "
        f"{triage_result['department']} team; the customer seems "
        f"{triage_result['frustration']}.\n\nMessage: {message}"
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()


VERIFY_QUESTIONS = {
    "on_topic": {
        "type": "noul",
        "instructions": "Does this draft reply directly address the customer's original message?",
    },
    "safe_to_send": {
        "type": "choice",
        "instructions": "Should this draft be sent to the customer as-is?",
        "criteria": {
            "send": "Clear, appropriate, and addresses the message",
            "review": "Plausible but risky, vague, or could use human review",
            "block": "Off-topic, inappropriate, or clearly wrong",
        },
    },
}


def verify_reply(message: str, reply: str) -> dict:
    state = f"Customer message: {message}\n\nDrafted reply: {reply}"
    result = call_jev(state, VERIFY_QUESTIONS)
    answers = result["answers"]
    return {
        "on_topic": answers["on_topic"]["noul"] > 0.5,
        "verdict": answers["safe_to_send"]["choice"],
        "confidence": answers["safe_to_send"]["confidence"],
    }


def should_auto_send(verification: dict) -> bool:
    return (
        verification["on_topic"]
        and verification["verdict"] == "send"
        and verification["confidence"] > 0.8
    )


def main() -> None:
    client = openai_client()

    for message in TICKETS:
        print("=" * 80)
        print(f"TICKET: {message}\n")

        triage_result = triage(message)
        print(f"[Jev triage]   urgent={triage_result['is_urgent']} "
              f"department={triage_result['department']} "
              f"frustration={triage_result['frustration']}")

        reply = draft_reply(client, message, triage_result)
        print(f"[GPT draft]    {reply}")

        verification = verify_reply(message, reply)
        print(f"[Jev verify]   on_topic={verification['on_topic']} "
              f"verdict={verification['verdict']} "
              f"(confidence {verification['confidence']:.0%})")

        if should_auto_send(verification):
            print("[Decision]     -> AUTO-SEND\n")
        else:
            print("[Decision]     -> HOLD FOR HUMAN REVIEW\n")


if __name__ == "__main__":
    main()
