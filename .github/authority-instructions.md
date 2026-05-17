# Agent and Hook Authority Instructions

This file defines the authoritative workflow for Python development and testing in this workspace.

## Purpose
- Ensure all Python implementation, modification, defect fixing, and testing work is handled through the workspace agents.
- Enforce use of `python-developer` for code implementation and `python-tester` for pytest validation.
- Prevent direct execution of Python tools from bypassing the agent workflow.

## Required Workflow
1. For new Python programs, use `python-developer` to write or modify code.
2. For testing Python programs, use `python-tester` to execute `pytest` and validate results.
3. After `python-tester` reports failures, hand the issue back to `python-developer` for fixes.
4. No Python program should be finalized without a successful `python-tester` validation pass.

## Hooks
The workspace hook files under `.github/hooks/` are authoritative and should be used to enforce this workflow:
- `.github/hooks/python_developer_agent.json`
- `.github/hooks/ensure_python_developer_agent.py`

These hooks should detect Python prompts and direct Python or `pytest` tool executions and route them to the appropriate agent workflow.

## Agent Guidance
- `.github/agents/python_developer.agent.md` should be used for all code implementation and defect fix work.
- `.github/agents/python_tester.agent.md` should be used for all pytest validation and test coverage work.

## Enforcement
If a prompt or tool request involves Python development or testing, the hook should:
- Recommend `python-developer` for implementation and `python-tester` for validation.
- Deny direct tool execution of Python or `pytest` commands in favor of agent workflows.

## Notes
- This file is authoritative for workspace policy and supersedes any local or user-specific memory preferences.
- Keep these instructions in sync with the hook and agent configuration files.
