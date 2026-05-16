"""Statistical phrase quality checker."""

from __future__ import annotations

import importlib.resources
import json
import re
from functools import cached_property
from pathlib import Path

from .._models import DocumentContext, Finding, Severity, SectionType
from . import Checker


def _load_stat_phrases() -> dict:
    try:
        pkg_files = importlib.resources.files("prose_check")
        path = Path(str(pkg_files / "data" / "stat_phrases.json"))
        if path.exists():
            with open(path) as f:
                return json.load(f)
    except Exception:
        pass
    # fallback: local dev path
    local = Path(__file__).parent.parent / "data" / "stat_phrases.json"
    if local.exists():
        with open(local) as f:
            return json.load(f)
    return {}


class StatPhraseChecker(Checker):
    """
    Flags problematic statistical language in scientific manuscripts:
    - Phrases that soften non-significant results ("marginally significant")
    - Binary significance framing ("statistically significant" as conclusion)
    - Threshold-only p-value reporting ("p < 0.05" as a final value)
    """

    name = "stat_phrases"

    @cached_property
    def _data(self) -> dict:
        return _load_stat_phrases()

    def check(self, text: str, context: DocumentContext) -> list[Finding]:
        findings: list[Finding] = []
        findings.extend(self._check_marginal_phrases(text))
        findings.extend(self._check_binary_significance(text))
        findings.extend(self._check_threshold_pvalues(text, context))
        return findings

    def _check_marginal_phrases(self, text: str) -> list[Finding]:
        """Flag phrases that hedge non-significant results."""
        findings: list[Finding] = []
        for phrase in self._data.get("marginal_phrases", []):
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            for match in pattern.finditer(text):
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 40)
                ctx = "..." + text[start:end].replace("\n", " ") + "..."
                findings.append(Finding(
                    checker=self.name,
                    rule_id="marginal_sig",
                    text=match.group(),
                    message=(
                        f'"{phrase}" softens a non-significant result. '
                        "Report exact p-values and effect sizes without hedging."
                    ),
                    severity=Severity.HIGH,
                    alternative="Report exact p-value and effect size; omit the qualifier",
                    context=ctx,
                ))
        return findings

    def _check_binary_significance(self, text: str) -> list[Finding]:
        """Flag binary significant/not-significant framing used as a conclusion."""
        findings: list[Finding] = []
        for phrase in self._data.get("binary_sig_phrases", []):
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            for match in pattern.finditer(text):
                # Check if an exact p-value appears within ±100 chars (mitigates false positives)
                window_start = max(0, match.start() - 100)
                window_end = min(len(text), match.end() + 100)
                window = text[window_start:window_end]
                has_exact_pvalue = bool(re.search(
                    r"p\s*[=<>]\s*0?\.\d{3,}",  # e.g. p = 0.032, p < 0.001
                    window, re.IGNORECASE
                ))
                if not has_exact_pvalue:
                    ctx_start = max(0, match.start() - 40)
                    ctx_end = min(len(text), match.end() + 40)
                    ctx = "..." + text[ctx_start:ctx_end].replace("\n", " ") + "..."
                    findings.append(Finding(
                        checker=self.name,
                        rule_id="binary_sig",
                        text=match.group(),
                        message=(
                            f'"{phrase}" frames significance as binary. '
                            "Report exact p-values and effect sizes."
                        ),
                        severity=Severity.MEDIUM,
                        alternative="Report exact p-value (e.g., p = 0.032) and effect size",
                        context=ctx,
                    ))
        return findings

    def _check_threshold_pvalues(self, text: str, context: DocumentContext) -> list[Finding]:
        """Flag p-values reported only as threshold comparisons in results/discussion."""
        # Only flag in results and discussion — threshold reporting in methods (e.g.,
        # "we used p < 0.05 as the significance threshold") is appropriate.
        if context.section_type not in (
            SectionType.RESULTS, SectionType.DISCUSSION, SectionType.UNKNOWN
        ):
            return []
        findings: list[Finding] = []
        for pval_str in self._data.get("threshold_pvalue_strings", []):
            pattern = re.compile(re.escape(pval_str), re.IGNORECASE)
            for match in pattern.finditer(text):
                # Skip if this looks like a methods threshold definition
                window_start = max(0, match.start() - 80)
                window = text[window_start:match.start()].lower()
                if any(kw in window for kw in ("threshold", "cutoff", "significance level",
                                                "set to", "defined as", "criterion")):
                    continue
                ctx_start = max(0, match.start() - 40)
                ctx_end = min(len(text), match.end() + 40)
                ctx = "..." + text[ctx_start:ctx_end].replace("\n", " ") + "..."
                findings.append(Finding(
                    checker=self.name,
                    rule_id="threshold_pvalue",
                    text=match.group(),
                    message=(
                        f'"{pval_str}" reports only a threshold, not an exact p-value. '
                        "Most journals require exact values unless p < 0.001."
                    ),
                    severity=Severity.MEDIUM,
                    alternative='Report exact p-value, e.g. "p = 0.032". Use "p < 0.001" only when appropriate.',
                    context=ctx,
                ))
        return findings
