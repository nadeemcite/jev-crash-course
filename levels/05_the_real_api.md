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
[`examples/common.py`](../examples/common.py)) instead of the SDK, so you
can see exactly what's happening on the wire with no abstraction in the way.

## `examples/common.py`, explained

Every runnable example from here on (`05` through `10`) starts with
`from common import ...`. It's a small shared file, not a hidden SDK — read
it once and every later example is instantly familiar. It exports three
things:

- **`require_key(name)`** — reads an env var and, if it's missing, exits
  with a message telling you to copy `.env.example` to `.env` and fill it
  in. Every example fails this way instead of with a raw `KeyError` or a
  confusing 401 from the API three lines later.
- **`call_jev(state, questions, model="jev-latest")`** — does exactly the
  HTTP request shown above with `requests.post()`: reads
  `TYPESAFE_API_KEY` via `require_key()`, POSTs `{model, state, questions}`
  to the endpoint, times the round trip, and returns the parsed JSON with
  a `_elapsed_ms` field bolted on so every example can print the real
  latency. `resp.raise_for_status()` means a malformed `questions` schema
  (like giving `score` a dict instead of a list) fails loudly and
  immediately, not silently.
- **`chat_complete(prompt, model=None, **kwargs)`** — the "write" half,
  used only in Levels 6 and 10 where an LLM drafts prose. It calls
  `litellm.completion()` instead of any single provider's SDK, which is
  what makes "bring your own model" possible: `model` defaults to
  `CHAT_MODEL` from `.env` (or `gpt-4o-mini` if that's unset), and LiteLLM
  reads whichever provider's API key matches that model string. Swapping
  providers is a one-line `.env` edit, never a code change — see the
  README's "Bring Your Own Model" section.

`call_jev()` never calls an LLM, and `chat_complete()` never touches the
Jev endpoint — keeping them separate is the same "decide vs. write" split
this whole course is about, just at the code level instead of the
conceptual one.

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
we run the *same* task through an LLM and through Jev side by side.

<details>
<summary>🧠 Try it yourself</summary>

Edit [`examples/05_raw_jev_call.py`](../examples/05_raw_jev_call.py) to add
a third question of type `score`
to the same request (pick any scale you like — formality, technicality,
optimism). Re-run it and confirm the `_elapsed_ms` barely moves compared to
the two-question version — that's the "adding questions is nearly free"
claim from [Level 4](04_the_three_primitives.md), verified with your own
eyes.

</details>
