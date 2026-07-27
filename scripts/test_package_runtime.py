#!/usr/bin/env python3
"""Public-behavior tests for minimal runtime packaging."""

from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

import package_runtime


def main() -> int:
    manifest = package_runtime.load_manifest()
    measurement = package_runtime.measure(manifest)
    assert measurement["within_limit"], measurement
    assert measurement["runtime_bytes"] < measurement["repository_bytes"], measurement

    with tempfile.TemporaryDirectory() as tmp:
        first = Path(tmp) / "first.zip"
        second = Path(tmp) / "second.zip"
        first_result = package_runtime.build_archive(first, manifest)
        second_result = package_runtime.build_archive(second, manifest)
        assert first_result["sha256"] == second_result["sha256"]
        with zipfile.ZipFile(first) as archive:
            names = set(archive.namelist())
        assert "end-to-end-loop/SKILL.md" in names
        assert "end-to-end-loop/scripts/loop_kernel.py" in names
        assert not any(name.startswith("end-to-end-loop/evals/") for name in names)

    print("runtime package tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
