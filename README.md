# jev-learn

![uv](https://img.shields.io/badge/managed%20with-uv-de5fe9)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)

![Hero illustration: a small fast decision spark branching inside a larger slow-thinking brain](assets/images/hero.png)

An 11-level crash course (0-10) to understand **Jev** — the "System One"
decision model from TypeSafe AI that's been generating buzz since its
Sept 2026 launch — from zero, with hands-on, runnable examples against the
real API. Works with **any** LLM provider for the "write" half of the
examples, thanks to [LiteLLM](https://docs.litellm.ai/) — bring your own
key, including free ones.

⏱️ **Total read time: ~65 minutes** (reading + running every example),
across 11 levels — see the per-level breakdown in the table below.
Everything's numbered and self-contained, so it's just as fine to do a
level a day as it is to binge it in one sitting.

## Quick start

**1. Install [uv](https://docs.astral.sh/uv/)** (a fast Python package/project manager), if you don't have it:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS, via Homebrew
brew install uv

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**2. Clone this repo, install dependencies, and set up your keys:**

```bash
uv sync                # installs everything into a local .venv
cp .env.example .env   # then open .env and fill in your keys
```

**3. Run the hello-world sanity check:**

```bash
uv run examples/00_hello_world.py
```

If that prints a probability and a millisecond timing, you're set up.
Start reading at **[Level 0 — Hello, Jev](levels/00_hello_world.md)**.

## Get a TypeSafe API key

Every level from 0 onward calls the real Jev API, so you'll need a
`TYPESAFE_API_KEY`. Jev is in early access as of Sept 2026:

- [typesafe.ai](https://typesafe.ai/) — request access / join the waitlist
- [docs.typesafe.ai](https://docs.typesafe.ai/) — API reference
- [console.typesafe.ai](https://console.typesafe.ai/) — once approved, generate your key here

Paste it into `.env` as `TYPESAFE_API_KEY=...`.

## Bring your own model (free options)

Levels 6 and 10 also use a regular LLM for the "write" half of the pipeline
(drafting text) — Jev only decides, it never writes prose. This project
uses [LiteLLM](https://docs.litellm.ai/), so **any** provider works: just
set `CHAT_MODEL` in `.env` to a LiteLLM model string and add the matching
key. A few ways to get a free key in a couple of minutes today:

| Provider | Free key | `CHAT_MODEL` value |
|---|---|---|
| **Google AI Studio** | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — no card needed | `gemini/gemini-2.5-flash` |
| **Groq** | [console.groq.com/keys](https://console.groq.com/keys) — fast inference, free tier | `groq/<model-name-from-console>` |
| **OpenRouter** | [openrouter.ai/keys](https://openrouter.ai/keys) — aggregator, some free-tagged models | `openrouter/<model>` |
| **Ollama (local)** | none — install [ollama.com](https://ollama.com), `ollama pull llama3.2` | `ollama_chat/llama3.2` |
| **Ollama Cloud** | none — install Ollama, `ollama signin` (no card needed), `ollama pull gemma4:31b-cloud` | `ollama_chat/gemma4:31b-cloud` |

Don't sleep on **Ollama Cloud**: it's not just "install Ollama and run
everything on your laptop" — after a free `ollama signin`, your local
Ollama daemon transparently proxies any model tagged `-cloud` (including
Google's **Gemma 4**) to Ollama's own hosted infrastructure, so you get a
free, reasonably capable hosted model with zero local GPU/RAM requirements
and no separate API key to manage. Verified working via `chat_complete()`
in this repo.

⚠️ Free tiers and model availability shift often — check each provider's
own pricing/limits page for what's currently offered rather than trusting
numbers written here. `.env.example` has the exact env var names for each.

## The course

Read the levels in order — each one links to the next at the bottom.

```mermaid
flowchart LR
    L0["0. Hello World"] --> L1["1. What Is Jev?"]
    L1 --> L2["2. The Problem"]
    L2 --> L3["3. System 1 vs 2"]
    L3 --> L4["4. Three Primitives"]
    L4 --> L5["5. The Real API"]
    L5 --> L6["6. Jev vs LLM"]
    L6 --> L7["7. Agent Loop Patterns"]
    L7 --> L8["8. Confidence Gating"]
    L8 --> L9["9. Limits & Skepticism"]
    L9 --> L10["10. Capstone"]
```

| # | Level | Runnable example | Expected read time |
|---|---|---|---|
| 0 | [Hello, Jev](levels/00_hello_world.md) | `uv run` [`examples/00_hello_world.py`](examples/00_hello_world.py) | 3 min |
| 1 | [What Is Jev?](levels/01_what_is_jev.md) | — | 5 min |
| 2 | [The Problem It Solves](levels/02_the_problem_it_solves.md) | — | 6 min |
| 3 | [System One vs. System Two](levels/03_system_one_vs_system_two.md) | — | 4 min |
| 4 | [The Three Primitives](levels/04_the_three_primitives.md) | — | 5 min |
| 5 | [The Real API](levels/05_the_real_api.md) | `uv run` [`examples/05_raw_jev_call.py`](examples/05_raw_jev_call.py) | 5 min |
| 6 | [Jev vs. LLM, Hands-On](levels/06_jev_vs_llm_hands_on.md) | `uv run` [`examples/06_llm_vs_jev_timing.py`](examples/06_llm_vs_jev_timing.py) | 6 min |
| 7 | [Agent Loop Patterns](levels/07_agent_loop_patterns.md) | `uv run` [`examples/07_tool_gate_demo.py`](examples/07_tool_gate_demo.py) | 6 min |
| 8 | [Confidence-Gated Decisions](levels/08_confidence_gating_best_practices.md) | — | 5 min |
| 9 | [Limits, Hype & Skepticism](levels/09_limits_hype_and_skepticism.md) | — | 6 min |
| 10 | [Capstone Project](levels/10_capstone_project.md) | `uv run` [`examples/10_capstone_ticket_triage.py`](examples/10_capstone_ticket_triage.py) — a real project in [`capstone/`](capstone/), with [tests](tests/) and [evals](evals/) | 15 min |
| | | **Total** | **~65 min** |

`TYPESAFE_API_KEY` is required from Level 0 on. `CHAT_MODEL` + a matching
provider key is only needed for levels 6 and 10. Read times include running
the paired example and are estimates — go slower if you're pausing to poke
at the code, which is encouraged.

### Progress checklist

Fork this repo and check off levels as you go:

- [ ] 0 — Hello, Jev
- [ ] 1 — What Is Jev?
- [ ] 2 — The Problem It Solves
- [ ] 3 — System One vs. System Two
- [ ] 4 — The Three Primitives
- [ ] 5 — The Real API
- [ ] 6 — Jev vs. LLM, Hands-On
- [ ] 7 — Agent Loop Patterns
- [ ] 8 — Confidence-Gated Decisions
- [ ] 9 — Limits, Hype & Skepticism
- [ ] 10 — Capstone Project

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
levels/          11 markdown lessons (0-10), read in order
examples/        runnable scripts paired with levels 0, 5-7, and 10
capstone/        Level 10's pipeline as a real, importable package
                 (client.py, pipeline.py, cli.py)
tests/           unit tests for capstone/ — fast, free, mocked (uv run pytest)
evals/           quality checks for capstone/ against a golden dataset —
                 real API calls, tracked over time, not pass/fail
assets/images/   illustrations embedded in the levels and this README
.env             your API keys (gitignored)
```

Levels 0-9 are single scripts, each isolating one idea. Level 10 is
structured like a real project on purpose — see
[levels/10_capstone_project.md](levels/10_capstone_project.md) for why
that structure (and the unit-tests-vs-evals split) matters once you're
building something you'd actually ship.
