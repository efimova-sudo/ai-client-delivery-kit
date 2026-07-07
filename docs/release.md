# Release

This project uses semantic versioning for repository releases.

Prompt versions are tracked separately in prompt YAML frontmatter. A repository release may include one or more prompt version changes.

## Release Checklist

Before creating a release:

1. Confirm prompt validation passes.
2. Confirm tests pass.
3. Review `docs/security.md`.
4. Update `CHANGELOG.md`.
5. Confirm sample data only.
6. Confirm no secrets or local config files are staged.
7. Create a git tag using the repository version.

## Commands

```bash
python scripts/validate_prompt_library.py
pytest
```

Example tag command:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Do not create a release tag until the repository has been reviewed and the changelog entry is final.
