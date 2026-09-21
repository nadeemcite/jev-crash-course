# Level 9 — Limits, Hype & Skepticism

This is the level that actually answers "why is this in the market" with a
critical eye, not just a recap of the launch announcement.

## What Jev genuinely cannot do

- **No open-ended output.** It can't write prose, summarize, explain its
  reasoning, or call tools itself. It only ever picks from options you
  defined in advance. If your task needs generation, you still need an LLM.
- **Weak at exact math and comparisons.** Don't ask it to count words, do
  arithmetic, or compare two dates/numbers precisely — keep that in code
  (see Level 8, rule 6).
- **Literal interpretation, not inferred intent.** It answers the question
  you asked about the state you gave it — it won't reliably infer context
  you didn't include.
- **Prompt injection surface.** Since `state` is often untrusted (a user
  message, a webpage, a tool's output), adversarial content inside it could
  try to steer the answer. This is an active, unsolved problem across the
  whole industry, not unique to Jev, but worth remembering before wiring a
  Jev "risk: low" answer straight into an unattended, high-stakes action.

## The benchmark numbers are self-reported

TypeSafe's headline claims — "up to 193.6x faster and 444.6x cheaper" in
their own workflow benchmarks, "200x faster / 400x lower cost" on
classification tasks — come from **TypeSafe's own testing**, not an
independent third party. That doesn't make them false, but it does mean:

- The comparisons are against whatever baseline LLM setup TypeSafe chose to
  benchmark against, on tasks TypeSafe chose to highlight.
- Your own numbers will vary a lot by task — you saw this directly in
  [Level 6](06_jev_vs_llm_hands_on.md), where a small, fast LLM narrowed the
  gap considerably compared to TypeSafe's biggest cited multiples (which
  come from comparisons against slower, more expensive frontier reasoning
  setups on harder workflows).

Treat "Nx faster/cheaper" marketing numbers — from *any* company — as "the
best case they found," and always benchmark against your own task before
committing.

## Competitive & critical context

Jev isn't landing in a vacuum. A few things happened around the same time
that are useful context:

- **Inference-acceleration companies (e.g. Groq)** attack the same
  "LLM calls are slow and expensive" problem from a different angle: instead
  of building a new, narrower model class, they run *existing* frontier
  models faster on purpose-built chips. Different bet, same underlying pain
  point.
- **AI evaluation/guardrail companies** built the mirror-image layer:
  scoring an LLM's output *after* it's generated, rather than making a fast
  decision *before* or *during* generation. Within days of Jev's launch,
  the AI observability company Arize published an analysis titled
  *"Can Decision Models Replace LLM Judges?"* — publicly questioning how
  much of the LLM-as-judge use case a narrower decision model actually
  displaces versus complements.
- **Demand outpaced the infrastructure at launch** — TypeSafe's API
  reportedly briefly fell over under developer demand in the first days of
  early access, which is a genuine (if slightly backhanded) signal of real
  interest, not just a company's press release.

## The fair, non-hype summary

- **What's real:** a genuinely different model category, backed by a
  credible founding team, solving a real and growing cost/latency problem
  in agent loops, with a live API you can (and did, in this course) call
  yourself and get fast, structured, calibrated answers from.
- **What's still unproven:** whether the biggest headline speed/cost
  multiples hold up outside TypeSafe's own benchmarks, whether "System One
  models" become a durable new category or get absorbed into existing
  agent frameworks as a feature rather than a separate product, and how
  the security story around adversarial `state` content matures.
- **The honest one-liner:** Jev is a real, useful, narrow tool for a real
  problem (fast structured decisions inside agent loops) — not a
  replacement for LLMs, and not yet a proven long-term category, but a
  legitimate and interesting bet worth understanding regardless of how the
  market shakes out.

Next: **[Level 10 — Capstone Project](10_capstone_project.md)**, where you
put an LLM and Jev to work together, end to end.
