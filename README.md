# AI Client Delivery Kit

[![Validate](https://github.com/efimova-sudo/ai-client-delivery-kit/actions/workflows/validate.yml/badge.svg)](https://github.com/efimova-sudo/ai-client-delivery-kit/actions/workflows/validate.yml)

A compact toolkit for packaging AI-assisted delivery workflows for an example B2B SaaS client.

This repository shows how client-facing AI work can be made repeatable, reviewable, and safe to adapt across accounts. It combines prompt operations, client configuration, platform setup, GitHub automation, validation, and handoff documentation in a reusable delivery system.

This repository uses fictional/sample client data only. No real customer data, secrets, or proprietary materials are included.

## Why This Exists

AI-assisted delivery often starts as one-off chat work: useful, but hard to review, hand off, or repeat for another client. This kit turns that work into a structured operating pattern with versioned prompts, explicit inputs and outputs, dry-run automation, validation, and client-safe documentation.

The goal is to keep the workflow lightweight while making the important parts inspectable: what data is used, which prompts produce which deliverables, how outputs are reviewed, where automation runs, and how secrets stay out of the repository.

## Use Cases

- Prepare an AI delivery workspace for a sample or client-approved account.
- Maintain a reusable prompt library with metadata, versioning, and review criteria.
- Generate account research notes, executive briefs, and quality review notes from approved inputs.
- Run a dry-run GitHub activity digest before connecting live repository access.
- Hand off setup, security, and operating guidance to a client team or internal delivery owner.

## What This Kit Includes

- Prompt library with metadata, versions, inputs, outputs, and review criteria.
- Claude Code project instructions in `CLAUDE.md`.
- Agent role boundaries in `AGENTS.md`.
- ChatGPT/GitHub connector and GitHub MCP setup notes.
- Python scripts for prompt validation, repository bootstrap, and GitHub API digest generation.
- GitHub Actions for validation and scheduled weekly digest automation.
- Curated sample outputs in `examples/`.
- Client-safe setup, handoff, security, and restricted-environment documentation.
- Release, tag, and changelog guidance.

## Operating Model

The repository is organized around a simple delivery flow:

```text
client-config.example.yaml
        |
        v
prompt library + scripts
        |
        v
validation + GitHub API digest
        |
        v
handoff documentation / client deliverables
```

`client-config.example.yaml` defines the sample client context, engagement objective, deliverables, security posture, and dry-run defaults. The prompt library defines reusable delivery tasks. Scripts validate the prompt library, prepare local workspaces, and generate GitHub activity digests. Documentation explains setup, data flow, restricted-environment options, release steps, and handoff criteria.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python scripts/validate_prompt_library.py
pytest
```

Generate a dry-run GitHub activity digest without network access:

```bash
python scripts/github_client.py --config client-config.example.yaml --dry-run
```

Generate a live GitHub digest only after configuring a local client config and exporting a read-only token:

```bash
export GITHUB_TOKEN=...
python scripts/github_client.py --config client-config.yaml --live
```

## Sample Outputs

Curated examples show the shape of deliverables without relying on live customer data:

- `examples/weekly-digest.sample.md`
- `examples/executive-brief.sample.md`

## Automation

The repository includes two GitHub Actions workflows:

- `Validate` runs on push, pull request, or manual dispatch. It installs the project, validates the prompt library, and runs tests in a clean GitHub-hosted environment.
- `Weekly Digest` runs on a weekly schedule or manual dispatch. It generates a dry-run GitHub activity digest and uploads the result as a workflow artifact.

Both workflows are designed to be inspectable before live client use. The weekly digest workflow intentionally passes `--dry-run`; live digest generation is an explicit local or reviewed workflow choice through `--live`.

## Safety And Review

The default posture is dry-run first:

- committed files use sample data only;
- `client-config.yaml` stays local and ignored by git;
- secrets come from environment variables or approved secret managers;
- tests do not require live network access;
- generated outputs stay in `outputs/`, which is ignored by git;
- prompts are expected to separate facts from assumptions and flag missing context.

Before adapting the kit for real client work, review `docs/security.md`, `docs/data-flow.md`, and `docs/handoff.md`.

## Repository Map

```text
prompts/            Versioned prompt library with YAML metadata
platform-config/    Setup guides for Claude, ChatGPT GitHub connector, and GitHub MCP
scripts/            Python automation and validation scripts
docs/               Setup, handoff, security, data-flow, and restricted-environment docs
examples/           Curated sample deliverables based on fictional data
tests/              Unit tests that run without live network access
.github/workflows/  Validation and scheduled digest workflows
```

## Adapting For Client Work

Use `client-config.example.yaml` as a template. For real work, copy it to `client-config.yaml`, keep that local file out of git, and provide secrets only through environment variables or approved secret managers.

The default workflow is dry-run first. Scripts should not require live GitHub access unless explicitly configured.

Before live use:

1. Replace sample config values with approved client-specific values.
2. Confirm token scopes and repository permissions.
3. Run prompt validation and tests.
4. Generate the digest in dry-run mode.
5. Review generated outputs before external sharing.

## Common Commands

```bash
python scripts/validate_prompt_library.py
python scripts/bootstrap_repository.py --config client-config.example.yaml --dry-run
python scripts/github_client.py --config client-config.example.yaml --dry-run
python scripts/github_client.py --config client-config.yaml --live
pytest
```

## Release Status

Latest tagged version: `v0.1.1`.

See `CHANGELOG.md` for release notes and upgrade history.
See `docs/release.md` for the release checklist and tag convention.
