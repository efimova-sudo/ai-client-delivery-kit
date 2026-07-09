# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning for repository releases. Individual prompts use their own prompt-level versions in YAML frontmatter.

## [0.2.0] - 2026-07-09

### Added

- Explicit live GitHub digest generation through `--live`.
- Resilient GitHub API client handling for rate-limit and temporary API failures.
- Issue and pull request templates for reviewable GitHub workflow.
- CI badge in the README.
- Branch protection setup guidance for requiring successful validation before merge.

### Changed

- GitHub digest generation now remains in dry-run mode unless live mode is explicitly requested.
- Digest output filters issues, pull requests, and releases to the configured digest window.

### Tests

- Covered live request construction, digest date filtering, rate-limit handling, and missing token behavior.

## [0.1.1] - 2026-07-07

### Added

- Curated sample outputs for weekly digest and executive brief deliverables.

## [0.1.0] - 2026-07-07

### Added

- Initial repository structure for the AI Client Delivery Kit.
- Sample B2B SaaS client configuration with dry-run defaults.
- Versioned prompt library convention with YAML frontmatter.
- Prompt validation script and unit test coverage.
- GitHub digest script with dry-run support.
- GitHub Actions workflows for validation and scheduled digest generation.
- Client-safe setup, handoff, security, data-flow, restricted-environment, and release documentation.
- Portfolio-ready README framing for operating model, automation, safety, and client adaptation.
