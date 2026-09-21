"""Level 0 — hello world. Proves your setup works before anything else does.

Run: uv run examples/00_hello_world.py

Only needs TYPESAFE_API_KEY — no LLM, no litellm, nothing else. If this
prints an answer, your .env and network access are good and you're ready
for levels/01_what_is_jev.md.
"""

from common import call_jev

if __name__ == "__main__":
    result = call_jev(
        state="It is raining heavily and the streets are flooding.",
        questions={
            "should_bring_umbrella": {
                "type": "noul",
                "instructions": "Should someone heading outside bring an umbrella?",
            }
        },
    )

    probability = result["answers"]["should_bring_umbrella"]["noul"]
    print(f"Hello, Jev! P(bring umbrella) = {probability:.0%}")
    print(f"(round trip took {result['_elapsed_ms']} ms)")
