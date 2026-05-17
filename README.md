An AI-powered Python development workflow using GitHub Copilot agents for automatic code generation, testing, and validation.

Features
AI-assisted Python code generation
Automatic test creation
Pytest integration
Agent-based development workflow
Hook-based automation
Organized skill and instruction system

AI_AGENT/
agents/
│python_developer.agent.md
│python_tester.agent.md

hooks/
│ensure_python_developer_agent.py
│python_developer_agent.json

skills/
│python-developer/
│SKILL.md

├merge_sort.py
├test_merge_sort.py
├README.md
├.gitignore

├.github/
├.venv/
├__pycache__/
└.pytest_cache/

How It Works

This project uses GitHub Copilot agent workflows to:

Generate Python code automatically
Create corresponding test cases
Run tests using python_tester.agent.md
Validate implementation through hooks

The developer agent creates logic and functionality, while the tester agent verifies correctness through automated testing.
