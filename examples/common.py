"""Shared helpers for the Jev crash course examples.

Loads .env once and exposes:
- `call_jev()`      — a thin wrapper around the real TypeSafe System One API
- `chat_complete()` — a model-agnostic "write" helper via LiteLLM, so the
                       course works with OpenAI, Anthropic, Gemini, Groq,
                       OpenRouter, local Ollama, or anything else LiteLLM
                       supports, just by changing CHAT_MODEL in .env.

Nothing here is Jev's own SDK — call_jev is a deliberately thin wrapper so
you can see exactly what's going over the wire.
"""

from __future__ import annotations

import os
import time

import requests
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"

# Any LiteLLM-style model string: "gpt-4o-mini", "gemini/gemini-2.5-flash",
# "groq/<model>", "ollama_chat/llama3.2", etc. See README "Bring Your Own Model".
DEFAULT_CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")


def require_key(name: str) -> str:
    """Fetch an env var or fail with a clear, actionable message."""
    value = os.getenv(name)
    if not value:
        raise SystemExit(
            f"Missing {name} in .env — copy .env.example to .env and fill it in."
        )
    return value


def call_jev(state: str, questions: dict, model: str = "jev-latest") -> dict:
    """Call the real Jev (System One) API.

    `questions` is a dict of name -> question spec, e.g.:
        {
            "is_urgent": {"type": "noul", "instructions": "..."},
            "department": {"type": "choice", "instructions": "...",
                            "criteria": {"billing": "...", "technical": "..."}},
            "frustration": {"type": "score", "instructions": "...",
                             "criteria": ["calm", "annoyed", "furious"]},
        }

    Returns the parsed JSON response. Raises for non-200 responses so
    schema mistakes (e.g. `score` criteria must be a *list*, not a dict)
    surface immediately instead of failing silently.
    """
    key = require_key("TYPESAFE_API_KEY")
    started = time.perf_counter()
    resp = requests.post(
        JEV_ENDPOINT,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "state": state, "questions": questions},
        timeout=15,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    resp.raise_for_status()
    data = resp.json()
    data["_elapsed_ms"] = round(elapsed_ms, 1)
    return data


def chat_complete(prompt: str, model: str | None = None, **kwargs) -> str:
    """Ask any LLM to write something, via LiteLLM.

    `model` accepts any LiteLLM model string — "gpt-4o-mini" (default),
    "claude-haiku-4-5-20251001", "gemini/gemini-2.5-flash", "groq/<model>",
    "ollama_chat/llama3.2" (local), "ollama_chat/gemma4:31b-cloud" (free,
    hosted — no local hardware needed), etc. If omitted, uses CHAT_MODEL
    from .env (or "gpt-4o-mini" if that's not set either). LiteLLM reads
    the matching provider API key from the environment automatically —
    see README "Bring Your Own Model" for where to get one for free.
    """
    resp = completion(
        model=model or DEFAULT_CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    return resp.choices[0].message.content
