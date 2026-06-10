Write a gstack report-only review for `{{subject_path}}` and save it to
`{{report_path}}`.

Use the gstack review posture: staff-engineer correctness, QA evidence,
security concerns, and completeness gaps. Because this entry point is
report-only, do not apply fixes unless the parent workflow explicitly routes a
fix lane.

Do not invoke provider-native subagents. Gas City fanouts own review
delegation.
