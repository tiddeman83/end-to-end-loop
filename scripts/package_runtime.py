#!/usr/bin/env python3
"""Measure and build the minimal end-to-end-loop runtime package."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "runtime-package.json"
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "runtime-package-v1":
        raise ValueError("unsupported runtime package schema")
    profiles = data.get("profiles")
    if not isinstance(profiles, dict) or not isinstance(profiles.get("runtime"), list):
        raise ValueError("runtime package manifest requires profiles.runtime")
    return data


def runtime_files(manifest: dict[str, Any], root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    seen: set[str] = set()
    for raw in manifest["profiles"]["runtime"]:
        if not isinstance(raw, str) or not raw:
            raise ValueError("runtime package entries must be non-empty strings")
        relative = PurePosixPath(raw)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"unsafe runtime package path: {raw}")
        if raw in seen:
            raise ValueError(f"duplicate runtime package path: {raw}")
        seen.add(raw)
        path = root / raw
        if not path.is_file():
            raise ValueError(f"runtime package file does not exist: {raw}")
        files.append(path)
    return files


def measure(manifest: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    files = runtime_files(manifest, root)
    runtime_bytes = sum(path.stat().st_size for path in files)
    repository_files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and "dist" not in path.parts
    ]
    repository_bytes = sum(path.stat().st_size for path in repository_files)
    return {
        "schema_version": "runtime-package-measurement-v1",
        "runtime_files": len(files),
        "runtime_bytes": runtime_bytes,
        "repository_files": len(repository_files),
        "repository_bytes": repository_bytes,
        "excluded_bytes": repository_bytes - runtime_bytes,
        "runtime_share": round(runtime_bytes / repository_bytes, 4) if repository_bytes else 0,
        "limit_bytes": manifest["limits"]["runtime_bytes"],
        "within_limit": runtime_bytes <= manifest["limits"]["runtime_bytes"],
    }


def build_archive(output: Path, manifest: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in runtime_files(manifest, root):
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"end-to-end-loop/{relative}", FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return {
        **measure(manifest, root),
        "archive": str(output),
        "archive_bytes": output.stat().st_size,
        "sha256": digest,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, help="Write a deterministic runtime ZIP archive.")
    parser.add_argument("--check", action="store_true", help="Fail when the runtime byte limit is exceeded.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = load_manifest()
    result = build_archive(args.build, manifest) if args.build else measure(manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.check and not result["within_limit"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
