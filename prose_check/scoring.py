"""Scoring for prose_check check results."""

from __future__ import annotations

from ._models import Finding, Severity


def calculate_score(findings: list[Finding], word_count: int) -> int:
    """
    Convert findings into a 0-100 score (100 = most human-like).

    Penalty is proportional to finding density per 100 words:
      high severity: -10 pts each
      medium severity: -3 pts each
    """
    if word_count == 0:
        return 100
    high = sum(1 for f in findings if f.severity == Severity.HIGH)
    medium = sum(1 for f in findings if f.severity == Severity.MEDIUM)
    penalty = (high * 10 + medium * 3) / (word_count / 100)
    return max(0, min(100, int(100 - penalty)))


def get_grade(score: int) -> str:
    if score >= 90:
        return "Excellent - Very human-like"
    elif score >= 75:
        return "Good - Minor issues"
    elif score >= 60:
        return "Fair - Some AI patterns"
    elif score >= 40:
        return "Needs work - Notable AI patterns"
    return "High AI signal - Many AI patterns"
