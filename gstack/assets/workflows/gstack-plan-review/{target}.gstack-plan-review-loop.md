Run the gstack plan-review loop.

This loop has four review lanes plus synthesis and plan-fix application:
founder scope, design, engineering, and developer experience. It maps upstream
gstack autoplan review behavior into Gas City fanout/fanin.

The apply-plan-review-findings lane owns
`design_review.verdict=done|iterate`. The loop repeats until the plan is
approved.

Do not invoke provider-native subagents. Continue only through this Gas City
graph loop.
