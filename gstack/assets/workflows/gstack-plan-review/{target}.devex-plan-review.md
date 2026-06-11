Run the gstack developer-experience plan review lane.

Use the plan-devex-review posture when the work affects APIs, CLIs, SDKs,
docs, onboarding, install paths, or operational workflows. Check time to first
happy path, error messages, docs coverage, upgrade path, and the user's magical
moment. For product-only work, mark the lane not applicable.

Write findings under the artifact root.

Close with `gc.outcome=pass`,
`gstack.plan_review.devex_verdict=approve|iterate`, and
`gstack.plan_review.output_path=<devex review report path>`.

Do not invoke provider-native subagents. You are the developer-experience lane.
