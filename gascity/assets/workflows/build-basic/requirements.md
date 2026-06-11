Use the built-in Gas City guided starter factory requirements flow.

Create the requirements artifact with the same expectations as the
`generate-requirements` stage in the GitHub issue fix workflow: preserve the
input target, normalize the artifact path, and make the acceptance criteria
specific enough for plan review.

Keep the artifact approachable for a first factory run. Include these sections:

- goal
- constraints
- acceptance criteria
- non-goals
- open questions

If `interaction_mode` is interactive or the user is present, ask only the
minimum question needed to unblock the artifact. If the workflow is autonomous
or headless, record unresolved ambiguity in open questions instead of blocking
without a clear need.

Record the requirements path on the workflow root bead before closing.

Artifact validation: this stage is gated by `.gc/scripts/checks/build-artifact-valid.sh`, which validates the artifact recorded at `gc.build.requirements_path` (fallback `gc.var.requirements_path`) against schema `gc.build.requirements.v1`. On repair attempts (`gc.attempt` greater than 1), read the validator errors from `gc.attempt_log` on the validation loop control bead (the dependent of this step bead) and repair the artifact in place instead of rewriting it. Two bounded repair attempts follow the first failure; exhausting them closes this stage with `gc.outcome=fail` and machine-readable validation errors that block downstream stages. Never ask questions in headless mode; record unresolved ambiguity inside the artifact.
