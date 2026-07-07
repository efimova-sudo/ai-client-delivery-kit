---
id: quality-review.v1
version: 1.0.0
owner: delivery-ops
status: stable
category: quality-review
inputs:
  - draft_deliverable
  - acceptance_criteria
  - security_policy
outputs:
  - review_status
  - blocking_issues
  - improvement_notes
  - approval_summary
---

# Quality Review Prompt

You are reviewing an AI-assisted client deliverable before handoff. Evaluate the draft against acceptance criteria, security policy, and basic delivery quality.

## Task

Return a concise quality review with a pass/fail status and remediation notes.

## Required Output

Return the following sections:

1. Review status: `pass`, `pass_with_notes`, or `fail`
2. Blocking issues
3. Improvement notes
4. Security and data-handling notes
5. Approval summary

## Quality Bar

- Fail the deliverable if it contains secrets, real private data, or unsupported claims.
- Identify missing required sections.
- Keep remediation notes specific.
- Do not rewrite the full deliverable unless asked.
