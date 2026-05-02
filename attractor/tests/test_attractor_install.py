import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from attractor_compile import CompileResult
from attractor_install import InstallError, install_compiled_formula, run_compiled_formula


class FakeRunner:
    def __init__(self):
        self.calls = []

    def __call__(self, args, **kwargs):
        self.calls.append((list(args), kwargs))
        if args[:3] == ["gc", "config", "show"]:
            return subprocess.CompletedProcess(args, 0, stdout="[daemon]\nformula_v2 = true\n", stderr="")
        return subprocess.CompletedProcess(args, 0, stdout="slung\n", stderr="")


class InstallTests(unittest.TestCase):
    def test_install_refuses_legacy_collision_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            city = pathlib.Path(tmp)
            formulas = city / "formulas"
            formulas.mkdir()
            (formulas / "mol-attractor-demo.formula.toml").write_text("legacy", encoding="utf-8")
            compiled = CompileResult("mol-attractor-demo", "formula = \"mol-attractor-demo\"\n", [])

            with self.assertRaisesRegex(InstallError, "already exists"):
                install_compiled_formula(compiled, city_path=city, force=False, runner=FakeRunner())

    def test_install_writes_canonical_toml_when_forced(self):
        with tempfile.TemporaryDirectory() as tmp:
            city = pathlib.Path(tmp)
            compiled = CompileResult("mol-attractor-demo", "formula = \"mol-attractor-demo\"\n", [])
            path = install_compiled_formula(compiled, city_path=city, force=True, runner=FakeRunner())

            self.assertEqual(path, city / "formulas" / "mol-attractor-demo.toml")
            self.assertEqual(path.read_text(encoding="utf-8"), compiled.text)

    def test_run_keeps_install_and_sling_force_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            city = pathlib.Path(tmp)
            runner = FakeRunner()
            compiled = CompileResult("mol-attractor-demo", "formula = \"mol-attractor-demo\"\n", [])

            run_compiled_formula(
                compiled,
                target="worker",
                city_path=city,
                force_install=True,
                force_sling=True,
                vars=["task=ship"],
                title="Demo",
                scope_kind="city",
                scope_ref="demo",
                runner=runner,
            )

            sling_calls = [call for call in runner.calls if call[0][:2] == ["gc", "sling"]]
            self.assertEqual(len(sling_calls), 1)
            args = sling_calls[0][0]
            self.assertIn("--force", args)
            self.assertIn("--formula", args)
            self.assertIn("--var", args)
            self.assertIn("task=ship", args)


if __name__ == "__main__":
    unittest.main()
