"""Unit tests for capstone/pipeline.py.

These are deterministic and free: every Jev/LLM call is mocked, so they run
in milliseconds with no network and no API key. They test the *code* — does
it parse a response correctly, does it apply the right threshold, does it
build the prompt it should — not whether Jev or the LLM gave a *good*
answer. That's a completely different question, answered by `evals/
run_eval.py` against the real API instead. See levels/10_capstone_project.md
for why that split matters.

Note the monkeypatch target: `capstone.pipeline.call_jev`, not
`capstone.client.call_jev`. pipeline.py did `from .client import call_jev`,
which binds its own name pointing at the same function object — patching
the original in client.py would leave pipeline's copy of the reference
untouched, and the test would silently call the real API instead of the
mock. Patch where a name is looked up, not where it's defined.
"""

import pytest

from capstone import pipeline
from capstone.pipeline import (
    TriageResult,
    VerificationResult,
    should_auto_send,
)


def fake_jev_response(answers: dict) -> dict:
    """Shape a mock response the way the real Jev API returns one."""
    return {"answers": answers, "_elapsed_ms": 12.3}


def test_triage_parses_urgent_department_and_frustration(monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "call_jev",
        lambda state, questions: fake_jev_response(
            {
                "is_urgent": {"noul": 0.93},
                "department": {"choice": "billing"},
                "frustration": {"score": 3, "legend": {"3": "angry"}},
            }
        ),
    )

    result = pipeline.triage("My payment failed and I need this fixed now!")

    assert result == TriageResult(is_urgent=True, department="billing", frustration="angry")


def test_triage_below_threshold_is_not_urgent(monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "call_jev",
        lambda state, questions: fake_jev_response(
            {
                "is_urgent": {"noul": 0.2},
                "department": {"choice": "sales"},
                "frustration": {"score": 0, "legend": {"0": "calm"}},
            }
        ),
    )

    result = pipeline.triage("Just curious about pricing, no rush.")

    assert result.is_urgent is False


def test_draft_reply_includes_department_and_message(monkeypatch):
    captured_prompt = {}

    def fake_chat_complete(prompt, **kwargs):
        captured_prompt["value"] = prompt
        return "  Thanks for reaching out, we're on it!  "

    monkeypatch.setattr(pipeline, "chat_complete", fake_chat_complete)

    triage_result = TriageResult(is_urgent=True, department="technical", frustration="annoyed")
    reply = pipeline.draft_reply("My API key is broken", triage_result)

    # draft_reply() strips whitespace from the LLM's response
    assert reply == "Thanks for reaching out, we're on it!"
    assert "technical" in captured_prompt["value"]
    assert "annoyed" in captured_prompt["value"]
    assert "My API key is broken" in captured_prompt["value"]


def test_verify_reply_parses_verdict_and_confidence(monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "call_jev",
        lambda state, questions: fake_jev_response(
            {
                "on_topic": {"noul": 0.97},
                "safe_to_send": {"choice": "send", "confidence": 0.91},
            }
        ),
    )

    result = pipeline.verify_reply("original message", "drafted reply")

    assert result == VerificationResult(on_topic=True, verdict="send", confidence=0.91)


@pytest.mark.parametrize(
    "verification,expected",
    [
        # Everything lines up -> auto-send.
        (VerificationResult(on_topic=True, verdict="send", confidence=0.95), True),
        # Off-topic -> never auto-send, regardless of confidence.
        (VerificationResult(on_topic=False, verdict="send", confidence=0.99), False),
        # Verdict isn't "send" -> hold for review.
        (VerificationResult(on_topic=True, verdict="review", confidence=0.99), False),
        (VerificationResult(on_topic=True, verdict="block", confidence=0.99), False),
        # Confidence exactly at the threshold does not clear it (strict >).
        (VerificationResult(on_topic=True, verdict="send", confidence=0.8), False),
        # Just above the threshold does.
        (VerificationResult(on_topic=True, verdict="send", confidence=0.801), True),
    ],
)
def test_should_auto_send_gating_rules(verification, expected):
    assert should_auto_send(verification) is expected


def test_process_ticket_runs_full_pipeline_and_wires_results_together(monkeypatch):
    """One mocked end-to-end run: triage feeds draft_reply, draft feeds
    verify_reply, verify feeds should_auto_send. This is the test that
    would catch a broken hookup between the pipeline's stages."""

    call_jev_responses = iter(
        [
            fake_jev_response(
                {
                    "is_urgent": {"noul": 0.9},
                    "department": {"choice": "billing"},
                    "frustration": {"score": 4, "legend": {"4": "furious"}},
                }
            ),
            fake_jev_response(
                {
                    "on_topic": {"noul": 0.95},
                    "safe_to_send": {"choice": "send", "confidence": 0.9},
                }
            ),
        ]
    )

    monkeypatch.setattr(pipeline, "call_jev", lambda state, questions: next(call_jev_responses))
    monkeypatch.setattr(pipeline, "chat_complete", lambda prompt, **kwargs: "We're on it.")

    outcome = pipeline.process_ticket("My payouts have failed for 3 days!")

    assert outcome.triage.department == "billing"
    assert outcome.reply == "We're on it."
    assert outcome.verification.verdict == "send"
    assert outcome.auto_send is True
