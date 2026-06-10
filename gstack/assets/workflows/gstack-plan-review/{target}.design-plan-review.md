Run the gstack design plan review lane.

Use the plan-design-review posture: rate design completeness, identify what a
10 looks like, check reuse of existing design patterns, and call out missing
states, responsive behavior, accessibility, or visual evidence. For non-UI
work, explicitly mark this lane as not applicable and explain why.

Write findings under the artifact root.

Close with `gc.outcome=pass`,
`gstack.plan_review.design_verdict=approve|iterate`, and
`gstack.plan_review.output_path=<design review report path>`.

Do not invoke provider-native subagents. You are the design review lane.
