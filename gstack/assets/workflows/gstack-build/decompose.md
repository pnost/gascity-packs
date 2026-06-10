Create the gstack implementation convoy.

Read the approved plan and decompose it into implementation beads under the
workflow root bead. Each bead must map to one vertical slice and include
acceptance criteria, files or modules likely affected, first verification
command, and expected proof command.

Record `gc.input_convoy_id` on the current step, create the implementation
convoy, and link source-anchor beads back to the workflow root bead. Before
closing, ensure the implementation convoy is discoverable from the workflow
root bead.

Do not copy review-lane procedure into implementation beads. The convoy should
describe product work; `gstack-work` carries the execution process.

Close with `gc.outcome=pass`.

Do not invoke provider-native subagents. Gas City graph lanes own fanout.
