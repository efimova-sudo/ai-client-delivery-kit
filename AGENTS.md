# Agent Roles

This file describes role boundaries for AI-assisted delivery. These are operating patterns, not claims of fully autonomous production agents.

## Account Research Agent

Purpose:

- synthesize account context from approved inputs;
- identify business priorities, risks, open questions, and likely stakeholders;
- produce structured account research notes.

Primary prompt:

- `prompts/account-research/account-research.md`

Review expectations:

- cite only provided or approved sources;
- separate facts from assumptions;
- flag missing context.

## Executive Brief Agent

Purpose:

- convert account research into a concise executive-ready brief;
- focus on business relevance, risks, and recommended next steps;
- adapt tone for senior stakeholders.

Primary prompt:

- `prompts/executive-brief/executive-brief.md`

Review expectations:

- avoid unsupported claims;
- keep recommendations tied to evidence;
- make next steps concrete.

## Quality Review Agent

Purpose:

- review deliverables before handoff;
- check structure, assumptions, completeness, and safety;
- return pass/fail status with remediation notes.

Primary prompt:

- `prompts/quality-review/quality-review.md`

Review expectations:

- enforce metadata and deliverable criteria;
- flag secrets, PII, and unsupported claims;
- produce concise issue lists.

## Delivery Manager Agent

Purpose:

- coordinate workflow stages;
- confirm that validation and handoff docs are complete;
- ensure that client-specific changes are tracked.

Review expectations:

- check acceptance criteria in `client-config.example.yaml`;
- confirm that dry-run workflows work before live use.

## Security Reviewer Agent

Purpose:

- review data handling, permissions, and secret management;
- ensure the kit is safe for public portfolio use and client adaptation.

Review expectations:

- no committed secrets;
- sample data only;
- clear token scope guidance;
- restricted-environment fallback paths documented.
