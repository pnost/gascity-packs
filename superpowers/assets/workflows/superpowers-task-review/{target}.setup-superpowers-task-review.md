Prepare the Superpowers per-task review fanout.

Resolve the implementation task context, task summary, changed files, test
evidence, approved requirements, approved plan, and decomposition artifact.
Write a compact review context file under the task artifact directory and store
its path on the workflow root as `gc.superpowers.task_review_context_path`.

This setup lane converts the raw Superpowers fresh-reviewer handoff into Gas
City fanout lanes. Do not invoke provider-native subagents or upstream plugin
runtime commands.

Close this setup bead with `gc.outcome=pass` only after the context file exists.

