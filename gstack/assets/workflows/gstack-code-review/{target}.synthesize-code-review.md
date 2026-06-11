Synthesize the gstack code review.

Read the staff, QA evidence, security, and gap-analysis reports. Deduplicate
findings and produce one ordered list of required fixes, missing evidence, and
residual risks. Preserve the source lane for each finding.

Write a synthesis under the artifact root.

Close with `gc.outcome=pass`,
`code_review.synthesis_path=<code review synthesis path>`, and
`code_review.output_path=<code review synthesis path>`.

Do not invoke provider-native subagents. Synthesis happens in this Gas City
fan-in lane.
