Run the Superpowers per-task review loop.

The child lanes are Gas City fanout lane work items that replace the raw
`subagent-driven-development` reviewer handoffs. The spec compliance lane runs
first. The code quality lane waits for the spec-compliance fix lane so code
quality never starts before the spec review has been addressed.

The apply-code-quality lane is the only child that sets
`code_review.verdict=done|iterate` and `code_review.report_path=<task review
summary path>`. The implementation review check repeats this loop until the
latest task review verdict is `done`.

Do not invoke provider-native subagents. Re-run or continue only through this
Gas City graph loop.

