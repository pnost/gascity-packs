# Mayor Plan Asset

This asset defines the default Mayor product requirements contract. Packs that
import this one may shadow this same relative path:
`assets/skills/mayor/plan.md`.

Use this asset when the user is still defining what should change. Write or
revise `requirements.md`; do not make engineering design decisions here.
When the artifact already exists and needs to be normalized or reviewed, run
the `design-review` formula with
`output_schema=assets/skills/mayor/requirements.schema.md`.

`requirements.md` starts with:

```yaml
---
plan_slug: example-slug
phase: requirements
rig: backend
rig_root: /absolute/path/to/rig
artifact_root: /absolute/path/to/rig/plans
status: draft
created_at: 2026-05-10T00:00:00Z
updated_at: 2026-05-10T00:00:00Z
---
```

Use this body:

```markdown
# Requirements: <title>

## Problem Statement

## Solution

## User Stories

## Out Of Scope

## Other Notes
```

Each user story should include lightweight acceptance criteria, usually 2-5
bullets. Capture constraints discovered from the repo. Do not preselect bead
IDs or formula targets in requirements.

For stricter normalization and review, use
`assets/skills/mayor/requirements.schema.md` as the output schema.
