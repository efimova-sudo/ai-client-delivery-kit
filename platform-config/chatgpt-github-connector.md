# ChatGPT GitHub Connector Setup

This guide describes a safe setup pattern for using ChatGPT with GitHub repository context.

## Access Model

Use the minimum repository access needed for the task:

- read repository files;
- read issues and pull requests if needed for digest or delivery review;
- avoid write permissions unless explicitly approved.

## Recommended Use Cases

- summarize repository structure;
- review prompt library changes;
- prepare executive summaries from approved docs;
- inspect GitHub issues or PRs for delivery status.

## Safety Rules

- Do not expose secrets through connector context.
- Do not connect repositories containing unapproved customer data.
- Review generated outputs before sharing externally.
- Keep `client-config.yaml` local and out of git.

## Validation Before Use

Run:

```bash
python scripts/validate_prompt_library.py
pytest
```

Then confirm that only approved sample or client-safe files are available through the connector.
