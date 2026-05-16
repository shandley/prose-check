from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SectionType(str, Enum):
    INTRODUCTION = "introduction"
    METHODS = "methods"
    RESULTS = "results"
    DISCUSSION = "discussion"
    ABSTRACT = "abstract"
    UNKNOWN = "unknown"


class StudyType(str, Enum):
    OBSERVATIONAL = "observational"
    EXPERIMENTAL = "experimental"
    REVIEW = "review"
    METHODS_PAPER = "methods_paper"
    UNKNOWN = "unknown"


@dataclass
class Finding:
    checker: str        # "ai_patterns", "stat_phrases", "causal_lang", "structure", "bio_methods"
    rule_id: str        # e.g. "llm_word_delve", "marginal_sig", "causal_drives"
    text: str           # the flagged text span
    message: str        # human-readable explanation
    severity: Severity
    alternative: str | None = None   # suggested replacement
    context: str | None = None       # surrounding text snippet for display


@dataclass
class DocumentContext:
    section_type: SectionType = SectionType.UNKNOWN
    study_type: StudyType = StudyType.UNKNOWN
    journal: str | None = None
    technical: bool = True   # when True, suppress technical term false positives


@dataclass
class CheckResult:
    findings: list[Finding]
    score: int            # 0-100, higher = more human-like
    word_count: int
    section_type: SectionType

    @property
    def high(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.HIGH]

    @property
    def medium(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.MEDIUM]

    @property
    def low(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.LOW]

    def by_checker(self, checker_name: str) -> list[Finding]:
        return [f for f in self.findings if f.checker == checker_name]
