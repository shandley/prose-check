"""Configuration loading for prose_check."""

from __future__ import annotations

import fnmatch
import sys
from pathlib import Path
from typing import Any

try:
    import yaml as _yaml
    _YAML_AVAILABLE = True
except ImportError:
    _yaml = None  # type: ignore[assignment]
    _YAML_AVAILABLE = False

DEFAULT_CONFIG: dict[str, Any] = {
    "min_score": 60,
    "exclude": [],
    "ignore_patterns": [],
    "technical": True,
}


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load config from .prose-check.yaml, merging with defaults."""
    config = DEFAULT_CONFIG.copy()

    if config_path is None:
        for candidate in (
            Path.cwd() / ".prose-check.yaml",
            Path.cwd() / ".prose-check.yml",
            Path(__file__).parent.parent / ".prose-check.yaml",
            Path(__file__).parent.parent / ".prose-check.yml",
        ):
            if candidate.exists():
                config_path = candidate
                break

    if config_path and config_path.exists():
        if not _YAML_AVAILABLE:
            print("Warning: PyYAML not installed, config file ignored", file=sys.stderr)
            return config
        try:
            with open(config_path) as f:
                file_config = _yaml.safe_load(f) or {}  # type: ignore[union-attr]
        except Exception as e:
            print(f"Warning: Invalid config file {config_path}: {e}", file=sys.stderr)
            return config
        for key in ("min_score", "exclude", "ignore_patterns", "technical"):
            if key in file_config:
                config[key] = file_config[key]

    return config


def should_exclude_file(filepath: str, exclude_patterns: list[str]) -> bool:
    """Return True if filepath matches any exclude glob pattern."""
    name = Path(filepath).name
    return any(
        fnmatch.fnmatch(filepath, pat) or fnmatch.fnmatch(name, pat)
        for pat in exclude_patterns
    )
