Apply gstack plan-review findings.

Read the synthesis and update the plan artifact in place when required fixes
remain. Keep optional ambition clearly separated from accepted scope. In
interactive mode, only add new scope after explicit approval is recorded; in
autonomous mode, preserve optional scope as deferred follow-up.

Set `design_review.verdict=done` only when founder, design, engineering, and
developer-experience lanes approve. Set `design_review.verdict=iterate` when
required plan fixes remain.

Close with `gc.outcome=pass`,
`design_review.verdict=done|iterate`,
`design_review.report_path=<plan review summary path>`, and
`gstack.plan_review.output_path=<plan review summary path>`.

Do not invoke provider-native subagents. This Gas City graph lane is the plan
fix delegation mechanism.
