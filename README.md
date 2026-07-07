# AI Client Delivery Kit

A compact toolkit for packaging AI delivery workflows for an example B2B SaaS client.

This repository demonstrates prompt operations, client configuration, platform setup, GitHub automation, validation, and handoff documentation in a reusable delivery system.

This repository uses fictional/sample client data only. No real customer data, secrets, or proprietary materials are included.

## What It Shows

- Prompt library with metadata, versions, inputs, outputs, and review criteria.
- Claude Code project instructions in `CLAUDE.md`.
- Agent role boundaries in `AGENTS.md`.
- ChatGPT/GitHub connector and GitHub MCP setup notes.
- Python scripts for prompt validation, repository bootstrap, and GitHub API digest generation.
- GitHub Actions for validation and scheduled weekly digest automation.
- Client-safe setup, handoff, security, and restricted-environment documentation.
- Release, tag, and changelog guidance.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python scripts/validate_prompt_library.py
pytest
```

Generate a dry-run GitHub activity digest without network access:

```bash
python scripts/github_client.py --config client-config.example.yaml --dry-run
```

## Repository Map

```text
prompts/            Versioned prompt library with YAML metadata
platform-config/    Setup guides for Claude, ChatGPT GitHub connector, and GitHub MCP
scripts/            Python automation and validation scripts
docs/               Setup, handoff, security, data-flow, and restricted-environment docs
tests/              Unit tests that run without live network access
.github/workflows/  Validation and scheduled digest workflows
```

## Client Data Policy

Use `client-config.example.yaml` as a template. For real work, copy it to `client-config.yaml`, keep that local file out of git, and provide secrets only through environment variables or approved secret managers.

The default workflow is dry-run first. Scripts should not require live GitHub access unless explicitly configured.

## Common Commands

```bash
python scripts/validate_prompt_library.py
python scripts/bootstrap_repository.py --config client-config.example.yaml --dry-run
python scripts/github_client.py --config client-config.example.yaml --dry-run
pytest
```

## Release Status

Current planned version: `0.1.0`.

See `CHANGELOG.md` for release notes and upgrade history.
See `docs/release.md` for the release checklist and tag convention.
