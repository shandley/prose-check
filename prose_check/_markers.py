"""Marker loading for prose_check."""

from __future__ import annotations

import importlib.resources
import json
import sys
from pathlib import Path


def find_markers_file() -> Path:
    """Find markers.json, checking package data first, then fallback locations."""
    # 1. Package data (installed package -- the canonical location)
    try:
        pkg_files = importlib.resources.files("prose_check")
        pkg_path = pkg_files / "data" / "markers.json"
        # files() returns a Traversable; resolve to Path via as_file context if needed
        # For regular installed packages the path is directly accessible
        resolved = Path(str(pkg_path))
        if resolved.exists():
            return resolved
    except (TypeError, AttributeError, ModuleNotFoundError):
        pass

    # 2. Local dev path (running from source tree)
    local_path = Path(__file__).parent / "data" / "markers.json"
    if local_path.exists():
        return local_path

    # 3. Venv / prefix install (data-files at <sys.prefix>/share/prose-check/)
    prefix_path = Path(sys.prefix) / "share" / "prose-check" / "markers.json"
    if prefix_path.exists():
        return prefix_path

    # 4. User data directory
    user_data = Path.home() / ".prose-check" / "markers.json"
    if user_data.exists():
        return user_data

    # Fall back to local path; load_markers() will emit a clear error if absent
    return local_path


def load_markers() -> list[dict]:
    """Load and return the markers list from markers.json."""
    path = find_markers_file()
    if not path.exists():
        raise FileNotFoundError(
            f"markers.json not found at {path}. "
            "Run 'uv run python scripts/build_curated_markers.py' to regenerate."
        )
    with open(path) as f:
        data = json.load(f)
    return data.get("markers", [])
