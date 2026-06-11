Synthesize the gstack plan review.

Read the founder, design, engineering, and developer-experience reports.
Deduplicate findings, preserve lane attribution, and classify each item as
required fix, optional expansion, deferred follow-up, or residual risk.

Write one synthesis under the artifact root with the final recommendation and
the exact plan edits needed before implementation.

Close with `gc.outcome=pass`,
`gstack.plan_review.synthesis_path=<plan review synthesis path>`, and
`gstack.plan_review.output_path=<plan review synthesis path>`.

Do not invoke provider-native subagents. Synthesis happens in this Gas City
fan-in lane.
