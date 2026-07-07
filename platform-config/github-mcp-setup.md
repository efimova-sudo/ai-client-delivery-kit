# GitHub MCP Setup

This guide describes a safe pattern for using GitHub MCP with the AI Client Delivery Kit.

## Permission Principles

- Prefer read-only access.
- Scope access to the specific repository.
- Avoid organization-wide permissions unless required and approved.
- Store tokens outside the repository.

## Suggested Capabilities

For this kit, MCP access may be useful for:

- reading files;
- reading issues;
- reading pull requests;
- reading releases;
- supporting delivery digest generation.

Write capabilities are not required for the default workflow.

## Local Environment

Set secrets outside committed files:

```bash
export GITHUB_TOKEN=your_token_here
```

Do not place this value in `.env` if the environment does not approve local secret files.

## Verification

Run the local dry-run first:

```bash
python scripts/github_client.py --config client-config.example.yaml --dry-run
```

Then test live access only after permissions are approved.
