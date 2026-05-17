import json
import subprocess
import sys
from pathlib import Path

HOOK_SCRIPT = Path(__file__).parent / ".github" / "hooks" / "ensure_python_developer_agent.py"


def run_hook(payload: dict) -> dict:
    process = subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(HOOK_SCRIPT.parent),
        check=True,
    )
    return json.loads(process.stdout)


def test_prompt_detection_triggers_python_developer_and_tester():
    payload = {
        "hookEventName": "UserPromptSubmit",
        "prompt": "Please write a Python script to sort a list of numbers using merge sort.",
    }

    result = run_hook(payload)

    assert result["continue"] is True
    assert "python-developer" in result["systemMessage"]
    assert "python-tester" in result["systemMessage"]


def test_pytest_validation_prompt_recommends_python_tester():
    payload = {
        "hookEventName": "UserPromptSubmit",
        "prompt": "Please validate the Python merge sort implementation using pytest and report any failures.",
    }

    result = run_hook(payload)

    assert result["continue"] is True
    assert "python-tester" in result["systemMessage"]
    assert "pytest validation" in result["systemMessage"] or "pytest" in result["systemMessage"]


def test_direct_python_command_is_denied_for_pretooluse():
    payload = {
        "hookEventName": "PreToolUse",
        "command": "python script.py",
    }

    result = run_hook(payload)

    assert result["continue"] is False
    assert result["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "Direct Python and pytest commands are blocked" in result["hookSpecificOutput"]["permissionDecisionReason"]


def test_direct_pytest_command_is_denied_for_pretooluse():
    payload = {
        "hookEventName": "PreToolUse",
        "command": "pytest -q test_merge_sort.py",
    }

    result = run_hook(payload)

    assert result["continue"] is False
    assert result["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "Direct Python and pytest commands are blocked" in result["hookSpecificOutput"]["permissionDecisionReason"]


def test_development_prompt_recommends_python_developer_and_python_tester_confirmation():
    payload = {
        "hookEventName": "UserPromptSubmit",
        "prompt": "Please implement a Python module that parses CSV data and generates a summary report.",
    }

    result = run_hook(payload)

    assert result["continue"] is True
    assert "python-developer" in result["systemMessage"]
    assert "python-tester" in result["systemMessage"]
    assert "not final" in result["systemMessage"].lower() or "confirm" in result["systemMessage"].lower()
