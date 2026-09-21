# Level 0 — Hello, Jev

Before any theory: prove your setup works.

## Setup (2 minutes)

```bash
uv sync                          # install dependencies
cp .env.example .env             # then open .env and paste in your key
uv run examples/00_hello_world.py
```

You only need `TYPESAFE_API_KEY` for this one — no OpenAI key, no LiteLLM,
nothing else. If you don't have a TypeSafe key yet, see the README's
**"Get a TypeSafe API key"** section.

## What it does

[`examples/00_hello_world.py`](../examples/00_hello_world.py) asks Jev a
single yes/no (`noul`) question about one hardcoded sentence and prints the
probability it comes back with:

```
Hello, Jev! P(bring umbrella) = 94%
(round trip took 187.3 ms)
```

Your number and timing will differ — that's fine. What matters is that you
got *a* number back in well under a second, with no prose, no chat, just a
calibrated probability. That's the entire shape of Jev, in miniature.

## Checkpoint

- [ ] Script ran without a `Missing TYPESAFE_API_KEY` error
- [ ] You saw a probability and a millisecond timing printed

If both are checked, you're fully set up. Next: **[Level 1 — What Is
Jev?](01_what_is_jev.md)**, where we unpack what you just called and why it
exists.
