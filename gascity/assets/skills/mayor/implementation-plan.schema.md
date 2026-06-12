# Implementation Plan Schema

Schema: `gc.mayor.implementation-plan.v1`

This schema describes the artifact that design iteration must produce. The
output artifact is `implementation-plan.md` in a Mayor plan directory:

```text
<rig-root>/plans/<plan-slug>/implementation-plan.md
```

It is not a module-local reference document, review transcript, requirements
ledger, or task list.

## Required Front Matter

`implementation-plan.md` must start with YAML front matter:

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

Rules:

- `phase` must be `implementation-plan`.
- `requirements_file` must point at the approved `requirements.md`.
- `status` is `draft`, `questions`, `approved`, or `blocked`.
- Do not use `design_file` in this artifact family.

## Required Body

Use exactly these top-level sections, in this order:

```markdown
# Implementation Plan: <title>

## Summary

## Current System

## Proposed Implementation

## Data And State

## Testing

## Rollout And Recovery

## Open Questions
```

## Section Contract

`Summary` states the implementation outcome in 2-5 sentences.

`Current System` names the current files, modules, commands, tests, data, and
caller paths that constrain the work. It should be source-grounded, not a
general architecture essay.

`Proposed Implementation` describes the concrete code changes, ownership
boundaries, sequencing, and APIs or helpers to add or change. It must be
specific enough for a later `tasks.md` decomposition.

`Data And State` names durable metadata, stores, artifacts, schemas, migrations,
compatibility risks, and rollback/scrub requirements. Use `<none>` when the work
does not touch durable state.

`Testing` names focused tests and commands that prove the change. Prefer exact
packages, files, scenario rows, and command lines.

`Rollout And Recovery` explains how the change can land, how failures are
noticed, and how to revert or repair persisted state when relevant. Use
`<none>` only for genuinely low-risk docs-only or test-only work.

`Open Questions` lists only decisions that materially block decomposition. Use
`None` when the plan is ready to decompose.

## Design Iteration Rules

Design iteration may edit `implementation-plan.md` only to improve this schema's
artifact.

It must not:

- append review-attempt summaries to `implementation-plan.md`
- add `Attempt N Review Response` sections
- turn the artifact into a requirements ledger
- turn the artifact into a module-local `DESIGN.md`
- create `tasks.md` content inside the implementation plan
- approve the plan when material questions remain open

Review reports, attempt notes, diffs, and apply summaries belong in the workflow
artifact directory, not in `implementation-plan.md`.

If the current artifact is the wrong path or wrong schema, stop with
`blocked:wrong-artifact` rather than iterating the document.

If blockers require code, tests, inventory files, proof commands, or other
external prerequisites before the plan can pass, stop with
`blocked:prerequisite` rather than appending more prose.

## Decomposition Readiness

The implementation plan is ready for `tasks.md` decomposition when:

- front matter matches this schema
- required sections are present
- current-system claims cite concrete files, modules, commands, or tests
- proposed implementation names enough files and boundaries to create beads
- testing names exact proof commands or explicitly says what proof is missing
- rollout/recovery handles durable state or states `<none>` with a reason
- open questions are `None`

The plan is not ready when it requires readers to infer the actual code changes
from broad architecture principles.
