# Attractor Pack

`attractor` compiles a strict static Attractor-style DOT graph into a Gas City
`graph.v2` formula and can install or run that formula through backend workers
with `gc sling`.

This pack is opt-in. It does not add orchestration behavior to Gas City core,
and it does not execute shell commands in the controller. Tool nodes become
worker instructions.

## Commands

```bash
gc attractor validate <dot-file>
gc attractor compile <dot-file> [--formula <name>] [--output <path>]
gc attractor install <dot-file> [--formula <name>] [--force]
gc attractor run <target> <dot-file> [--formula <name>] [--force-install] [--force-sling] [--var key=value ...]
```

`install` writes the generated formula to:

```text
$GC_CITY_PATH/formulas/<formula>.toml
```

It refuses to overwrite either `<formula>.toml` or the older
`<formula>.formula.toml` path unless `--force` is supplied. `install` and `run`
require `[daemon] formula_v2 = true` in the resolved city config.

## DOT Subset

The compiler accepts one directed `digraph`. It supports graph, node, and edge
attributes; directed edge chains; comments; quoted strings; simple unquoted
identifiers; optional semicolons; and grouping/default subgraphs.

Node IDs must match:

```text
[A-Za-z_][A-Za-z0-9_]*
```

Executable nodes:

- Agent: `shape=box`, `type=agent`, or `type=codergen`
- Tool instruction: `shape=parallelogram` or `type=tool`

Structural nodes compile away:

- Start: `shape=Mdiamond` or `type=start`
- Exit: `shape=Msquare` or `type=exit`
- Parallel split: `shape=component` or `type=parallel`
- Parallel fan-in: `shape=tripleoctagon` or `type=parallel.fan_in`

The compiler rejects dynamic branching, loops, runtime conditions, model
selection hints, timeouts, human gates, ports, HTML labels, undirected graphs,
multiple graphs, unreachable executable nodes, and dependency cycles.

## Variables

Lowercase `$var`, `${var}`, and `{{var}}` references compile to formula
variables. Unknown variables become required `[vars.<name>]` entries.

Graph `goal` handling is special:

- `goal="Ship the change"` creates `[vars.goal]` with a default.
- `goal="$task"` aliases `goal` to `task`; `$goal` and `$task` both compile to
  `{{task}}`.
- `goal="Ship $task"` requires runtime `goal` and emits a warning because the
  graph mixes a literal with a variable.

## Example

```bash
gc attractor validate attractor/examples/simple.dot
gc attractor compile attractor/examples/simple.dot
gc attractor run worker attractor/examples/simple.dot --var task="ship docs"
```

See `docs/compiler-semantics.md` for the exact generated formula contract.
