import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from attractor_dot import DotSyntaxError, parse_dot


class DotParserTests(unittest.TestCase):
    def test_parses_graph_attrs_defaults_subgraphs_and_edge_chains(self):
        graph = parse_dot(
            r'''
            digraph Simple {
              graph [label="Simple Flow", goal="Ship $task", default_max_retry=1]
              node [shape=box, style="rounded,filled"]

              subgraph cluster_main {
                label="Main"
                start [shape=Mdiamond]
                Build [label="Build It", prompt="Do $task"]
                Verify [shape=parallelogram, tool_command="make test"]
                exit [shape=Msquare]
              }

              start -> Build -> Verify -> exit
            }
            ''',
            source="simple.dot",
        )

        self.assertEqual(graph.name, "Simple")
        self.assertEqual(graph.graph_attrs["goal"], "Ship $task")
        self.assertEqual(graph.nodes["Build"].attrs["shape"], "box")
        self.assertEqual(graph.nodes["Build"].attrs["style"], "rounded,filled")
        self.assertEqual(graph.nodes["Verify"].attrs["shape"], "parallelogram")
        self.assertEqual(
            [(edge.src, edge.dst) for edge in graph.edges],
            [("start", "Build"), ("Build", "Verify"), ("Verify", "exit")],
        )

    def test_rejects_undirected_graphs(self):
        with self.assertRaises(DotSyntaxError):
            parse_dot("graph G { a -- b }")

    def test_rejects_html_labels(self):
        with self.assertRaises(DotSyntaxError):
            parse_dot("digraph G { a [label=<html>] }")

    def test_subgraph_visual_attrs_do_not_override_root_graph_attrs(self):
        graph = parse_dot(
            """
            digraph G {
              graph [label="Workflow"]
              subgraph cluster_one {
                label="Cluster"
                node [shape=box]
                Build [prompt="build"]
              }
            }
            """
        )

        self.assertEqual(graph.graph_attrs["label"], "Workflow")
        self.assertEqual(graph.nodes["Build"].attrs["shape"], "box")


if __name__ == "__main__":
    unittest.main()
