# Level 2 — The Problem It Solves

## What an "AI agent" actually spends its time doing

Picture a typical AI agent loop — a coding assistant, a support-ticket bot,
a browser-automation agent. It looks roughly like this:

```mermaid
flowchart LR
    A[Observe current state] --> B["Decide what to do next 🡐 most steps are HERE"]
    B --> C[Take an action / call a tool]
    C --> D["Check whether the result is good enough 🡐 and HERE"]
    D --> E["Continue, retry, or ask a human? 🡐 and HERE"]
    E --> A
```

Watch a production agent run for real, and most individual steps are not
"write a paragraph." They're small judgment calls:

- *Which* tool should I call right now?
- Is this shell command safe to run automatically, or should I ask first?
- Is this support ticket urgent?
- Did the model's last output actually satisfy the user's request, or should
  I retry?
- Should this go to a human reviewer?

Today, almost all of these decisions get routed through the same tool used
for everything else: a full generative LLM, asked to produce structured
output (JSON) that the surrounding code then parses.

## Why that's a bad fit

Using a full reasoning LLM for a yes/no or pick-one-of-five decision has
three concrete costs:

1. **Latency.** A frontier LLM call for a structured decision typically takes
   **3–30+ seconds** (TypeSafe's own benchmarks cite up to 329 seconds in
   some workflows). If your agent makes a dozen such decisions per task,
   that adds up to a genuinely slow product.
2. **Cost.** You're paying full frontier-model token pricing to answer what
   is often a one-bit or one-of-N question.
3. **Reliability.** LLMs generate structured output *token by token*. That
   means it's possible to get truncated JSON, a hallucinated field, or an
   option that doesn't exist in your schema at all — reported error rates on
   structured-output tasks across LLMs range from under 1% to over 45%
   depending on task and model. Every one of those failures needs
   try/except and retry logic in your agent code.

None of this is really the LLM's fault — it's a generation model being
pointed at a job (constrained decision-making) that it wasn't optimized for.

## The proposed fix

TypeSafe's argument: **separate the "write" step from the "decide" step**,
and use a purpose-built model for each:

- Keep a full LLM (GPT, Claude, Gemini) for the parts of the loop that
  genuinely require open-ended reasoning or generation — drafting a reply,
  writing code, planning multiple steps ahead.
- Use **Jev** for the parts of the loop that are really just classification,
  routing, scoring, or verification — evaluate a **state**, answer one or
  more **typed questions**, get back **structured, calibrated probabilities**
  in well under a second, by construction (no partial/malformed output is
  possible, because Jev isn't generating token-by-token prose).

This is explicitly **not** a claim that Jev replaces LLMs. It's a claim that
most agent loops are doing *two different jobs* with *one tool*, and
splitting them lowers latency and cost for the "decide" half without
touching the "write" half at all.

## Why this is landing as a market moment right now (Sept 2026)

Two forces converged:

- **Agents went mainstream in 2025–2026.** Coding agents, browser agents, and
  support/ops agents moved from demos to production, which means the
  "thousands of tiny decisions per task" problem became an actual cost and
  latency line item companies started noticing.
- **A credible team is making the argument.** TypeSafe's founder co-invented
  RLHF at OpenAI — the technique behind ChatGPT's original alignment — which
  gives the "decisions need their own model class" pitch more attention than
  it would get from an unknown team, and helped it raise $40M in seed
  funding and generate strong day-one developer interest (the API reportedly
  fell over briefly at launch from demand).

We'll come back to whether the pitch fully holds up in
**[Level 9](09_limits_hype_and_skepticism.md)** — for now, the point is just
to understand *what gap* Jev is claiming to fill.

Next: **[Level 3 — System One vs. System Two](03_system_one_vs_system_two.md)**.

<details>
<summary>🧠 Try it yourself</summary>

Pick a real agent, workflow, or app you've built or used recently (a coding
assistant, a support bot, a form-processing script — anything with a
loop). List 3 decision points inside its loop, and for each one write down:
whether it's currently a hardcoded `if`, an LLM call, or a human — and
whether Jev-style typed questions (`noul`/`choice`/`score`) could replace
whichever one it currently is.

</details>
