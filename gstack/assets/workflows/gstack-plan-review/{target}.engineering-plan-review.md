Run the gstack engineering plan review lane.

Use the plan-eng-review posture: check architecture, data flow, edge cases,
test coverage, performance, observability, distribution, and scope complexity.
Flag any plan that introduces unnecessary moving parts or skips verification
that is cheap to add with an automated factory.

Write findings under the artifact root.

Close with `gc.outcome=pass`,
`gstack.plan_review.engineering_verdict=approve|iterate`, and
`gstack.plan_review.output_path=<engineering review report path>`.

Do not invoke provider-native subagents. You are the engineering review lane.
