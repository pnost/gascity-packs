Use the built-in Gas City `create-beads` decomposition flow.

Create task beads or a decomposition artifact from the approved requirements
and implementation plan. Preserve traceability from each work item back to the
relevant acceptance criteria and plan section, and record the implementation convoy
that the `implement` formula will drain.

Create a new implementation convoy for the work units. Do not reuse the source
or launch convoy from `gc.var.convoy_id`.

Record the decomposition output on the workflow root bead, then set both
`gc.input_convoy_id=<implementation-convoy-id>` and
`gc.build.implementation_convoy_id=<implementation-convoy-id>` on the workflow
root bead with a quoted command like:

`bd update "<workflow-root-id>" --set-metadata "gc.input_convoy_id=<implementation-convoy-id>" --set-metadata "gc.build.implementation_convoy_id=<implementation-convoy-id>"`

before closing, verify both metadata fields exist on the workflow root and point
to the new implementation convoy.

Artifact validation: this stage is gated by `.gc/scripts/checks/build-artifact-valid.sh`, which validates the artifact recorded at `gc.build.decomposition_path` (fallback `gc.var.decomposition_path`) against schema `gc.build.decomposition.v1`. On repair attempts (`gc.attempt` greater than 1), read the validator errors from `gc.attempt_log` on the validation loop control bead (the dependent of this step bead) and repair the artifact in place instead of rewriting it. Two bounded repair attempts follow the first failure; exhausting them closes this stage with `gc.outcome=fail` and machine-readable validation errors that block downstream stages. Never ask questions in headless mode; record unresolved ambiguity inside the artifact.
