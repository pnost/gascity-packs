from __future__ import annotations

from dataclasses import dataclass, field
import re

from attractor_dot import DotGraph


class ValidationError(Exception):
    pass


@dataclass
class AttractorStep:
    node_id: str
    step_id: str
    title: str
    kind: str
    source_order: int
    node_shape: str = ""
    prompt: str = ""
    command: str = ""
    run_target: str = ""
    max_retries: int | None = None
    needs: list[str] = field(default_factory=list)


@dataclass
class AttractorModel:
    graph: DotGraph
    formula_name: str
    description: str
    goal: str
    default_max_retries: int | None
    steps: list[AttractorStep]
    warnings: list[str] = field(default_factory=list)


NODE_ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

VISUAL_ATTRS = {
    "label",
    "shape",
    "style",
    "class",
    "color",
    "fillcolor",
    "fontname",
    "fontsize",
    "penwidth",
    "margin",
    "width",
}
GRAPH_ATTRS = {"label", "goal", "rankdir", "default_max_retry", "default_max_retries", "gc_formula"}
NODE_ATTRS = VISUAL_ATTRS | {
    "prompt",
    "llm_prompt",
    "type",
    "node_type",
    "command",
    "tool_command",
    "gc_run_target",
    "max_retries",
    "is_codergen",
}
EDGE_ATTRS = VISUAL_ATTRS


def build_model(graph: DotGraph, formula_name: str) -> AttractorModel:
    _validate_attrs(graph)
    _validate_node_ids(graph)

    default_retries = _graph_default_retries(graph)
    classes = {node_id: _classify_node(node_id, attrs) for node_id, attrs in _node_attrs(graph).items()}

    starts = [node_id for node_id, kind in classes.items() if kind == "start"]
    exits = [node_id for node_id, kind in classes.items() if kind == "exit"]
    if len(starts) != 1:
        raise ValidationError(f"expected exactly one start node, found {len(starts)}")
    if not exits:
        raise ValidationError("expected at least one exit node")

    _validate_structural_degrees(graph, classes)
    _validate_reachability(graph, classes, starts[0], exits)

    executable_ids = [node_id for node_id, kind in classes.items() if kind in {"agent", "tool"}]
    step_ids: dict[str, str] = {}
    original_by_step: dict[str, str] = {}
    for node_id in executable_ids:
        step_id = normalize_step_id(node_id)
        if step_id in original_by_step:
            raise ValidationError(
                f'nodes "{original_by_step[step_id]}" and "{node_id}" normalize to the same step id "{step_id}"'
            )
        step_ids[node_id] = step_id
        original_by_step[step_id] = node_id

    deps_by_node = _executable_dependencies(graph, classes, executable_ids)
    _validate_no_cycles(deps_by_node)

    ordered_nodes = _topological_order(executable_ids, deps_by_node, graph)
    steps: list[AttractorStep] = []
    for node_id in ordered_nodes:
        node = graph.nodes[node_id]
        attrs = node.attrs
        kind = classes[node_id]
        title = attrs.get("label") or title_from_id(node_id)
        max_retries = _node_max_retries(node_id, attrs)
        if max_retries is None:
            max_retries = default_retries
        if kind == "agent":
            prompt = attrs.get("prompt") or attrs.get("llm_prompt") or ""
            if not prompt:
                raise ValidationError(f'node {node_id}: executable agent node requires "prompt"')
            command = ""
        else:
            command = attrs.get("tool_command") or attrs.get("command") or ""
            if not command:
                raise ValidationError(f'node {node_id}: tool node requires "tool_command" or "command"')
            prompt = ""
        steps.append(
            AttractorStep(
                node_id=node_id,
                step_id=step_ids[node_id],
                title=title,
                kind=kind,
                source_order=node.order,
                node_shape=attrs.get("shape", ""),
                prompt=prompt,
                command=command,
                run_target=attrs.get("gc_run_target", ""),
                max_retries=max_retries,
                needs=[step_ids[dep] for dep in _topological_sort_deps(deps_by_node[node_id], graph)],
            )
        )

    return AttractorModel(
        graph=graph,
        formula_name=formula_name,
        description=graph.graph_attrs.get("label", f"Attractor workflow {graph.name}"),
        goal=graph.graph_attrs.get("goal", ""),
        default_max_retries=default_retries,
        steps=steps,
    )


def normalize_step_id(node_id: str) -> str:
    parts = node_id.replace("_", "-")
    out: list[str] = []
    for i, ch in enumerate(parts):
        prev = parts[i - 1] if i > 0 else ""
        nxt = parts[i + 1] if i + 1 < len(parts) else ""
        if ch.isupper() and i > 0 and (prev.islower() or prev.isdigit()) and nxt.islower():
            out.append("-")
        out.append(ch.lower())
    normalized = re.sub(r"-+", "-", "".join(out)).strip("-")
    return normalized


def title_from_id(node_id: str) -> str:
    return normalize_step_id(node_id).replace("-", " ").title()


def _validate_attrs(graph: DotGraph) -> None:
    for key in graph.graph_attrs:
        if key not in GRAPH_ATTRS:
            raise ValidationError(f'graph: unsupported attribute "{key}"')
    for node_id, node in graph.nodes.items():
        for key in node.attrs:
            if key not in NODE_ATTRS:
                raise ValidationError(f'node {node_id}: unsupported attribute "{key}"')
        if "is_codergen" in node.attrs and node.attrs["is_codergen"].strip().lower() != "true":
            raise ValidationError(f'node {node_id}: is_codergen must be "true" when present')
        if "timeout" in node.attrs:
            raise ValidationError(f'node {node_id}: unsupported attribute "timeout"')
    for edge in graph.edges:
        for key in edge.attrs:
            if key in {"condition", "loop_restart"}:
                raise ValidationError(f'edge {edge.src} -> {edge.dst}: unsupported attribute "{key}"')
            if key not in EDGE_ATTRS:
                raise ValidationError(f'edge {edge.src} -> {edge.dst}: unsupported attribute "{key}"')


def _validate_node_ids(graph: DotGraph) -> None:
    for node_id in graph.nodes:
        if not NODE_ID_RE.match(node_id):
            raise ValidationError(f'node {node_id!r}: node IDs must match [A-Za-z_][A-Za-z0-9_]*')


def _graph_default_retries(graph: DotGraph) -> int | None:
    raw = graph.graph_attrs.get("default_max_retries", graph.graph_attrs.get("default_max_retry", ""))
    if raw == "":
        return None
    return _parse_non_negative_int("graph default_max_retries", raw)


def _node_max_retries(node_id: str, attrs: dict[str, str]) -> int | None:
    if "max_retries" not in attrs:
        return None
    return _parse_non_negative_int(f"node {node_id} max_retries", attrs["max_retries"])


def _parse_non_negative_int(label: str, raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as err:
        raise ValidationError(f"{label}: must be a non-negative integer") from err
    if value < 0:
        raise ValidationError(f"{label}: must be a non-negative integer")
    return value


def _node_attrs(graph: DotGraph) -> dict[str, dict[str, str]]:
    return {node_id: node.attrs for node_id, node in graph.nodes.items()}


def _classify_node(node_id: str, attrs: dict[str, str]) -> str:
    node_type = (attrs.get("type") or attrs.get("node_type") or "").strip().lower()
    shape = attrs.get("shape", "").strip().lower()
    if node_type == "start" or shape == "mdiamond":
        return "start"
    if node_type == "exit" or shape == "msquare":
        return "exit"
    if node_type == "conditional" or shape == "diamond":
        raise ValidationError(f"node {node_id}: conditional nodes are not supported")
    if node_type == "wait.human" or shape == "hexagon":
        raise ValidationError(f"node {node_id}: human wait nodes are not supported")
    if node_type == "parallel" or shape == "component":
        return "parallel"
    if node_type == "parallel.fan_in" or shape == "tripleoctagon":
        return "parallel_join"
    if node_type == "tool" or shape == "parallelogram":
        return "tool"
    if node_type in {"agent", "codergen"} or (shape == "box" and node_type == ""):
        return "agent"
    if node_type:
        raise ValidationError(f'node {node_id}: unsupported executable type "{node_type}"')
    raise ValidationError(f'node {node_id}: unsupported node shape "{shape or "<empty>"}"')


def _validate_structural_degrees(graph: DotGraph, classes: dict[str, str]) -> None:
    out_counts: dict[str, int] = {node_id: 0 for node_id in graph.nodes}
    in_counts: dict[str, int] = {node_id: 0 for node_id in graph.nodes}
    for edge in graph.edges:
        out_counts[edge.src] += 1
        in_counts[edge.dst] += 1
    for node_id, kind in classes.items():
        if kind == "parallel" and out_counts[node_id] < 2:
            raise ValidationError(f"node {node_id}: parallel component requires at least two outgoing branches")
        if kind == "parallel_join" and in_counts[node_id] < 2:
            raise ValidationError(f"node {node_id}: parallel fan-in requires at least two incoming branches")


def _validate_reachability(graph: DotGraph, classes: dict[str, str], start: str, exits: list[str]) -> None:
    forward = _adjacency(graph)
    reverse = _reverse_adjacency(graph)
    from_start = _walk(forward, [start])
    to_exit = _walk(reverse, exits)
    for node_id, kind in classes.items():
        if kind in {"agent", "tool"}:
            if node_id not in from_start:
                raise ValidationError(f"node {node_id}: executable is not reachable from start")
            if node_id not in to_exit:
                raise ValidationError(f"node {node_id}: executable cannot reach an exit")


def _executable_dependencies(
    graph: DotGraph, classes: dict[str, str], executable_ids: list[str]
) -> dict[str, set[str]]:
    reverse = _reverse_adjacency(graph)
    deps: dict[str, set[str]] = {node_id: set() for node_id in executable_ids}
    for node_id in executable_ids:
        stack = list(reverse[node_id])
        seen: set[str] = set()
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            kind = classes[current]
            if kind in {"agent", "tool"}:
                deps[node_id].add(current)
                continue
            if kind == "exit":
                continue
            stack.extend(reverse[current])
    return deps


def _validate_no_cycles(deps: dict[str, set[str]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visited:
            return
        if node_id in visiting:
            raise ValidationError("graph contains a dependency cycle")
        visiting.add(node_id)
        for dep in deps[node_id]:
            visit(dep)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in deps:
        visit(node_id)


def _topological_order(node_ids: list[str], deps: dict[str, set[str]], graph: DotGraph) -> list[str]:
    remaining = set(node_ids)
    result: list[str] = []
    while remaining:
        ready = [node_id for node_id in remaining if not (deps[node_id] & remaining)]
        if not ready:
            raise ValidationError("graph contains a dependency cycle")
        ready.sort(key=lambda item: graph.nodes[item].order)
        result.extend(ready)
        remaining.difference_update(ready)
    return result


def _topological_sort_deps(deps: set[str], graph: DotGraph) -> list[str]:
    return sorted(deps, key=lambda item: graph.nodes[item].order)


def _adjacency(graph: DotGraph) -> dict[str, list[str]]:
    adj: dict[str, list[str]] = {node_id: [] for node_id in graph.nodes}
    for edge in graph.edges:
        adj[edge.src].append(edge.dst)
    return adj


def _reverse_adjacency(graph: DotGraph) -> dict[str, list[str]]:
    adj: dict[str, list[str]] = {node_id: [] for node_id in graph.nodes}
    for edge in graph.edges:
        adj[edge.dst].append(edge.src)
    return adj


def _walk(adj: dict[str, list[str]], starts: list[str]) -> set[str]:
    seen: set[str] = set()
    stack = list(starts)
    while stack:
        node_id = stack.pop()
        if node_id in seen:
            continue
        seen.add(node_id)
        stack.extend(adj[node_id])
    return seen
