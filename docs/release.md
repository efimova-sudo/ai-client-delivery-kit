# Release

This project uses semantic versioning for repository releases.

Prompt versions are tracked separately in prompt YAML frontmatter. A repository release may include one or more prompt version changes.

## Release Checklist

Before creating a release:

1. Confirm prompt validation passes.
2. Confirm tests pass.
3. Confirm the pull request has passed required CI.
4. Review `docs/security.md`.
5. Update `CHANGELOG.md`.
6. Confirm sample data only.
7. Confirm no secrets or local config files are staged.
8. Merge through a pull request.
9. Create a git tag using the repository version from `main`.

## Branch Protection

Protect `main` before merging live-integration work:

1. Open repository settings in GitHub.
2. Add a branch protection rule for `main`.
3. Require a pull request before merging.
4. Require status checks to pass before merging.
5. Select the `Validate` workflow check after it has run at least once.
6. Block force pushes and branch deletion.

If the GitHub UI exposes rulesets instead of classic branch protection, create an equivalent ruleset for `main` with required pull requests and required `Validate` status checks.

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
