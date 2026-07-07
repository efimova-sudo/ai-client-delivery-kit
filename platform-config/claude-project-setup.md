# Claude Project Setup

Use this guide to configure a Claude Project for the AI Client Delivery Kit.

## Recommended Setup

1. Create a Claude Project for the delivery engagement.
2. Add approved client context only.
3. Add or reference the repository-level `CLAUDE.md` instructions.
4. Upload or reference relevant prompt files from `prompts/`.
5. Keep client-specific secrets and credentials out of project knowledge.

## Project Instructions

The Claude Project instructions should reinforce:

- sample data only unless approved context is provided;
- dry-run-first automation;
- no invented customer details;
- facts separated from assumptions;
- security review before handoff.

## Claude Code Usage

Claude Code should read `CLAUDE.md` as project-level instructions and follow the validation workflow:

```bash
python scripts/validate_prompt_library.py
pytest
```

## Handoff Notes

Before handing the project to a client team, confirm which files are approved for upload into Claude Project knowledge and which must remain local.
