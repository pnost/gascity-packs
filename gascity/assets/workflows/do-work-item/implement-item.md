
Run inside an existing shared worktree lifecycle. Resolve reserved `convoy_id`,
read `gc.drain_member_id` and `gc.drain_item_index`, validate ownership and
verification policy, validate context path {{context_path}} when set, implement
the item, write an item summary, and close only the source anchor on success.

Write or update the item summary with these starter factory evidence fields:

- intended behavior
- first verification command
- changed files
- proof command
- remaining risks

Write the summary as a `gc.build.implementation-summary.v1` artifact and record
its absolute path on the workflow root bead as `gc.implementation.summary_path`
before closing.

Artifact validation: this step is gated by `.gc/scripts/checks/build-artifact-valid.sh`, which validates the summary recorded at `gc.implementation.summary_path` (fallbacks `gc.build.implementation_summary_path`, then `gc.var.summary_path`) against schema `gc.build.implementation-summary.v1`. On repair attempts (`gc.attempt` greater than 1), read the validator errors from `gc.attempt_log` on the validation loop control bead (the dependent of this step bead) and repair the summary in place instead of rewriting it. Two bounded repair attempts follow the first failure; exhausting them closes this stage with `gc.outcome=fail` and machine-readable validation errors that block downstream stages. Never ask questions in headless mode; record unresolved ambiguity inside the summary.
