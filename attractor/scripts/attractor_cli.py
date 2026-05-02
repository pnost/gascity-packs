#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

from attractor_compile import compile_dot
from attractor_dot import DotSyntaxError
from attractor_install import InstallError, install_compiled_formula, run_compiled_formula
from attractor_model import ValidationError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gc attractor")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a strict static Attractor DOT file")
    validate.add_argument("dot_file")

    compile_cmd = sub.add_parser("compile", help="compile DOT to a graph.v2 formula")
    compile_cmd.add_argument("dot_file")
    compile_cmd.add_argument("--formula")
    compile_cmd.add_argument("--output", "-o")

    install = sub.add_parser("install", help="install a compiled formula into city/formulas")
    install.add_argument("dot_file")
    install.add_argument("--formula")
    install.add_argument("--force", action="store_true")

    run = sub.add_parser("run", help="install and run a DOT workflow through gc sling")
    run.add_argument("target")
    run.add_argument("dot_file")
    run.add_argument("--formula")
    run.add_argument("--force-install", action="store_true")
    run.add_argument("--force-sling", action="store_true")
    run.add_argument("--var", action="append", default=[])
    run.add_argument("--title", default="")
    run.add_argument("--scope-kind", default="")
    run.add_argument("--scope-ref", default="")
    run.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            compiled = _compile_path(args.dot_file, None)
            for warning in compiled.warnings:
                print(f"warning: {warning}", file=sys.stderr)
            print(f"{args.dot_file}: ok")
            return 0
        if args.command == "compile":
            compiled = _compile_path(args.dot_file, args.formula)
            if args.output:
                pathlib.Path(args.output).write_text(compiled.text, encoding="utf-8")
            else:
                print(compiled.text, end="")
            _print_warnings(compiled.warnings)
            return 0
        if args.command == "install":
            compiled = _compile_path(args.dot_file, args.formula)
            path = install_compiled_formula(compiled, force=args.force)
            _print_warnings(compiled.warnings)
            print(path)
            return 0
        if args.command == "run":
            compiled = _compile_path(args.dot_file, args.formula)
            result = run_compiled_formula(
                compiled,
                target=args.target,
                force_install=args.force_install,
                force_sling=args.force_sling,
                vars=args.var,
                title=args.title,
                scope_kind=args.scope_kind,
                scope_ref=args.scope_ref,
                dry_run=args.dry_run,
            )
            _print_warnings(compiled.warnings)
            if result is None:
                return 0
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            return result.returncode
    except (DotSyntaxError, ValidationError, InstallError, OSError, subprocess.SubprocessError) as err:
        print(f"gc attractor {args.command}: {err}", file=sys.stderr)
        return 1
    return 1


def _compile_path(path: str, formula: str | None):
    dot_path = pathlib.Path(path)
    text = dot_path.read_text(encoding="utf-8")
    return compile_dot(text, formula_name=formula, source_label=path)


def _print_warnings(warnings: list[str]) -> None:
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
