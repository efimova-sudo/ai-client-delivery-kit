# Claude Code Project Instructions

## Operating Principles

- Read `README.md`, `client-config.example.yaml`, and relevant files under `docs/` before making broad changes.
- Preserve the dry-run-first posture for scripts and workflows.
- Do not commit or invent secrets, real customer names, private emails, API keys, access tokens, or proprietary data.
- Prefer small, reviewable changes that keep the kit useful for AI Solutions Engineer and AI Automation Specialist portfolio review.
- Keep implementation practical and compact. Avoid turning this into a large framework.

## Prompt Library Rules

Prompt files live under `prompts/<category>/` and use Markdown with YAML frontmatter.

Required prompt metadata:

- `id`
- `version`
- `owner`
- `status`
- `category`
- `inputs`
- `outputs`

Allowed statuses:

- `draft`
- `stable`
- `deprecated`

When editing prompts:

- update the prompt version if the expected behavior changes;
- keep inputs and outputs explicit;
- include quality checks and safety constraints;
- run `python scripts/validate_prompt_library.py`.

## Python and Automation Rules

- Use `client-config.example.yaml` for sample behavior.
- Use `client-config.yaml` only as a local, ignored file.
- Read secrets from environment variables, never from committed files.
- Scripts must support dry-run behavior where practical.
- Tests must not require live network access.

## Validation Commands

```bash
python scripts/validate_prompt_library.py
pytest
```

## Documentation Style

- Write handoff-ready docs for a client delivery team.
- Be explicit about assumptions, permissions, dry-run behavior, and setup steps.
- Keep security notes actionable rather than generic.
