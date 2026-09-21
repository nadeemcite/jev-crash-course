# jev-learn

A 10-level crash course to understand **Jev** — the "System One" decision
model from TypeSafe AI that's been generating buzz since its Sept 2026
launch — from zero, with hands-on, runnable examples against the real API.

## Setup

```bash
uv sync              # installs python-dotenv, openai, requests into .venv
cp .env.example .env # then fill in OPENAI_API_KEY and TYPESAFE_API_KEY
```

`TYPESAFE_API_KEY` requires early access to Jev (waitlist as of Sept 2026 —
see [typesafe.ai](https://typesafe.ai/)). Without it, levels 1–4 and 9 (pure
reading) still work fine; levels 5–8 and 10 need it for the runnable scripts.

## The course

Read the levels in order — each one links to the next at the bottom.

| # | Level | Runnable example |
|---|---|---|
| 1 | [What Is Jev?](levels/01_what_is_jev.md) | — |
| 2 | [The Problem It Solves](levels/02_the_problem_it_solves.md) | — |
| 3 | [System One vs. System Two](levels/03_system_one_vs_system_two.md) | — |
| 4 | [The Three Primitives](levels/04_the_three_primitives.md) | — |
| 5 | [The Real API](levels/05_the_real_api.md) | `uv run examples/05_raw_jev_call.py` |
| 6 | [Jev vs. LLM, Hands-On](levels/06_jev_vs_llm_hands_on.md) | `uv run examples/06_llm_vs_jev_timing.py` |
| 7 | [Agent Loop Patterns](levels/07_agent_loop_patterns.md) | `uv run examples/07_tool_gate_demo.py` |
| 8 | [Confidence-Gated Decisions](levels/08_confidence_gating_best_practices.md) | — |
| 9 | [Limits, Hype & Skepticism](levels/09_limits_hype_and_skepticism.md) | — |
| 10 | [Capstone Project](levels/10_capstone_project.md) | `uv run examples/10_capstone_ticket_triage.py` |

## TL;DR

Jev isn't a chatbot. You send it a **state** (some text/JSON context) and
one or more **typed questions** — `noul` (yes/no probability), `choice`
(pick one of N), or `score` (position on a scale) — and it answers in
under half a second with calibrated probabilities, never prose. It's meant
to run *alongside* an LLM inside an agent loop, handling the fast
routing/gating/verification decisions so the LLM only gets used for the
parts that genuinely need generation. See [`sources.md`](sources.md) for
everything this course is based on.

## Project layout

```
levels/     10 markdown lessons, read in order
examples/   runnable scripts paired with levels 5-7 and 10
.env        your API keys (gitignored)
```
