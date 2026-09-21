"""Thin wrappers around the Jev API and LiteLLM.

This mirrors `examples/common.py` almost exactly — duplicated on purpose.
The capstone is meant to be a standalone real project you could hand to
someone else; it shouldn't secretly depend on a sibling tutorial folder.
In a larger codebase, this is the kind of module you'd usually pull out
into a shared internal package once more than one project needs it.
"""

from __future__ import annotations

import os
import time

import requests
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"
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
    """Call the real Jev (System One) API. See examples/common.py for the
    full explanation of the request/response shape."""
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
    """Ask any LLM to write something, via LiteLLM. Defaults to CHAT_MODEL
    from .env — see README "Bring Your Own Model"."""
    resp = completion(
        model=model or DEFAULT_CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    return resp.choices[0].message.content
