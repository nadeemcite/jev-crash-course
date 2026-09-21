"""Shared helpers for the Jev crash course examples.

Loads .env once and exposes a tiny `call_jev()` wrapper around the real
TypeSafe System One API, plus a couple of small utilities used by several
level scripts. Nothing here is Jev's own SDK — it's a deliberately thin
wrapper so you can see exactly what's going over the wire.
"""

from __future__ import annotations

import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"


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


def openai_client():
    """Return an OpenAI client, failing clearly if the key is missing."""
    from openai import OpenAI

    return OpenAI(api_key=require_key("OPENAI_API_KEY"))
