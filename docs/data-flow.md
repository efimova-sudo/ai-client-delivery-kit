# Data Flow

The kit is organized around a simple delivery flow:

```text
client-config.example.yaml
        |
        v
prompt library + scripts
        |
        v
validation + GitHub API digest
        |
        v
handoff documentation / client deliverables
```

## Inputs

Primary inputs:

- sample client config;
- approved account or delivery notes;
- prompt library files;
- optional GitHub repository metadata.

Secrets are not inputs to committed files. Live API credentials come from environment variables.

## Processing

The prompt validator checks prompt metadata, folder consistency, versions, and duplicate IDs.

The bootstrap script prepares a local output workspace from config.

The GitHub client can generate a dry-run digest from sample data or a live digest from GitHub API reads.

## Outputs

Typical outputs:

- account research notes;
- executive briefs;
- quality review notes;
- weekly GitHub digest;
- handoff checklist.

Generated outputs should stay in `outputs/`, which is ignored by git.

## Controls

- Dry-run first.
- Sample data only in repository files.
- Tests do not require network access.
- CI validates prompts and tests.
