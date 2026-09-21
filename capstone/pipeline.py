"""The actual triage -> draft -> verify business logic.

This is the part of the capstone worth unit testing: given a Jev/LLM
response, does the code parse it correctly and make the right call? We
never test "did Jev/the LLM give a good answer" here — that's what
`evals/run_eval.py` is for. See levels/10_capstone_project.md for the
full explanation of why that split matters.

Note for anyone writing tests against this module: it imports `call_jev`
and `chat_complete` by name (`from .client import ...`), so mocks need to
patch them where they're *looked up* — `capstone.pipeline.call_jev` — not
where they're defined (`capstone.client.call_jev`). Patching the original
in `client.py` would leave this module's already-bound reference untouched.
"""

from __future__ import annotations

from dataclasses import dataclass

from .client import call_jev, chat_complete

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

# Higher stakes than a misrouted ticket -> demand a higher confidence bar
# before letting anything auto-send. See levels/08 rule #2.
AUTO_SEND_CONFIDENCE_THRESHOLD = 0.8


@dataclass(frozen=True)
class TriageResult:
    is_urgent: bool
    department: str
    frustration: str


@dataclass(frozen=True)
class VerificationResult:
    on_topic: bool
    verdict: str
    confidence: float


@dataclass(frozen=True)
class TicketOutcome:
    message: str
    triage: TriageResult
    reply: str
    verification: VerificationResult
    auto_send: bool


def triage(message: str) -> TriageResult:
    result = call_jev(message, TRIAGE_QUESTIONS)
    answers = result["answers"]
    return TriageResult(
        is_urgent=answers["is_urgent"]["noul"] > 0.5,
        department=answers["department"]["choice"],
        frustration=answers["frustration"]["legend"][
            str(round(answers["frustration"]["score"]))
        ],
    )


def draft_reply(message: str, triage_result: TriageResult) -> str:
    prompt = (
        "You are a support agent. Write a short, warm, 2-3 sentence reply to "
        f"this customer message. The message has been routed to the "
        f"{triage_result.department} team; the customer seems "
        f"{triage_result.frustration}.\n\nMessage: {message}"
    )
    return chat_complete(prompt).strip()


def verify_reply(message: str, reply: str) -> VerificationResult:
    state = f"Customer message: {message}\n\nDrafted reply: {reply}"
    result = call_jev(state, VERIFY_QUESTIONS)
    answers = result["answers"]
    return VerificationResult(
        on_topic=answers["on_topic"]["noul"] > 0.5,
        verdict=answers["safe_to_send"]["choice"],
        confidence=answers["safe_to_send"]["confidence"],
    )


def should_auto_send(verification: VerificationResult) -> bool:
    return (
        verification.on_topic
        and verification.verdict == "send"
        and verification.confidence > AUTO_SEND_CONFIDENCE_THRESHOLD
    )


def process_ticket(message: str) -> TicketOutcome:
    """Run one message through the full triage -> draft -> verify pipeline."""
    triage_result = triage(message)
    reply = draft_reply(message, triage_result)
    verification = verify_reply(message, reply)
    return TicketOutcome(
        message=message,
        triage=triage_result,
        reply=reply,
        verification=verification,
        auto_send=should_auto_send(verification),
    )
