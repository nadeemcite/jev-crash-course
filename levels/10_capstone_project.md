# Level 10 — Capstone: A Support-Ticket Triage Pipeline

Everything from Levels 1–9, combined into one small end-to-end pipeline you
can actually run against your own keys.

## The pipeline

```
incoming support message
        │
        ▼
  Jev: is_urgent? department? frustration?      <- Level 4, 7 (fan-out)
        │
        ▼
  GPT: draft a reply, given the message
       and Jev's read on department/tone         <- the "write" half
        │
        ▼
  Jev: does the draft actually address the       <- Level 7, Pattern 3
       message? is it safe to auto-send?          (verification gate)
        │
        ├─ high confidence, on-topic  → auto-send the draft
        └─ low confidence / off-topic → hold for human review
```

This mirrors real production patterns: Jev handles every *decision* point
(triage in, verification out), GPT handles the one part that genuinely
needs open-ended generation (the reply itself). Neither model does the
other's job.

## Run it

```bash
uv run examples/10_capstone_ticket_triage.py
```

Watch the console output for each of the sample tickets: the triage
answers, the drafted reply, the verification check, and the final routing
decision (auto-send vs. hold for review).

## Where to take this next

- Swap in your own real support messages instead of the sample list.
- Tighten or loosen the confidence thresholds in `should_auto_send()` and
  see how the routing behavior changes.
- Add a `score` question for reply quality/tone before allowing auto-send.
- Read `examples/common.py` and `typesafe-sdk` on PyPI if you want to move
  from this course's raw `requests` calls to the official SDK.
- Revisit [Level 9](09_limits_hype_and_skepticism.md) before wiring anything
  like this into a system that touches real customers — confidence-gate
  aggressively, and keep a human in the loop for anything you're not
  confident about yet.

## What you now understand about Jev

- It's a **System One** decision model from **TypeSafe AI** (launched Sept
  2026, $40M seed), not a chatbot — it never generates prose.
- It answers **typed questions** (`noul`, `choice`, `score`) about a
  **state**, returning calibrated probabilities in well under a second.
- It's meant to sit **alongside** LLMs in an agent loop, handling the
  "decide" steps while an LLM handles the "write" steps.
- The core patterns are **routing, gating, and verification**, all built on
  the same confidence-threshold branching pattern.
- The headline performance claims are real but self-reported, and the
  category's long-term shape is still an open question — worth using, worth
  watching, not worth taking on faith.

That's the crash course. Go build something.
