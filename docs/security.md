# Security

This repository is designed for safe public portfolio use and client adaptation.

## Data Policy

- Use sample data only in committed files.
- Do not commit real customer names, private emails, contract details, API responses, or proprietary materials.
- Treat `client-config.example.yaml` as a template, not a live client config.
- Keep `client-config.yaml` local and ignored by git.

## Secrets

Never commit:

- API keys
- GitHub tokens
- OAuth credentials
- webhook secrets
- client-specific environment files

Use environment variables or an approved secret manager. The GitHub digest script reads `GITHUB_TOKEN` from the environment.

## GitHub Token Scope Guidance

For read-only digest generation, prefer the minimum scopes needed for the target repository:

- repository metadata read access;
- issues read access;
- pull requests read access;
- releases read access.

Avoid write scopes unless a workflow explicitly needs them and has been reviewed.

## Prompt and Output Safety

Prompts should:

- use approved inputs only;
- mark missing data as unknown;
- separate facts from assumptions;
- avoid unsupported claims;
- flag secrets or PII during quality review.

Generated outputs should be reviewed before external sharing.

## Review Checklist

- No secrets in committed files.
- No real customer data in samples.
- Dry-run works without live credentials.
- GitHub Actions use least-privilege permissions.
- Handoff docs explain local config and credential handling.
