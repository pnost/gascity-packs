from __future__ import annotations

from dataclasses import dataclass, field


class DotSyntaxError(Exception):
    pass


@dataclass
class DotNode:
    node_id: str
    attrs: dict[str, str] = field(default_factory=dict)
    order: int = 0


@dataclass
class DotEdge:
    src: str
    dst: str
    attrs: dict[str, str] = field(default_factory=dict)


@dataclass
class DotGraph:
    name: str
    graph_attrs: dict[str, str] = field(default_factory=dict)
    nodes: dict[str, DotNode] = field(default_factory=dict)
    edges: list[DotEdge] = field(default_factory=list)
    source: str = "<memory>"


@dataclass
class Token:
    kind: str
    value: str
    pos: int


SYMBOLS = {"{", "}", "[", "]", "=", ";", ",", ":"}


def parse_dot(text: str, source: str = "<memory>") -> DotGraph:
    return Parser(lex(text), source).parse()


def lex(text: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "#":
            i = _skip_line_comment(text, i + 1)
            continue
        if ch == "/" and i + 1 < len(text) and text[i + 1] == "/":
            i = _skip_line_comment(text, i + 2)
            continue
        if ch == "/" and i + 1 < len(text) and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            if end < 0:
                raise DotSyntaxError("unterminated block comment")
            i = end + 2
            continue
        if ch == "-" and i + 1 < len(text) and text[i + 1] == ">":
            tokens.append(Token("ARROW", "->", i))
            i += 2
            continue
        if ch == "-" and i + 1 < len(text) and text[i + 1] == "-":
            raise DotSyntaxError("undirected edges are not supported")
        if ch == "<":
            raise DotSyntaxError("HTML labels are not supported")
        if ch in SYMBOLS:
            tokens.append(Token(ch, ch, i))
            i += 1
            continue
        if ch == '"':
            value, i = _read_string(text, i)
            tokens.append(Token("VALUE", value, i))
            continue
        if ch.isalpha() or ch == "_":
            start = i
            i += 1
            while i < len(text) and (text[i].isalnum() or text[i] == "_"):
                i += 1
            tokens.append(Token("VALUE", text[start:i], start))
            continue
        if ch.isdigit() or ch == ".":
            start = i
            i += 1
            while i < len(text) and (text[i].isalnum() or text[i] in "._-"):
                i += 1
            tokens.append(Token("VALUE", text[start:i], start))
            continue
        raise DotSyntaxError(f"unexpected character {ch!r} at byte {i}")
    tokens.append(Token("EOF", "", len(text)))
    return tokens


def _skip_line_comment(text: str, i: int) -> int:
    while i < len(text) and text[i] not in "\r\n":
        i += 1
    return i


def _read_string(text: str, i: int) -> tuple[str, int]:
    out: list[str] = []
    i += 1
    while i < len(text):
        ch = text[i]
        if ch == '"':
            return "".join(out), i + 1
        if ch == "\\":
            i += 1
            if i >= len(text):
                raise DotSyntaxError("unterminated string escape")
            esc = text[i]
            out.append({"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}.get(esc, esc))
            i += 1
            continue
        out.append(ch)
        i += 1
    raise DotSyntaxError("unterminated string")


class Parser:
    def __init__(self, tokens: list[Token], source: str):
        self.tokens = tokens
        self.index = 0
        self.source = source
        self.graph = DotGraph(name="", source=source)
        self.next_order = 0

    def parse(self) -> DotGraph:
        first = self._take_value()
        if first == "graph":
            raise DotSyntaxError("undirected graphs are not supported")
        if first != "digraph":
            raise DotSyntaxError("expected digraph")
        if self._peek().kind == "VALUE":
            self.graph.name = self._take_value()
        else:
            self.graph.name = "G"
        self._expect("{")
        self._parse_stmt_list({}, {}, True)
        self._expect("}")
        self._expect("EOF")
        return self.graph

    def _parse_stmt_list(
        self, node_defaults: dict[str, str], edge_defaults: dict[str, str], top_level: bool
    ) -> None:
        while self._peek().kind not in {"}", "EOF"}:
            if self._peek().kind in {";", ","}:
                self.index += 1
                continue
            self._parse_stmt(node_defaults, edge_defaults, top_level)
            if self._peek().kind in {";", ","}:
                self.index += 1

    def _parse_stmt(self, node_defaults: dict[str, str], edge_defaults: dict[str, str], top_level: bool) -> None:
        tok = self._peek()
        if tok.kind != "VALUE":
            raise DotSyntaxError(f"expected statement at byte {tok.pos}")
        word = self._take_value()
        if word == "subgraph":
            if self._peek().kind == "VALUE":
                self._take_value()
            self._expect("{")
            self._parse_stmt_list(dict(node_defaults), dict(edge_defaults), False)
            self._expect("}")
            return
        if word in {"graph", "node", "edge"} and self._peek().kind == "[":
            attrs = self._parse_attr_lists()
            if word == "graph" and top_level:
                self.graph.graph_attrs.update(attrs)
            elif word == "node":
                node_defaults.update(attrs)
            elif word == "edge":
                edge_defaults.update(attrs)
            return
        if self._peek().kind == "=":
            self.index += 1
            value = self._take_value()
            if top_level:
                self.graph.graph_attrs[word] = value
            return
        if self._peek().kind == ":":
            raise DotSyntaxError("ports are not supported")
        if self._peek().kind == "ARROW":
            self._parse_edge_stmt(word, edge_defaults)
            return
        attrs = dict(node_defaults)
        if self._peek().kind == "[":
            attrs.update(self._parse_attr_lists())
        self._ensure_node(word, attrs)

    def _parse_edge_stmt(self, first: str, edge_defaults: dict[str, str]) -> None:
        chain = [first]
        while self._peek().kind == "ARROW":
            self.index += 1
            node_id = self._take_value()
            if self._peek().kind == ":":
                raise DotSyntaxError("ports are not supported")
            chain.append(node_id)
        attrs = dict(edge_defaults)
        if self._peek().kind == "[":
            attrs.update(self._parse_attr_lists())
        for node_id in chain:
            self._ensure_node(node_id, {})
        for src, dst in zip(chain, chain[1:]):
            self.graph.edges.append(DotEdge(src, dst, dict(attrs)))

    def _parse_attr_lists(self) -> dict[str, str]:
        attrs: dict[str, str] = {}
        while self._peek().kind == "[":
            self.index += 1
            while self._peek().kind != "]":
                key = self._take_value()
                self._expect("=")
                attrs[key] = self._take_value()
                if self._peek().kind in {",", ";"}:
                    self.index += 1
            self._expect("]")
        return attrs

    def _ensure_node(self, node_id: str, attrs: dict[str, str]) -> DotNode:
        existing = self.graph.nodes.get(node_id)
        if existing is not None:
            existing.attrs.update(attrs)
            return existing
        node = DotNode(node_id=node_id, attrs=dict(attrs), order=self.next_order)
        self.next_order += 1
        self.graph.nodes[node_id] = node
        return node

    def _take_value(self) -> str:
        tok = self._peek()
        if tok.kind != "VALUE":
            raise DotSyntaxError(f"expected value at byte {tok.pos}")
        self.index += 1
        return tok.value

    def _expect(self, kind: str) -> Token:
        tok = self._peek()
        if tok.kind != kind:
            raise DotSyntaxError(f"expected {kind}, got {tok.kind} at byte {tok.pos}")
        self.index += 1
        return tok

    def _peek(self) -> Token:
        return self.tokens[self.index]
