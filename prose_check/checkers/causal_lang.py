"""Causal language checker for observational scientific studies."""

from __future__ import annotations

import importlib.resources
import json
import re
from functools import cached_property
from pathlib import Path

from .._models import DocumentContext, Finding, Severity, SectionType, StudyType
from . import Checker


def _load_causal_data() -> dict:
    try:
        pkg_files = importlib.resources.files("prose_check")
        path = Path(str(pkg_files / "data" / "causal_verbs.json"))
        if path.exists():
            with open(path) as f:
                return json.load(f)
    except Exception:
        pass
    local = Path(__file__).parent.parent / "data" / "causal_verbs.json"
    if local.exists():
        with open(local) as f:
            return json.load(f)
    return {}


# Sections where causal language is flagged (not methods/introduction where framing is fine)
_FLAGGED_SECTIONS = {SectionType.RESULTS, SectionType.DISCUSSION, SectionType.UNKNOWN}

# Study types where causal claims need flagging
_OBSERVATIONAL_TYPES = {StudyType.OBSERVATIONAL, StudyType.UNKNOWN}


class CausalLangChecker(Checker):
    """
    Flags causal verbs and phrases in results/discussion of observational studies.

    Causal language ("drives", "causes", "demonstrates") is appropriate in experimental
    contexts but overstates the evidence in observational studies (GWAS, population
    genetics, molecular ecology surveys). Does not fire in methods or introduction
    sections, or when study type is explicitly experimental.
    """

    name = "causal_lang"

    @cached_property
    def _data(self) -> dict:
        return _load_causal_data()

    @cached_property
    def _causal_pattern(self) -> re.Pattern:
        all_terms = self._data.get("causal_verbs", []) + self._data.get("causal_phrases", [])
        # Sort longest first to prefer multi-word phrase matches
        all_terms.sort(key=len, reverse=True)
        escaped = [re.escape(t) for t in all_terms]
        return re.compile(r"\b(?:" + "|".join(escaped) + r")\b", re.IGNORECASE)

    def check(self, text: str, context: DocumentContext) -> list[Finding]:
        # Skip in methods and introduction — causal framing is fine there
        if context.section_type not in _FLAGGED_SECTIONS:
            return []
        # Skip for experimental studies — causality can be supported
        if context.study_type not in _OBSERVATIONAL_TYPES:
            return []

        findings: list[Finding] = []
        alternatives_map = self._data.get("associational_alternatives", {})

        for match in self._causal_pattern.finditer(text):
            term = match.group()
            alt = alternatives_map.get(term.lower(), "is associated with")
            ctx_start = max(0, match.start() - 50)
            ctx_end = min(len(text), match.end() + 50)
            ctx = "..." + text[ctx_start:ctx_end].replace("\n", " ") + "..."
            findings.append(Finding(
                checker=self.name,
                rule_id="causal_verb",
                text=term,
                message=(
                    f'"{term}" implies causality. In observational studies, '
                    "use associational language."
                ),
                severity=Severity.MEDIUM,
                alternative=alt,
                context=ctx,
            ))

        return findings
