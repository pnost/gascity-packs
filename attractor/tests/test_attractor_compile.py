import pathlib
import sys
import tomllib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from attractor_compile import compile_dot
from attractor_model import ValidationError


class CompilerTests(unittest.TestCase):
    def test_compiles_static_graph_to_graph_v2_formula(self):
        result = compile_dot(
            r'''
            digraph Simple {
              graph [
                label="Simple Flow",
                goal="$task",
                default_max_retry=1
              ]

              start [shape=Mdiamond]
              exit [shape=Msquare]
              Build [shape=box, label="Build It", prompt="Goal: $goal\nDo $task", gc_run_target="{{worker_target}}"]
              Verify [shape=parallelogram, max_retries=0, tool_command="make test"]

              start -> Build -> Verify -> exit
            }
            ''',
            source_label="examples/simple.dot",
        )

        parsed = tomllib.loads(result.text)
        self.assertEqual(parsed["formula"], "mol-attractor-simple")
        self.assertEqual(parsed["contract"], "graph.v2")
        self.assertIn("source_sha256", result.text)

        self.assertTrue(parsed["vars"]["task"]["required"])
        self.assertTrue(parsed["vars"]["worker_target"]["required"])
        self.assertNotIn("goal", parsed["vars"])

        steps = {step["id"]: step for step in parsed["steps"]}
        self.assertEqual(steps["body"]["metadata"]["gc.kind"], "scope")
        self.assertEqual(steps["body"]["needs"], ["build", "verify"])
        self.assertEqual(steps["build"]["needs"], [])
        self.assertEqual(steps["verify"]["needs"], ["build"])
        self.assertEqual(steps["build"]["metadata"]["gc.run_target"], "{{worker_target}}")
        self.assertEqual(steps["build"]["metadata"]["attractor.node_id"], "Build")
        self.assertIn("Goal: {{task}}", steps["build"]["description"])
        self.assertEqual(steps["build"]["retry"]["max_attempts"], 2)
        self.assertNotIn("retry", steps["verify"])

    def test_rejects_dynamic_edge_conditions(self):
        with self.assertRaisesRegex(ValidationError, 'edge Build -> Verify: unsupported attribute "condition"'):
            compile_dot(
                """
                digraph G {
                  start [shape=Mdiamond]
                  exit [shape=Msquare]
                  Build [shape=box, prompt="build"]
                  Verify [shape=box, prompt="verify"]
                  start -> Build
                  Build -> Verify [condition="outcome=success"]
                  Verify -> exit
                }
                """
            )

    def test_rejects_normalized_step_id_collisions(self):
        with self.assertRaisesRegex(ValidationError, "normalize to the same step id"):
            compile_dot(
                """
                digraph G {
                  start [shape=Mdiamond]
                  exit [shape=Msquare]
                  BuildTest [shape=box, prompt="one"]
                  build_test [shape=box, prompt="two"]
                  start -> BuildTest -> exit
                  start -> build_test -> exit
                }
                """
            )

    def test_rejects_unknown_runtime_hints(self):
        with self.assertRaisesRegex(ValidationError, 'node Build: unsupported attribute "timeout"'):
            compile_dot(
                """
                digraph G {
                  start [shape=Mdiamond]
                  exit [shape=Msquare]
                  Build [shape=box, prompt="build", timeout=300]
                  start -> Build -> exit
                }
                """
            )

    def test_collects_variables_from_formula_description(self):
        result = compile_dot(
            """
            digraph G {
              graph [label="Release $task"]
              start [shape=Mdiamond]
              exit [shape=Msquare]
              Build [shape=box, prompt="build"]
              start -> Build -> exit
            }
            """
        )

        parsed = tomllib.loads(result.text)
        self.assertEqual(parsed["description"], "Release {{task}}")
        self.assertTrue(parsed["vars"]["task"]["required"])

    def test_source_provenance_does_not_emit_absolute_paths(self):
        result = compile_dot(
            """
            digraph G {
              start [shape=Mdiamond]
              exit [shape=Msquare]
              Build [shape=box, prompt="build"]
              start -> Build -> exit
            }
            """,
            source_label="/tmp/private/demo.dot",
        )

        self.assertEqual(result.formula_name, "mol-attractor-demo")
        self.assertIn('# source = "demo.dot"', result.text)
        self.assertNotIn("/tmp/private", result.text)

    def test_rejects_false_is_codergen_flag(self):
        with self.assertRaisesRegex(ValidationError, 'node Build: is_codergen must be "true" when present'):
            compile_dot(
                """
                digraph G {
                  start [shape=Mdiamond]
                  exit [shape=Msquare]
                  Build [shape=box, prompt="build", is_codergen=false]
                  start -> Build -> exit
                }
                """
            )


if __name__ == "__main__":
    unittest.main()
