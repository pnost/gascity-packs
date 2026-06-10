Run the Superpowers per-task fanout review.

The TDD implementation pass is complete for this task. This stage records that
Gas City has created the per-task review fanout that replaces raw
`subagent-driven-development` reviewer dispatch:

- spec compliance review
- implementation fixes for spec gaps
- code quality review
- implementation fixes for quality gaps

Do not invoke provider-native subagents or upstream plugin runtime commands.
The expanded Gas City graph is the delegation mechanism.

