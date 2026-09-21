# Level 6 — Jev vs. LLM, Hands-On

Time to stop reading claims and measure something yourself. This level runs
the **exact same task** — "how urgent is this support message, and which
department should handle it?" — two different ways against your own API
keys, and compares them.

## Approach A: a general-purpose LLM (`CHAT_MODEL`)

Ask an LLM to read the message and return JSON with the same two fields.
This is the standard way most agents do routing/classification today: a
prompt asking for JSON, then a `json.loads()` and a prayer that the model
followed the schema.

The script calls whatever model you've set as `CHAT_MODEL` in `.env`
(default `gpt-4o-mini`) via [LiteLLM](https://docs.litellm.ai/), so this
works identically with OpenAI, Anthropic, Gemini, Groq, OpenRouter, or a
local Ollama model — see the README's "Bring Your Own Model" section if you
don't have a key yet.

## Approach B: Jev (`TYPESAFE_API_KEY`)

Send the identical message as `state`, ask the same two questions as typed
`noul`/`choice` questions, get back a guaranteed-shaped answer with
calibrated probabilities.

## Run it

```bash
uv run examples/06_llm_vs_jev_timing.py
```

Open [`examples/06_llm_vs_jev_timing.py`](../examples/06_llm_vs_jev_timing.py)
alongside the output — it runs both approaches across a handful of test
messages and prints a small comparison table: latency, whether the LLM's
JSON parsed cleanly on the first try, and the answers from both sides.

## What to actually look for in the output

1. **Latency gap.** Even against a small, fast model like `gpt-4o-mini` you
   should see Jev come back noticeably quicker (roughly 1.5-3x in casual
   runs of this script) because it isn't generating text token-by-token at
   all. TypeSafe's own benchmarks show the gap widening to 10-100x+ against
   larger "reasoning" models doing multi-step structured-output tasks — this
   script uses a cheap model on purpose so you can actually see both sides
   respond quickly, not to reproduce their biggest headline number.
2. **Format reliability.** The script deliberately does *not* retry on a
   malformed LLM JSON response — watch whether that ever happens across your
   run. Jev's answer shape is guaranteed by construction; an LLM's isn't
   (even with a "return only JSON" instruction, it's still generating tokens
   that *could* theoretically go wrong, just less often than free-form
   prompting — and reliability varies noticeably by provider and model).
3. **What you *don't* get from Jev.** Notice Jev never explains itself in
   prose — no "I think this is billing because...". If you need a
   human-readable rationale attached to a decision, that's a job for the LLM
   side, not Jev. This is the tradeoff, not a bug.

Try swapping `CHAT_MODEL` to a different provider (e.g.
`gemini/gemini-2.5-flash`, local `ollama_chat/llama3.2`, or free hosted
`ollama_chat/gemma4:31b-cloud`) and re-running — the
latency gap and JSON reliability both shift depending on which model you
pick, which is itself part of the point: Jev's behavior here is constant
regardless of provider; a general LLM's isn't.

## The honest conclusion

This isn't a "Jev wins" exercise. For a **single, isolated call**, an LLM
with a tight prompt can produce a perfectly good classification too — the
gap only compounds when a decision like this happens **dozens or hundreds of
times per task**, inside a loop, where the latency and cost multiply and a
single malformed JSON response can stall an entire agent run. That's the
actual argument for a separate decision-model layer, and it's the subject of
[Level 7](07_agent_loop_patterns.md).

Next: **[Level 7 — Agent Loop Patterns](07_agent_loop_patterns.md)**.
