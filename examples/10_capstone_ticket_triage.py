"""Level 10 — capstone: an LLM drafts, Jev triages and gates, end to end.

Run: uv run examples/10_capstone_ticket_triage.py

This used to be one flat script. It's now a real project, living in the
top-level `capstone/` package: business logic in `capstone/pipeline.py`,
API wrappers in `capstone/client.py`, this demo loop in `capstone/cli.py`,
unit tests in `tests/`, and a quality eval in `evals/`. This file is kept
as a thin, backward-compatible entry point so `uv run
examples/10_capstone_ticket_triage.py` still works. Read
levels/10_capstone_project.md for the full walkthrough — start there, not
here.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from capstone.cli import main

if __name__ == "__main__":
    main()
