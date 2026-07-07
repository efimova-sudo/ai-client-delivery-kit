# Restricted Environment Options

Some client environments do not allow live connectors, broad network access, or local secrets. This kit is designed to keep working in those conditions.

## No Network Access

Use:

```bash
python scripts/github_client.py --config client-config.example.yaml --dry-run
python scripts/validate_prompt_library.py
pytest
```

Dry-run mode avoids live GitHub calls.

## No GitHub Token

If `GITHUB_TOKEN` is not set, the GitHub digest script falls back to dry-run sample data.

For client deployment, request only the read scopes needed for the digest workflow.

## No Connectors Approved

Use the repository directly:

- copy prompt text into the approved AI tool;
- use local docs for setup and handoff;
- run Python validation locally or in approved CI.

## No Client Data Allowed

Keep all examples generic:

- use `Example B2B SaaS Client`;
- remove account-specific details;
- mark unknown values explicitly;
- validate prompts and docs before sharing.

## Manual Handoff Mode

If automation is not approved, the delivery owner can still use:

- `client-config.example.yaml` as a checklist;
- prompts as controlled templates;
- `docs/handoff.md` as a delivery process;
- `docs/security.md` as a review guide.
