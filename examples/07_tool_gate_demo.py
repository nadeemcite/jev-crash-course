"""Level 7 — using Jev as a tool-call guardrail.

Run: uv run examples/07_tool_gate_demo.py

A mock agent "proposes" a shell command. Before a fake `run_shell()` ever
executes it, we ask Jev two questions about the command in context, and
gate execution on the answers — the same shape as LangChain's
AutoModeMiddleware pattern described in levels/07_agent_loop_patterns.md.
"""

from common import call_jev

GATE_QUESTIONS = {
    "reversible": {
        "type": "noul",
        "instructions": "If this shell command runs, can its effects be easily undone?",
    },
    "risk": {
        "type": "choice",
        "instructions": "How risky is running this command, unattended, on a developer's machine?",
        "criteria": {
            "low": "Read-only or clearly safe (listing files, printing status)",
            "medium": "Modifies files but is scoped and recoverable (git commit, npm install)",
            "high": "Broad, destructive, or irreversible (deleting directories, force-pushing, dropping data)",
        },
    },
}

PROPOSED_COMMANDS = [
    "git status",
    "npm install left-pad",
    "rm -rf build/ && rm -rf dist/",
    "git push --force origin main",
]


def gate(command: str) -> None:
    state = f"A coding agent wants to run this shell command: `{command}`"
    result = call_jev(state, GATE_QUESTIONS)
    answers = result["answers"]
    reversible = answers["reversible"]["noul"]
    risk = answers["risk"]["choice"]
    confidence = answers["risk"]["confidence"]

    print(f"$ {command}")
    print(f"  reversible: {reversible:.0%} likely | risk: {risk} (confidence {confidence:.0%})")

    if risk == "low" or (risk == "medium" and confidence < 0.6):
        print("  -> ALLOW: executing automatically\n")
    elif risk == "medium":
        print("  -> CONFIRM: asking the user before running\n")
    else:
        print("  -> BLOCK: too risky to run unattended\n")


def main() -> None:
    for command in PROPOSED_COMMANDS:
        gate(command)


if __name__ == "__main__":
    main()
