Review the Superpowers task for spec compliance.

Use the installed `subagent-driven-development/spec-reviewer-prompt.md`
guidance as source material, but execute it as this Gas City fanout lane. Check
only whether the implementation satisfies the approved requirements, plan task,
and decomposition bead without unapproved scope creep.

Read `gc.superpowers.task_review_context_path`. Write a spec compliance report
under the task artifact directory. Required findings must cite the requirement,
plan task, task bead, file, or test evidence that proves the mismatch.

Close with `gc.outcome=pass`,
`code_review.spec_verdict=approve|iterate`,
`code_review.spec_report_path=<spec compliance report path>`, and
`code_review.output_path=<spec compliance report path>`.

Do not set `code_review.verdict` or `code_review.report_path`; the
apply-code-quality lane owns those approval-check fields.

Do not invoke provider-native subagents. You are the Gas City fanout lane for
spec compliance.

