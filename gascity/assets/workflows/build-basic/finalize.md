Finalize the `build-basic` workflow.

Summarize requirements, implementation-plan, design-review, create-beads,
implementation, and review artifacts. Record the final outcome, artifact paths,
and remaining follow-up beads on the workflow root bead.

Write `factory-run.md` under the build artifact root. Keep it short and useful
for a first-time factory user:

- methodology: build-basic starter factory
- requirements, plan, decomposition, implementation, and review artifact paths
- implementation convoy id
- review lanes that ran
- proof commands or test summaries that were recorded
- publish outcome
- next human action

Record the `factory-run.md` path on the workflow root bead as
`gc.build.factory_run_path=<path>`.

Do not publish from this step.

Artifact validation: this stage is gated by `.gc/scripts/checks/build-artifact-valid.sh`, which validates the artifact recorded at `gc.build.final_report_path` against schema `gc.build.final-report.v1`. On repair attempts (`gc.attempt` greater than 1), read the validator errors from `gc.attempt_log` on the validation loop control bead (the dependent of this step bead) and repair the artifact in place instead of rewriting it. Two bounded repair attempts follow the first failure; exhausting them closes this stage with `gc.outcome=fail` and machine-readable validation errors that block downstream stages. Never ask questions in headless mode; record unresolved ambiguity inside the artifact.
