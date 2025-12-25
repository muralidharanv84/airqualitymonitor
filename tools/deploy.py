#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
from pathlib import Path

EXCLUDES = {
    ".DS_Store", ".Trashes", ".Spotlight-V100", ".fseventsd",
    "__pycache__",
}

def detect_circuitpy_mount() -> Path:
    # Allow override: CIRCUITPY=/Volumes/CIRCUITPY python tools/deploy.py
    env = os.getenv("CIRCUITPY")
    if env:
        p = Path(env)
        if p.exists():
            return p

    candidates = [
        Path("/Volumes/CIRCUITPY"),                  # macOS
        Path("/media") , Path("/mnt"),               # linux (varies)
        Path("E:/CIRCUITPY"), Path("F:/CIRCUITPY"),  # Windows (best-effort)
    ]
    for c in candidates:
        if c.exists():
            # linux: /media/<user>/CIRCUITPY
            if c.is_dir() and c.name == "CIRCUITPY":
                return c
            # search one level deep for linux mounts
            if c.is_dir():
                for child in c.glob("*/CIRCUITPY"):
                    if child.exists():
                        return child

    raise SystemExit("Could not find CIRCUITPY. Set CIRCUITPY env var to the mount path.")

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if any(p.startswith(".") for p in path.parts):
        return True
    return bool(parts & EXCLUDES)

def sync_dir(src: Path, dst: Path) -> None:
    # Copy everything except code.py first. Then copy code.py last to trigger reload.
    files = []
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        if should_skip(rel):
            continue
        if p.is_dir():
            continue
        files.append(rel)

    # Make sure directories exist
    for rel in sorted({f.parent for f in files}):
        (dst / rel).mkdir(parents=True, exist_ok=True)

    # Copy non-code.py first
    for rel in files:
        if rel.name == "code.py":
            continue
        shutil.copy2(src / rel, dst / rel)

    # Copy code.py last
    code_rel = Path("code.py")
    if (src / code_rel).exists():
        shutil.copy2(src / code_rel, dst / code_rel)

def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "device"
    if not src.exists():
        raise SystemExit(f"Missing {src}")

    dst = detect_circuitpy_mount()
    print(f"Deploying {src}  ->  {dst}")

    sync_dir(src, dst)
    print("Done. Board should auto-reload.")

if __name__ == "__main__":
    main()