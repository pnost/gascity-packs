# Mayor Design Asset

This asset defines the default Mayor engineering requirements contract. Packs
that import this one may shadow this same relative path:
`assets/skills/mayor/design.md`.

Use this asset after product requirements are approved, or when the user
explicitly asks to skip that gate. Inspect the codebase before writing. Ground
the engineering requirements in current files, modules, APIs, commands, tests,
config, and constraints.

The engineering requirements artifact is `implementation-plan.md`.
When the artifact already exists and needs to be normalized or reviewed, run
the `design-review` formula with
`output_schema=assets/skills/mayor/implementation-plan.schema.md`.

`implementation-plan.md` starts with:

```yaml
---
plan_slug: example-slug
phase: implementation-plan
rig: backend
rig_root: /absolute/path/to/rig
artifact_root: /absolute/path/to/rig/plans
requirements_file: /absolute/path/to/requirements.md
status: draft
created_at: 2026-05-10T00:00:00Z
updated_at: 2026-05-10T00:00:00Z
---
```

Use this body:

```markdown
# Implementation Plan: <title>

## Summary

## Current System

## Proposed Implementation

## Testing

## Rollout

## Open Questions
```

The engineering requirements should be concrete enough for bead creation: name
files/modules, interfaces, data flow, persistence, error handling, migration
concerns, and verification strategy where relevant. When work should be
implemented as a group, describe the grouping as a convoy boundary.

For stricter normalization and review, use
`assets/skills/mayor/implementation-plan.schema.md` as the output schema.
