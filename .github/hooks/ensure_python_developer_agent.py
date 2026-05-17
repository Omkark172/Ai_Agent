"""Hook helper to encourage Python development requests to use python-developer and python-tester agents."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

PYTHON_KEYWORDS = re.compile(r"\bpython\b", flags=re.IGNORECASE)
PYTHON_TASK_KEYWORDS = re.compile(
    r"\b(create|build|write|implement|test|run|debug|script|program|project|application)\b",
    flags=re.IGNORECASE,
)
PYTHON_TEST_KEYWORDS = re.compile(
    r"\b(test|validate|validation|pytest|unittest|coverage|assertions?)\b",
    flags=re.IGNORECASE,
)


def extract_prompt(payload: dict[str, Any]) -> str | None:
    candidates = [
        payload.get("prompt"),
        payload.get("userPrompt"),
        payload.get("text"),
        payload.get("input"),
    ]

    for candidate in candidates:
        if isinstance(candidate, str):
            return candidate
        if isinstance(candidate, list):
            return "\n".join(str(item) for item in candidate)

    messages = payload.get("messages") or payload.get("conversation")
    if isinstance(messages, list):
        text_parts = []
        for message in messages:
            if isinstance(message, str):
                text_parts.append(message)
            elif isinstance(message, dict):
                content = message.get("content") or message.get("text")
                if isinstance(content, str):
                    text_parts.append(content)
        if text_parts:
            return "\n".join(text_parts)

    return None


def should_trigger_agent(prompt: str) -> bool:
    text = prompt.lower()
    return bool(
        PYTHON_KEYWORDS.search(text)
        and (PYTHON_TASK_KEYWORDS.search(text) or PYTHON_TEST_KEYWORDS.search(text))
    )


def should_recommend_tester(prompt: str) -> bool:
    text = prompt.lower()
    return bool(PYTHON_KEYWORDS.search(text) and PYTHON_TEST_KEYWORDS.search(text))


def extract_command(payload: dict[str, Any]) -> str | None:
    candidates = [
        payload.get("command"),
        payload.get("toolName"),
        payload.get("toolCommand"),
        payload.get("toolArgs"),
        payload.get("input"),
        payload.get("text"),
    ]

    for candidate in candidates:
        if isinstance(candidate, str):
            return candidate
        if isinstance(candidate, list):
            return " ".join(str(item) for item in candidate)

    if isinstance(payload.get("messages"), list):
        for message in payload["messages"]:
            if isinstance(message, dict):
                content = message.get("content") or message.get("text")
                if isinstance(content, str):
                    return content

    return None


def is_python_execution(text: str) -> bool:
    return bool(
        re.search(r"\bpython\b", text, flags=re.IGNORECASE)
        or re.search(r"\.py\b", text, flags=re.IGNORECASE)
        or re.search(r"\bpytest\b", text, flags=re.IGNORECASE)
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    hook_event = payload.get("hookEventName") or payload.get("event") or payload.get("hookEvent")
    command_text = extract_command(payload) or ""

    if hook_event == "PreToolUse" and is_python_execution(command_text):
        print(
            json.dumps(
                {
                    "continue": False,
                    "systemMessage": (
                        "Direct Python or pytest execution is blocked by the authority workflow. "
                        "Use the `python-developer` agent for implementation requests and the `python-tester` agent for pytest validation."
                    ),
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            "Direct Python and pytest commands are blocked so Python development and testing must proceed through the approved agent workflow."
                        ),
                    },
                }
            )
        )
        return 0

    prompt_text = extract_prompt(payload)
    if prompt_text and should_trigger_agent(prompt_text):
        if should_recommend_tester(prompt_text):
            system_message = (
                "This prompt appears to be a Python testing or pytest validation request. "
                "Use the `python-tester` agent as the primary handler for Python testing and pytest validation. "
                "After validation, route any required code fixes back to `python-developer`."
            )
        else:
            system_message = (
                "This prompt appears to be a Python development request. "
                "Use the `python-developer` agent for implementation, and send pytest validation to `python-tester`. "
                "Python code is not final until `python-tester` confirms pytest validation has passed."
            )

        print(
            json.dumps(
                {
                    "continue": True,
                    "systemMessage": system_message,
                }
            )
        )
        return 0

    print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
