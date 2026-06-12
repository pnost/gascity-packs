# Requirements Schema

Schema: `gc.mayor.requirements.v1`

This schema describes the artifact that requirements iteration must produce.
The output artifact is `requirements.md` in a Mayor plan directory:

```text
<rig-root>/plans/<plan-slug>/requirements.md
```

It is not an implementation plan, module-local requirements ledger, task list,
or bead-creation payload.

## Required Front Matter

`requirements.md` must start with YAML front matter:

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

Rules:

- `phase` must be `requirements`.
- `status` is `draft`, `questions`, `approved`, or `blocked`.
- Do not use `requirements_file`, `implementation_plan_file`, or
  `design_file`; those belong to downstream artifacts.
- Do not include bead IDs, formula targets, implementation file assignments, or
  workflow launch metadata in requirements.

## Required Body

Use exactly these top-level sections, in this order:

```markdown
# Requirements: <title>

## Problem Statement

## W6H

## Example Mapping

## Acceptance Criteria

## Out Of Scope

## Open Questions
```

## Section Contract

`Problem Statement` describes the user-visible problem, why it matters, and the
desired outcome in product language.

`W6H` answers who, what, when, where, why, how, and how-much/scale. Unknowns
that materially affect the work must become `Open Questions`.

`Example Mapping` includes concrete scenarios:

- at least one happy path
- at least one negative path
- at least one edge case

Each example should name a concrete input, expected behavior, and repository,
issue, command, or test evidence when available.

`Acceptance Criteria` lists testable product outcomes. Each criterion must be
verifiable by a unit test, integration test, command verification, or explicit
manual check.

`Out Of Scope` names tempting adjacent work that this plan must not include.

`Open Questions` lists only product decisions that materially block
implementation planning. Use `None` when the requirements are ready for an
implementation plan.

## Requirements Iteration Rules

Requirements iteration may edit `requirements.md` only to improve this schema's
artifact.

It must not:

- choose implementation files, helper names, formula targets, or bead IDs
- create `implementation-plan.md` content inside requirements
- create `tasks.md` or bead YAML inside requirements
- append review-attempt summaries to `requirements.md`
- approve requirements when material product questions remain open

Research notes, interview transcripts, review reports, diffs, and apply
summaries belong in workflow artifacts, not in `requirements.md`.

If the current artifact is the wrong path or wrong schema, stop with
`blocked:wrong-artifact` rather than iterating the document.

If requirements cannot be completed without a product decision, set
`status: questions` and put the decision in `Open Questions`.

If blockers require unavailable external evidence before requirements can be
made truthful, stop with `blocked:prerequisite` rather than inventing a product
rule.

## Implementation-Plan Readiness

The requirements are ready for `implementation-plan.md` when:

- front matter matches this schema
- required sections are present
- W6H covers every material product dimension
- Example Mapping includes happy, negative, and edge scenarios
- Acceptance Criteria are testable and behavior-focused
- Out Of Scope names the most likely scope creep
- Open Questions are `None`

The requirements are not ready when the next agent would need to infer product
behavior from implementation guesses.
