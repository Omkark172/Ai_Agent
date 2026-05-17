---
name: python-developer
description: 'Create and test Python programs using the Python developer workflow. Use for implementing scripts, algorithms, CLI tools, and pytest suites.'
argument-hint: 'Describe the Python program, algorithm, or pytest case to create or validate.'
user-invocable: true
disable-model-invocation: false
---

# Python Developer Skill

## When to Use
- Implement Python programs, scripts, or libraries.
- Build or expand Python algorithms and data structures.
- Add pytest unit tests, edge cases, and validation.
- Refactor, debug, or improve existing Python code.

## Procedure
1. Read the user request and confirm it involves Python development.
2. Apply the engineering standards in `.github/agents/python_developer.agent.md`.
3. Produce working Python code first, then a concise rationale.
4. Add or update `pytest` tests that cover happy-path, edge cases, and failure conditions.
5. Validate the implementation by running the Python interpreter and test suite.

## Notes
- Keep code typed and mypy-clean where feasible.
- Prefer structured logging, explicit error handling, and no hardcoded secrets.
- Keep output concise and professional.
- This skill is aligned with `.github/agents/python_developer.agent.md`, collaborates with `.github/agents/python_tester.agent.md`, and is reinforced by the workspace hook in `.github/hooks/python_developer_agent.json`.
