# AGENTS.md

**This is the authoritative agent development guide for the scenario-labs repository. Do not reference or create other AGENTS.md files.**

This document defines standards, practices, and expectations for designing, building, testing, and documenting agentic functionality. It is intended for developers, product managers, and contributors to ensure high-quality, reproducible work with strong simulation outcomes.


## Project Overview
**Scenario-labs** is a Python framework for building and running multi-agent conversational simulations using LLMs (e.g., OpenAI, Google, xAI). It supports:

* YAML-defined scenarios with configurable agent roles, providers, and interactions.
* Parallelized simulation execution.
* Rich logging and structured data for analysis and downstream tooling.

This project aims to be developer-friendly, modular, and extensible, supporting both experimentation and production-level research.


## Environment Setup
Before doing anything:

1. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```
2. Check for `Makefile` or build scripts:

   * These scripts help automate environment setup, build steps, and dependency installs.
   * Use them to ensure consistency.


## Core Commands
* **Build**: `make build` — Installs dependencies and builds wheel via Hatch
* **Lint**: `make lint` — Runs Black & Ruff with auto-fix
* **Security Scan**: `make bandit` — Scans `src/` with Bandit using `pyproject.toml` config
* **Run All Tests**: `make test` — Executes the full test suite with pytest
* **Run Single Test**: `pytest -s tests/test_file.py::test_function`

Use `-v` with pytest for verbose output during debugging.


## Testing Guidelines
* Tests should not fail due to lack of network connectivity:
* Skip or shim remote-dependent tests to a success state if connectivity isn't detected.
* Use environment-aware test design. Override `XDG_CONFIG_HOME` in integration tests to ensure full test determinism within the repository.

## Code Style and Architecture
### General
* Code must be modular, readable, and typed.
* Leverage abstract base classes when designing reusable components.
* Write docstrings for every function, method, and class — use Google or NumPy style.

### Style Guide
* **Formatting**: Use Black. Run `make lint` to auto-format.
* **Typing**: Not required. Should be sane and consistent.
* **Imports**: Be explicit (e.g., `from x import y`). Avoid wildcards.
* **Naming**: Use `snake_case` for variables/functions, `CamelCase` for classes.
* **Constants**: Use `UPPER_CASE`.
* **Error Handling**: Raise specific exceptions. Avoid silent failures.
* **Comments**: Add meaningful comments where logic is non-obvious.

## Best Practices
### Development
* Never commit directly as an agent. Human review and commit is mandatory.
* Every function must have unit tests — target full branch coverage.
* Add integration tests for validating end-to-end agent behavior.

### CLI and Output Support
* Design support for multiple CLI tool conventions (different flag styles, output formats).
* Provide docstrings or CLI help descriptions for every argument and config option.


## Planning and Task Management
### Planning Guidelines
* Understand the problem deeply before coding.
* Ask clarifying questions. Do not assume.


## Never Do
These rules are absolute:

* Do not include CLI-generated attribution in commit messages.
* Do not commit code directly as an agent. Human commits only.
* Do not write vague TODOs or tasks without proper documentation.


## Final Thoughts
This project is meant to be both a toolkit and a canvas.

* Engineers: Focus on modularity, testability, extensibility.
* Artists: Focus on clarity, interaction flow, and user empathy.
* Product Managers: Insist on clear specs, transparent planning, and visible feedback loops.
* Users: Should find it easy to prototype, configure, and extend.


Build with clarity. Ship with pride.
