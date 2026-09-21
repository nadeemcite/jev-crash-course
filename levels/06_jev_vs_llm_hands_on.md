# Level 6 — Jev vs. LLM, Hands-On

Time to stop reading claims and measure something yourself. This level runs
the **exact same task** — "how urgent is this support message, and which
department should handle it?" — two different ways against your own API
keys, and compares them.

## Approach A: a general-purpose LLM (`OPENAI_API_KEY`)

Ask GPT to read the message and return JSON with the same two fields. This
is the standard way most agents do routing/classification today: a prompt
plus `response_format={"type": "json_object"}` plus a `json.loads()` and a
prayer that the model followed the schema.

## Approach B: Jev (`TYPESAFE_API_KEY`)

Send the identical message as `state`, ask the same two questions as typed
`noul`/`choice` questions, get back a guaranteed-shaped answer with
calibrated probabilities.

## Run it

```bash
uv run examples/06_llm_vs_jev_timing.py
```

The script runs both approaches across a handful of test messages and
prints a small comparison table: latency, whether the LLM's JSON parsed
cleanly on the first try, and the answers from both sides.

## What to actually look for in the output

1. **Latency gap.** Even against a small, fast model like `gpt-4o-mini` you
   should see Jev come back noticeably quicker (roughly 1.5-3x in casual
   runs of this script) because it isn't generating text token-by-token at
   all. TypeSafe's own benchmarks show the gap widening to 10-100x+ against
   larger "reasoning" models doing multi-step structured-output tasks — this
   script uses a cheap model on purpose so you can actually see both sides
   respond quickly, not to reproduce their biggest headline number.
2. **Format reliability.** The script deliberately does *not* retry on a
   malformed GPT JSON response — watch whether that ever happens across your
   run. Jev's answer shape is guaranteed by construction; GPT's isn't (even
   with `response_format` hints, it's still generating tokens that *could*
   theoretically go wrong, just less often than free-form prompting).
3. **What you *don't* get from Jev.** Notice Jev never explains itself in
   prose — no "I think this is billing because...". If you need a
   human-readable rationale attached to a decision, that's a job for the LLM
   side, not Jev. This is the tradeoff, not a bug.

## The honest conclusion

This isn't a "Jev wins" exercise. For a **single, isolated call**, an LLM
with a tight prompt can produce a perfectly good classification too — the
gap only compounds when a decision like this happens **dozens or hundreds of
times per task**, inside a loop, where the latency and cost multiply and a
single malformed JSON response can stall an entire agent run. That's the
actual argument for a separate decision-model layer, and it's the subject of
[Level 7](07_agent_loop_patterns.md).

Next: **[Level 7 — Agent Loop Patterns](07_agent_loop_patterns.md)**.
