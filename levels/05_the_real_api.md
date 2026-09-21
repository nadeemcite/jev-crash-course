# Level 5 — The Real API

## Endpoint & auth

```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <TYPESAFE_API_KEY>
Content-Type: application/json
```

One endpoint handles everything — there's no separate route per question
type. The request body always has the same three fields:

```json
{
  "model": "jev-latest",
  "state": "<text or JSON — the context to evaluate>",
  "questions": { "<name>": { "type": "noul|choice|score", "instructions": "...", "criteria": ... } }
}
```

- `model` — `"jev-latest"` is the SDK/docs default and always points at the
  current model (currently resolves to `jev-1.13.0`).
- `state` — what you want evaluated: a raw string, or a JSON object/array of
  text. Images/audio/video aren't supported yet.
- `questions` — a map of as many named questions as you want (see
  [Level 4](04_the_three_primitives.md) for the three shapes).

## SDKs

- Python: `typesafe-sdk` (PyPI)
- JS/TS: `@typesafe-ai/sdk` (npm)
- Also reachable through OpenRouter, Vercel AI Gateway, Netlify AI Gateway,
  AIMLAPI, and LiteLLM if you'd rather go through a gateway you already use.

This course calls the raw HTTP API directly with `requests` (see
`examples/common.py`) instead of the SDK, so you can see exactly what's
happening on the wire with no abstraction in the way.

## Pricing

**$0.042 per million input tokens. Output tokens are free**, since Jev
returns a small typed structure, not generated prose — there's no per-token
generation cost to pass on. For scale: `usage.input_tokens` on a typical
two-question call in this course is in the 300–400 token range, which at
that price is a rounding error per call.

## Run it

```bash
uv run examples/05_raw_jev_call.py
```

Open [`examples/05_raw_jev_call.py`](../examples/05_raw_jev_call.py) and read
it alongside the output — it sends one `state` with a `noul` and a `choice`
question, and prints the full response including the real latency of the
call (`_elapsed_ms`), so you can see the "under 500ms" claim for yourself
rather than take it on faith.

Next: **[Level 6 — Jev vs. LLM, Hands-On](06_jev_vs_llm_hands_on.md)**, where
we run the *same* task through GPT and through Jev side by side.
