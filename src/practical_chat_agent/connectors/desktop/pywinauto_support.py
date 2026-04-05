from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from typing import Any


def prepare_pywinauto(cache_dir: Path | None = None) -> tuple[Any | None, list[str]]:
    """Import pywinauto with a workspace-local comtypes cache."""

    notes: list[str] = []

    if importlib.util.find_spec("pywinauto") is None:
        notes.append("pywinauto is not installed yet, so desktop UI automation is unavailable.")
        return None, notes

    resolved_cache_dir = _ensure_local_comtypes_cache(cache_dir)

    try:
        import comtypes

        gen_module = sys.modules.get("comtypes.gen")
        if gen_module is None:
            gen_module = types.ModuleType("comtypes.gen")
            gen_module.__path__ = [str(resolved_cache_dir)]
            sys.modules["comtypes.gen"] = gen_module
        else:
            existing_paths = list(getattr(gen_module, "__path__", []))
            if str(resolved_cache_dir) not in existing_paths:
                existing_paths.append(str(resolved_cache_dir))
                gen_module.__path__ = existing_paths

        comtypes.gen = gen_module

        import comtypes.client

        comtypes.client.gen_dir = str(resolved_cache_dir)
        notes.append(f"Using local comtypes cache at '{resolved_cache_dir}'.")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"Failed to configure the local comtypes cache: {exc}")
        return None, notes

    try:
        from pywinauto import Desktop  # type: ignore
    except Exception as exc:  # noqa: BLE001
        notes.append(f"pywinauto import failed: {exc}")
        return None, notes

    return Desktop, notes


def _ensure_local_comtypes_cache(cache_dir: Path | None) -> Path:
    resolved_cache_dir = (cache_dir or Path.cwd() / ".cache" / "comtypes_gen").resolve()
    resolved_cache_dir.mkdir(parents=True, exist_ok=True)

    init_path = resolved_cache_dir / "__init__.py"
    if not init_path.exists():
        init_path.write_text("# local comtypes cache for pywinauto\n", encoding="utf-8")

    return resolved_cache_dir
