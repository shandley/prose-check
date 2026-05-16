"""Command-line interface for prose_check."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from . import check_text
from ._config import load_config, should_exclude_file
from ._models import (
    CheckResult, DocumentContext, Severity,
    SectionType, StudyType,
)
from .formatter import format_html, format_json, format_json_batch, format_text

SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".docx"}

_SECTION_MAP = {
    "introduction": SectionType.INTRODUCTION,
    "methods": SectionType.METHODS,
    "results": SectionType.RESULTS,
    "discussion": SectionType.DISCUSSION,
    "abstract": SectionType.ABSTRACT,
}

_STUDY_MAP = {
    "observational": StudyType.OBSERVATIONAL,
    "experimental": StudyType.EXPERIMENTAL,
    "review": StudyType.REVIEW,
    "methods-paper": StudyType.METHODS_PAPER,
}


def read_file(path: Path) -> str:
    """Read text from .txt/.md/.docx files."""
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        print(f"Error: Unsupported file type '{suffix}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}", file=sys.stderr)
        sys.exit(1)
    if suffix == ".docx":
        return _read_docx(path)
    return path.read_text()


def _read_docx(path: Path) -> str:
    """Extract text from .docx via textutil (macOS) or python-docx fallback."""
    try:
        result = subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", str(path)],
            capture_output=True, text=True, check=True,
        )
        return result.stdout
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError as e:
        print(f"Error converting docx: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        from docx import Document  # type: ignore[import-untyped]
        doc = Document(str(path))
        return "\n".join(para.text for para in doc.paragraphs)
    except ImportError:
        print("Error: Cannot read .docx. Install python-docx: pip install python-docx", file=sys.stderr)
        sys.exit(1)


def _highlight(text: str, pattern: str, window: int = 60) -> str:
    """Return ANSI-highlighted context snippet."""
    import re
    match = re.search(r"\b" + re.escape(pattern) + r"\b", text, re.IGNORECASE)
    if not match:
        return text[:window * 2]
    start = max(0, match.start() - window)
    end = min(len(text), match.end() + window)
    return (
        ("..." if start > 0 else "")
        + text[start:match.start()]
        + f"\033[1;31m{text[match.start():match.end()]}\033[0m"
        + text[match.end():end]
        + ("..." if end < len(text) else "")
    )


def _apply_replacement(text: str, pattern: str, replacement: str) -> str:
    """Replace the first occurrence of pattern with replacement."""
    import re
    m = re.search(r"\b" + re.escape(pattern) + r"\b", text, re.IGNORECASE)
    if not m:
        return text
    return text[:m.start()] + replacement + text[m.end():]


def interactive_mode(text: str, result: CheckResult, filepath: str) -> tuple[str, int]:
    """Interactively review findings and apply fixes. Returns (modified_text, changes_made)."""
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    print(f"File: {filepath}")
    print("Commands: [a]ccept suggestion, [s]kip, [e]dit manually, [q]uit")
    print("=" * 60 + "\n")

    modified = text
    changes = 0

    # Process high then medium findings; skip structural/aggregate ones
    candidates = [
        f for f in (result.high + result.medium)
        if f.rule_id not in ("short_paragraphs", "bullet_overuse", "hedging_overuse",
                              "formulaic_starters", "em_dash_overuse", "missing_accession")
    ]

    for i, finding in enumerate(candidates, 1):
        import re
        if not re.search(r"\b" + re.escape(finding.text) + r"\b", modified, re.IGNORECASE):
            continue

        color = "\033[1;31m" if finding.severity == Severity.HIGH else "\033[1;33m"
        print(f"\n[{i}/{len(candidates)}] {color}{finding.severity.value.upper()}\033[0m: \"{finding.text}\"")
        print(f"Context: {_highlight(modified, finding.text)}")
        if finding.alternative:
            print(f"Suggestions: {finding.alternative}")

        while True:
            try:
                choice = input("\n[a]ccept / [s]kip / [e]dit / [q]uit > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                choice = "q"

            if choice == "q":
                if changes > 0:
                    return modified, changes
                return text, 0
            elif choice == "s":
                break
            elif choice == "a":
                if not finding.alternative:
                    print("No suggestion available. Use [e]dit.")
                    continue
                # Take first suggestion; strip meta-notes like "(delete)"
                alts = [a.strip() for a in finding.alternative.split(",")]
                replacement = alts[0]
                if replacement.startswith("(") and replacement.endswith(")"):
                    replacement = ""
                import re as _re
                replacement = _re.sub(r"\s*\(or delete\)\s*", "", replacement, flags=_re.IGNORECASE).strip()
                replacement = _re.sub(r"\s*\([^)]+\)\s*$", "", replacement).strip()
                old = modified
                modified = _apply_replacement(modified, finding.text, replacement)
                if modified != old:
                    changes += 1
                    if replacement:
                        print(f"\033[31m- {finding.text}\033[0m\n\033[32m+ {replacement}\033[0m")
                    else:
                        print(f"\033[31m- {finding.text}\033[0m (deleted)")
                break
            elif choice == "e":
                try:
                    replacement = input("Enter replacement: ").strip()
                except (EOFError, KeyboardInterrupt):
                    continue
                old = modified
                modified = _apply_replacement(modified, finding.text, replacement)
                if modified != old:
                    changes += 1
                    print(f"\033[31m- {finding.text}\033[0m\n\033[32m+ {replacement}\033[0m")
                break
            else:
                print("Use a/s/e/q")

    print(f"\n{'=' * 60}\nChanges made: {changes}")
    if changes > 0:
        while True:
            try:
                save = input(f"\nSave changes to {filepath}? [y/n] > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return text, 0
            if save == "y":
                return modified, changes
            elif save == "n":
                return text, 0

    return text, 0


def process_file(
    filepath: str,
    context: DocumentContext,
    checker_names: list[str] | None,
    config: dict,
    interactive: bool = False,
) -> dict:
    """Process a single file, return a result dict."""
    path = Path(filepath)
    if not path.exists():
        return {"filename": filepath, "error": f"File not found: {filepath}"}
    if should_exclude_file(filepath, config.get("exclude", [])):
        return {"filename": filepath, "excluded": True}
    try:
        text = read_file(path)
    except Exception as e:
        return {"filename": filepath, "error": str(e)}

    result = check_text(text, context=context, checkers=checker_names)

    # Filter user-configured ignore_patterns
    ignore = {p.lower() for p in config.get("ignore_patterns", [])}
    if ignore:
        result = CheckResult(
            findings=[f for f in result.findings if f.text.lower() not in ignore],
            score=result.score,
            word_count=result.word_count,
            section_type=result.section_type,
        )
        from .scoring import calculate_score
        result = CheckResult(
            findings=result.findings,
            score=calculate_score(result.findings, result.word_count),
            word_count=result.word_count,
            section_type=result.section_type,
        )

    if interactive:
        modified, changes = interactive_mode(text, result, filepath)
        if changes > 0:
            path.write_text(modified)
            print(f"Saved {changes} changes to {filepath}")
            result = check_text(modified, context=context, checkers=checker_names)

    return {"filename": filepath, "result": result}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check writing for AI patterns and scientific prose issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prose-check document.md
  prose-check document.md --verbose
  prose-check document.md --format json
  prose-check document.md --section results --study-type observational
  prose-check document.md --checkers ai_patterns,stat_phrases
  cat document.md | prose-check --stdin
        """,
    )
    parser.add_argument("files", nargs="*", help="Files to check")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument(
        "--format", "-f", choices=["text", "json", "html"], default="text",
        help="Output format (default: text)",
    )
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive fix mode")
    parser.add_argument("--config", "-c", type=Path, help="Config file path")
    parser.add_argument("--min-score", type=int, help="Minimum score to pass")
    parser.add_argument("--no-technical", action="store_true", help="Stricter mode (no tech term exclusions)")
    parser.add_argument(
        "--section",
        choices=list(_SECTION_MAP.keys()),
        default=None,
        help="Section type for context-sensitive checks",
    )
    parser.add_argument(
        "--study-type",
        choices=list(_STUDY_MAP.keys()),
        default=None,
        dest="study_type",
        help="Study design type; activates causal language checker",
    )
    parser.add_argument(
        "--checkers",
        default=None,
        help="Comma-separated checker names to run (default: all)",
    )
    parser.add_argument("--json", "-j", action="store_true", help=argparse.SUPPRESS)  # legacy

    args = parser.parse_args()

    if args.json:
        args.format = "json"

    config = load_config(args.config)
    if args.min_score is not None:
        config["min_score"] = args.min_score
    if args.no_technical:
        config["technical"] = False

    min_score: int = config["min_score"]

    context = DocumentContext(
        section_type=_SECTION_MAP.get(args.section or "", SectionType.UNKNOWN),
        study_type=_STUDY_MAP.get(args.study_type or "", StudyType.UNKNOWN),
        technical=config.get("technical", True),
    )

    checker_names: list[str] | None = None
    if args.checkers:
        checker_names = [c.strip() for c in args.checkers.split(",")]

    if args.interactive and args.stdin:
        print("Error: --interactive requires file input (not stdin)", file=sys.stderr)
        sys.exit(1)

    # stdin mode
    if args.stdin:
        text = sys.stdin.read()
        result = check_text(text, context=context, checkers=checker_names)
        if args.format == "json":
            print(format_json(result, "<stdin>"))
        elif args.format == "html":
            print(format_html(result, "<stdin>"))
        else:
            print(format_text(result, "<stdin>", args.verbose))
        sys.exit(0 if result.score >= min_score else 1)

    if not args.files:
        parser.print_help()
        sys.exit(1)

    # file(s) mode
    outputs: list[tuple[str, CheckResult]] = []
    any_failed = False

    for filepath in args.files:
        item = process_file(
            filepath=filepath,
            context=context,
            checker_names=checker_names,
            config=config,
            interactive=args.interactive,
        )
        if item.get("error"):
            print(f"Error: {item['error']}", file=sys.stderr)
            any_failed = True
        elif item.get("excluded"):
            if args.verbose:
                print(f"Excluded: {filepath}", file=sys.stderr)
        elif "result" in item:
            r: CheckResult = item["result"]
            outputs.append((filepath, r))
            if r.score < min_score:
                any_failed = True

    if not outputs:
        if not any_failed:
            print("No valid files to check.", file=sys.stderr)
        sys.exit(1 if any_failed else 0)

    if args.interactive:
        pass  # interactive_mode handles its own output
    elif args.format == "json":
        if len(outputs) == 1:
            print(format_json(outputs[0][1], outputs[0][0]))
        else:
            print(format_json_batch(outputs))
    elif args.format == "html":
        if len(outputs) == 1:
            print(format_html(outputs[0][1], outputs[0][0]))
        else:
            print("<!DOCTYPE html><html><body>")
            print(f"<h1>Batch Report: {len(outputs)} files</h1><ul>")
            for fname, r in outputs:
                print(f"<li>{fname}: {r.score}/100</li>")
            print("</ul></body></html>")
    else:
        for fname, r in outputs:
            print(format_text(r, fname, args.verbose))
            if len(outputs) > 1:
                print()
        if len(outputs) > 1:
            print("=" * 60)
            print("BATCH SUMMARY")
            print("=" * 60)
            print(f"Files checked: {len(outputs)}")
            passing = sum(1 for _, r in outputs if r.score >= min_score)
            print(f"Passing (>={min_score}): {passing}")
            print(f"Failing (<{min_score}): {len(outputs) - passing}")
            avg = sum(r.score for _, r in outputs) / len(outputs)
            print(f"Average score: {avg:.1f}")
            print("=" * 60)

    sys.exit(1 if any_failed else 0)


if __name__ == "__main__":
    main()
