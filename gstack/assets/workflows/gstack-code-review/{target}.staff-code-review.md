Run the gstack staff-engineer code review lane.

Use the upstream review posture: find bugs that pass CI, scope drift, wrong
assumptions, brittle abstractions, missing tests, and production risks. Lead
with concrete file or artifact references and classify severity.

Write findings under the artifact root.

Close with `gc.outcome=pass`,
`code_review.staff_verdict=approve|iterate`, and
`code_review.output_path=<staff review report path>`.

Do not invoke provider-native subagents. You are the staff review lane.
