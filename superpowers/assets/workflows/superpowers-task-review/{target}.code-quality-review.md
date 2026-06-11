Review the Superpowers task for code quality.

Use the installed `subagent-driven-development/code-quality-reviewer-prompt.md`
guidance as source material, but execute it as this Gas City fanout lane. Review
maintainability, test quality, simplicity, integration risk, and whether the
task result is clean enough to move to the next implementation bead.

If the spec compliance report still requires changes, do not perform a full
quality review. Write a deferred quality report that points to the unresolved
spec findings and close with `code_review.quality_verdict=iterate`. Otherwise,
read `gc.superpowers.task_review_context_path` and the spec-fix summary, then
write a code quality report under the task artifact directory.

Close with `gc.outcome=pass`,
`code_review.quality_verdict=approve|iterate`,
`code_review.quality_report_path=<code quality report path>`, and
`code_review.output_path=<code quality report path>`.

Do not set `code_review.verdict` or `code_review.report_path`; the
apply-code-quality lane owns those approval-check fields.

Do not invoke provider-native subagents. You are the Gas City fanout lane for
code quality.

