"""
prose_check -- Scientific prose quality checker.

Public API:
    check_text(text, context=None, checkers=None) -> CheckResult
    DocumentContext, SectionType, StudyType, Finding, CheckResult, Severity
"""

from __future__ import annotations

from ._models import (
    CheckResult,
    DocumentContext,
    Finding,
    Severity,
    SectionType,
    StudyType,
)
from .scoring import calculate_score, get_grade
from .checkers.ai_patterns import AIPatternChecker
from .checkers.stat_phrases import StatPhraseChecker
from .checkers.causal_lang import CausalLangChecker
from .checkers.structure import StructureChecker
from .checkers.bio_methods import BioMethodsChecker

__all__ = [
    "check_text",
    "CheckResult",
    "DocumentContext",
    "Finding",
    "Severity",
    "SectionType",
    "StudyType",
    "get_grade",
]

_ALL_CHECKERS = [
    AIPatternChecker(),
    StatPhraseChecker(),
    CausalLangChecker(),
    StructureChecker(),
    BioMethodsChecker(),
]

_CHECKER_MAP = {c.name: c for c in _ALL_CHECKERS}

# Default (deterministic) checkers. These are lexical, format, or corpus-grounded
# and produce stable, reproducible findings, so the 0-100 score is derived from them.
# causal_lang is deliberately excluded: detecting overstated causality is an
# open-ended semantic judgment that keyword lists cannot do without word-sense
# awareness (e.g. "controlled retrospectively", "regulated by", "X-mediated" are
# not causal claims). That judgment belongs to an LLM in the loop, posted as
# advisory annotations. causal_lang remains available via explicit checkers=[...].
_DEFAULT_CHECKER_NAMES = ["ai_patterns", "stat_phrases", "structure", "bio_methods"]


def check_text(
    text: str,
    context: DocumentContext | None = None,
    checkers: list[str] | None = None,
) -> CheckResult:
    """
    Check text for prose quality issues.

    Args:
        text: The text to analyse.
        context: Document context (section type, study type, journal, etc.).
                 Defaults to DocumentContext() -- unknown section, technical mode on.
        checkers: Names of checkers to run. Defaults to the deterministic set:
                  ["ai_patterns", "stat_phrases", "structure", "bio_methods"].
                  "causal_lang" is opt-in (advisory) and must be requested explicitly.

    Returns:
        CheckResult with all findings, a 0-100 score, and convenience properties.
    """
    ctx = context or DocumentContext()
    names = _DEFAULT_CHECKER_NAMES if checkers is None else checkers
    active = [_CHECKER_MAP[name] for name in names if name in _CHECKER_MAP]
    findings: list[Finding] = []
    for checker in active:
        findings.extend(checker.check(text, ctx))

    wc = len(text.split())
    score = calculate_score(findings, wc)
    return CheckResult(
        findings=findings,
        score=score,
        word_count=wc,
        section_type=ctx.section_type,
    )
