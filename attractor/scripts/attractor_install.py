from __future__ import annotations

import os
import pathlib
import subprocess
import tempfile
import tomllib
from typing import Callable

from attractor_compile import CompileResult


class InstallError(Exception):
    pass


Runner = Callable[..., subprocess.CompletedProcess[str]]


def install_compiled_formula(
    compiled: CompileResult,
    city_path: str | pathlib.Path | None = None,
    force: bool = False,
    runner: Runner = subprocess.run,
) -> pathlib.Path:
    city = _city_path(city_path)
    ensure_formula_v2_enabled(city, runner)
    formulas = city / "formulas"
    formulas.mkdir(parents=True, exist_ok=True)
    canonical = formulas / f"{compiled.formula_name}.toml"
    legacy = formulas / f"{compiled.formula_name}.formula.toml"
    collisions = [path for path in [canonical, legacy] if path.exists()]
    if collisions and not force:
        existing = ", ".join(str(path) for path in collisions)
        raise InstallError(f"formula {compiled.formula_name!r} already exists: {existing}; use --force")
    _atomic_write(canonical, compiled.text)
    return canonical


def run_compiled_formula(
    compiled: CompileResult,
    target: str,
    city_path: str | pathlib.Path | None = None,
    force_install: bool = False,
    force_sling: bool = False,
    vars: list[str] | None = None,
    title: str = "",
    scope_kind: str = "",
    scope_ref: str = "",
    dry_run: bool = False,
    runner: Runner = subprocess.run,
) -> subprocess.CompletedProcess[str] | None:
    city = _city_path(city_path)
    if dry_run:
        ensure_formula_v2_enabled(city, runner)
    else:
        install_compiled_formula(compiled, city, force=force_install, runner=runner)
    args = ["gc", "sling", target, compiled.formula_name, "--formula"]
    if force_sling:
        args.append("--force")
    if title:
        args.extend(["--title", title])
    for item in vars or []:
        args.extend(["--var", item])
    if scope_kind or scope_ref:
        if not (scope_kind and scope_ref):
            raise InstallError("--scope-kind and --scope-ref must be provided together")
        args.extend(["--scope-kind", scope_kind, "--scope-ref", scope_ref])
    if dry_run:
        args.append("--dry-run")
    return runner(args, cwd=str(city), text=True, capture_output=True)


def ensure_formula_v2_enabled(city_path: pathlib.Path, runner: Runner = subprocess.run) -> None:
    result = runner(["gc", "config", "show"], cwd=str(city_path), text=True, capture_output=True)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise InstallError(f"gc config show failed: {stderr or result.returncode}")
    try:
        config = tomllib.loads(result.stdout or "")
    except tomllib.TOMLDecodeError as err:
        raise InstallError(f"parsing resolved config from gc config show: {err}") from err
    daemon = config.get("daemon") if isinstance(config, dict) else None
    enabled = isinstance(daemon, dict) and daemon.get("formula_v2") is True
    if not enabled:
        raise InstallError('graph.v2 formulas require [daemon] formula_v2 = true')


def _city_path(city_path: str | pathlib.Path | None) -> pathlib.Path:
    raw = city_path or os.environ.get("GC_CITY_PATH")
    if not raw:
        raise InstallError("missing city path; run inside a Gas City pack context or set GC_CITY_PATH")
    return pathlib.Path(raw)


def _atomic_write(path: pathlib.Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
