# Handoff

Use this checklist before handing the kit to a client team or internal delivery owner.

## Delivery Package

Include:

- `README.md`
- `CLAUDE.md`
- `AGENTS.md`
- `client-config.example.yaml`
- `prompts/`
- `platform-config/`
- `scripts/`
- `docs/`
- `.github/workflows/`

Do not include:

- `.env` files
- `client-config.yaml`
- generated `outputs/`
- real customer data
- private credentials

## Client Customization

Before live use:

1. Copy `client-config.example.yaml` to `client-config.yaml`.
2. Replace sample values with approved client-specific values.
3. Confirm GitHub owner and repo settings.
4. Review the prompt library with the delivery owner.
5. Confirm security and data-handling requirements.
6. Run prompt validation and tests.

## Acceptance Criteria

The handoff is ready when:

- prompt library validation passes;
- tests pass without network access;
- digest generation works in dry-run mode;
- setup docs are reviewed;
- security docs are reviewed;
- required secrets are stored outside the repository;
- platform setup guides match the client's approved tools.

## Ownership

Recommended ownership split:

- AI Solutions Engineer: workflow design, prompt quality, client setup, handoff.
- AI Automation Specialist: scripts, GitHub Actions, API behavior, scheduled reporting.
- Security Reviewer: token scopes, data policy, restricted-environment review.
