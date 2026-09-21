# Level 1 — What Is Jev?

![Illustration: a small glowing decision point branching into several arrows inside a larger head silhouette](../assets/images/hero.png)

## The one-paragraph version

**Jev** is an AI model made by a startup called **TypeSafe AI**. It came out of
stealth on **September 15, 2026**, backed by a **$40M seed round** led by DCVC.
Unlike ChatGPT, Claude, or Gemini, Jev doesn't chat and doesn't write text at
all. You give it some context (called a **state**) and one or more **typed
questions**, and it hands back a structured, probability-scored answer in
under half a second. TypeSafe calls this category of model a **"System One"
model** — the first of a new class of AI built to make fast, small decisions
*inside software*, not to talk to people.

That's it. That's the whole idea. Everything else in this course is
elaboration on that one paragraph.

## Who built it, and why the name

- **Founder/CEO:** Diogo Almeida — a former OpenAI researcher, credited as a
  co-inventor of **RLHF** (the technique that made ChatGPT possible in the
  first place).
- **Co-founders:** Erik Gafni and Sasha Sheng.
- **Funding:** $40M seed, led by DCVC (a firm known for backing "deep tech,"
  not just app-layer AI wrappers).

The name "Jev" is a nod to the **Jevons paradox** — the 19th-century economic
observation that making a resource *more efficient* to use often increases
total consumption of it, rather than decreasing it (more efficient steam
engines led to *more* coal being burned, not less). TypeSafe's bet: making
decisions 100-400x cheaper won't mean agents make the same number of
decisions for less money — it means they'll make *far more* decisions than
they do today, because suddenly it's cheap enough to ask.

## The "smart `if` statement" mental model

![Illustration: a signpost fork where one road glows and one branch trails off](../assets/images/smart-if-statement.png)

The most useful way to think about Jev, before any of the technical detail:

> Jev is a **smart `if` statement**. Instead of writing brittle rules
> (`if "urgent" in message.lower()`), you ask a model a well-defined question
> and get back a typed, calibrated answer you can branch on in code — the
> same way you'd branch on a boolean or an enum.

It sits at a very different point in your stack than a chatbot does:

```
Chatbot / reasoning LLM   →  writes things (replies, code, summaries, plans)
Jev / "System One" model  →  decides things (routing, gating, scoring, verifying)
```

## Quick facts to anchor the rest of the course

| | |
|---|---|
| Made by | TypeSafe AI |
| First model | Jev (`jev-latest`, currently `jev-1.13.0`) |
| Category name | "System One" model |
| Launched | Sept 15, 2026 (early access / waitlist) |
| Typical latency | ~70–500ms |
| Pricing | $0.042 / million **input** tokens, output tokens are free |
| Input types | text, JSON, arrays of text (no images/audio/video yet) |
| What it returns | typed answers + calibrated probabilities, never prose |

Next: **[Level 2 — The Problem It Solves](02_the_problem_it_solves.md)**, which
explains *why* something like this exists at all — what's actually broken
about using regular LLMs for this job today.
