Finalize the gstack code review.

Verify the latest review loop approved the implementation: confirm
`code_review.verdict=done` on the apply-review-findings lane, the synthesized
review report at workflow root `gc.build.code_review_report_path`, and the
review-fix summary at `gc.build.review_fix_summary_path`. Record
`gc.build.code_review_status=approved` and
`gc.build.code_review_approved_at=<UTC timestamp>` on the workflow root for QA
and the final sprint report.

Close with `gc.outcome=pass`.

Do not invoke provider-native subagents or provider-specific task tools.
