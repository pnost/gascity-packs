Decompose the approved gstack plan at `{{plan_path}}` into implementation work
and write the decomposition artifact to `{{decomposition_path}}` when supplied.

Create one implementation convoy and record `gc.input_convoy_id` so downstream
Gas City drains can find the workflow root bead and implementation convoy
before closing.

Do not invoke provider-native subagents.
