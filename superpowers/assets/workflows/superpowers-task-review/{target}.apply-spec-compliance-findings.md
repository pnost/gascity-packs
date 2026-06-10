Apply Superpowers spec-compliance findings.

Use implementation target {{implementation_target}} for code changes. Read the
spec compliance report from `code_review.spec_report_path`. If it approves,
write a no-op apply summary. If it requires changes, make the smallest code or
test updates needed to satisfy the approved task scope and rerun focused
verification.

Write the spec-fix summary under the task artifact directory with resolved
finding ids, changed files, tests run, and any blocker. Close with
`gc.outcome=pass` and `code_review.spec_apply_path=<spec-fix summary path>`.

Do not set `code_review.verdict` or `code_review.report_path`; code quality
still has to run after this lane.

Do not invoke provider-native subagents. This Gas City fanout lane is the
delegation mechanism.

