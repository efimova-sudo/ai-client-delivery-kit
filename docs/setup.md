# Setup

This guide prepares the AI Client Delivery Kit for local validation and dry-run automation.

## Requirements

- Python 3.10 or newer
- Git
- Optional: a GitHub token for live API calls

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Validate the Prompt Library

```bash
python scripts/validate_prompt_library.py
```

## Run Tests

```bash
pytest
```

## Prepare a Client Workspace

Dry-run mode prints the planned output folders without creating them:

```bash
python scripts/bootstrap_repository.py --config client-config.example.yaml --dry-run
```

To create local output folders:

```bash
python scripts/bootstrap_repository.py --config client-config.example.yaml
```

Generated output folders are ignored by git.

## Generate a GitHub Digest

Dry-run mode uses sample data and does not need network access:

```bash
python scripts/github_client.py --config client-config.example.yaml --dry-run
```

To write the digest to a file:

```bash
python scripts/github_client.py --config client-config.example.yaml --dry-run --output outputs/weekly-digest.md
```

For live GitHub API calls, set `GITHUB_TOKEN` in the environment and omit `--dry-run`.
