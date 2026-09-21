# Level 3 — System One vs. System Two

## Kahneman's framing, borrowed for AI

Psychologist Daniel Kahneman's *Thinking, Fast and Slow* describes two modes
of human thought:

- **System 1** — fast, automatic, intuitive. Recognizing a face, catching a
  ball, sensing that a sentence sounds "urgent." No deliberate reasoning
  involved; the answer just arrives.
- **System 2** — slow, deliberate, effortful. Doing long division, writing an
  essay, planning a multi-step argument. You consciously work through it.

TypeSafe borrows this vocabulary directly, and it's a genuinely useful lens
for today's AI landscape:

| | System 1 (Jev) | System 2 (reasoning LLMs) |
|---|---|---|
| Examples | Jev | GPT-5-class models, Claude, Gemini in "thinking" modes |
| Output | typed decision + probability | free-form text |
| Speed | ~70–500ms | seconds to minutes |
| Best at | classify / route / score / verify | reason / plan / write / code |
| Worst at | open-ended generation, exact math | doing 1,000 of these per second cheaply |

Neither is "better" in general — they're specialized for different jobs, the
same way a reflex and a deliberate decision are both "thinking," just at
different points on a speed/depth tradeoff.

## How Jev is actually trained: RLCD

Jev is trained using what TypeSafe calls **RLCD — Reinforcement Learning for
Calibrated Decisions**. The important word here is *calibrated*. A model can
be "accurate" (right more often than wrong) without being calibrated
(honest about *how sure* it is). Calibration means: when Jev says something
is `0.95` likely, it should actually be true about 95% of the time it says
that — not 60%, not 99.9%.

Why this matters in practice: calibration is exactly what lets you write
code like this later in the course —

```python
if answer.confidence > 0.9:
    act_automatically()
elif answer.confidence > 0.5:
    ask_user_to_confirm()
else:
    route_to_human()
```

— and actually trust the thresholds. An uncalibrated model that's "usually
right" is much less useful for this pattern, because you can't tell high-
confidence-and-correct apart from high-confidence-and-wrong.

## A model that "understands language" but never writes it

One subtlety worth sitting with: Jev is **not** a lookup table or a
traditional classifier. It reads natural language the same way an LLM does —
it can pick up nuance, sarcasm, urgency, implied meaning. The difference is
purely in the *output contract*: instead of predicting the next token
freely, its output space is constrained at generation time to a small,
predefined set of typed answers. That's what buys the speed (no long
token-by-token decoding) and the reliability (there is no such thing as
"malformed Jev output" — the answer is always one of the shapes you defined).

We'll see exactly what those shapes are next.

Next: **[Level 4 — The Three Primitives](04_the_three_primitives.md)**.
