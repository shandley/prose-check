"""Bioinformatics methods completeness checker."""

from __future__ import annotations

import importlib.resources
import json
import re
from functools import cached_property
from pathlib import Path

from .._models import DocumentContext, Finding, Severity, SectionType
from . import Checker


def _load_bio_tools() -> dict:
    try:
        pkg_files = importlib.resources.files("prose_check")
        path = Path(str(pkg_files / "data" / "bio_tools.json"))
        if path.exists():
            with open(path) as f:
                return json.load(f)
    except Exception:
        pass
    local = Path(__file__).parent.parent / "data" / "bio_tools.json"
    if local.exists():
        with open(local) as f:
            return json.load(f)
    return {}


# Patterns indicating a version number follows or precedes a tool name
_VERSION_PATTERN = re.compile(
    r"(?:v|version\s+|ver\s+|ver\.\s*)?\d+[\.\-]\d+(?:[\.\-]\d+)?",
    re.IGNORECASE,
)

_DATA_UNAVAILABLE_PATTERN = re.compile(
    r"\b(?:available\s+upon\s+request|upon\s+reasonable\s+request"
    r"|available\s+from\s+the\s+(?:corresponding\s+)?author"
    r"|available\s+on\s+request)\b",
    re.IGNORECASE,
)


class BioMethodsChecker(Checker):
    """
    Checks bioinformatics methods sections for common completeness issues:
    - Software tools mentioned without version numbers
    - "Available upon request" data statements (rejected by most journals)
    - Sequencing data mentioned without accession numbers
    """

    name = "bio_methods"

    @cached_property
    def _data(self) -> dict:
        return _load_bio_tools()

    @cached_property
    def _tool_pattern(self) -> re.Pattern:
        tools = self._data.get("tools", [])
        # Sort longest first to avoid partial matches
        tools_sorted = sorted(set(tools), key=len, reverse=True)
        escaped = [re.escape(t) for t in tools_sorted]
        return re.compile(r"\b(?:" + "|".join(escaped) + r")\b")

    def check(self, text: str, context: DocumentContext) -> list[Finding]:
        findings: list[Finding] = []
        findings.extend(self._check_data_availability(text))
        # Tool version and accession checks are most relevant in Methods
        if context.section_type in (SectionType.METHODS, SectionType.UNKNOWN):
            findings.extend(self._check_tool_versions(text))
            findings.extend(self._check_accession_numbers(text))
        return findings

    def _check_data_availability(self, text: str) -> list[Finding]:
        """Flag 'available upon request' -- rejected by eLife, PLOS, Genome Biology."""
        findings: list[Finding] = []
        for match in _DATA_UNAVAILABLE_PATTERN.finditer(text):
            ctx_start = max(0, match.start() - 40)
            ctx_end = min(len(text), match.end() + 40)
            ctx = "..." + text[ctx_start:ctx_end].replace("\n", " ") + "..."
            findings.append(Finding(
                checker=self.name,
                rule_id="data_unavailable",
                text=match.group(),
                message=(
                    '"Available upon request" violates data availability policies '
                    "at eLife, PLOS Biology, Genome Biology, and many others."
                ),
                severity=Severity.HIGH,
                alternative="Deposit data in Dryad, Zenodo, or SRA and provide accession number",
                context=ctx,
            ))
        return findings

    def _check_tool_versions(self, text: str) -> list[Finding]:
        """Flag known bioinformatics tools used without a version number anywhere.

        A tool is only flagged if NONE of its mentions has an adjacent version. This
        avoids false positives when a tool is first named bare ("bedtools flank")
        but versioned elsewhere in the section ("Bedtools version 2.31").
        """
        # Group every mention of each tool by name, in document order. Tool detection
        # is case-sensitive (so "STAR" the aligner is not "star" the word).
        mentions: dict[str, list[re.Match]] = {}
        for match in self._tool_pattern.finditer(text):
            mentions.setdefault(match.group().lower(), []).append(match)

        findings: list[Finding] = []
        for tool_lower, matches in mentions.items():
            # Versioned if ANY occurrence of the tool name has a version within +-60
            # chars. The version sweep is case-insensitive so a sentence-case mention
            # ("Bedtools version 2.31") counts for lowercase usages ("bedtools flank").
            # This only ever suppresses a finding, so the relaxed match is safe.
            versioned = any(
                _VERSION_PATTERN.search(
                    text[max(0, m.start() - 60):min(len(text), m.end() + 60)]
                )
                for m in re.finditer(r"\b" + re.escape(tool_lower) + r"\b", text, re.IGNORECASE)
            )
            if versioned:
                continue

            first = matches[0]
            tool = first.group()
            ctx_start = max(0, first.start() - 40)
            ctx_end = min(len(text), first.end() + 40)
            ctx = "..." + text[ctx_start:ctx_end].replace("\n", " ") + "..."
            findings.append(Finding(
                checker=self.name,
                rule_id="tool_no_version",
                text=tool,
                message=(
                    f'"{tool}" is mentioned without a version number. '
                    "Methods sections should specify versions for reproducibility."
                ),
                severity=Severity.MEDIUM,
                alternative=f'Add version, e.g. "{tool} v2.3.1"',
                context=ctx,
            ))

        return findings

    def _check_accession_numbers(self, text: str) -> list[Finding]:
        """Flag sequencing data mentions without nearby accession numbers."""
        sequencing_terms = self._data.get("sequencing_terms", [])
        if not sequencing_terms:
            return []

        # Build regex patterns for known accession formats
        accession_patterns = [
            re.compile(pat) for pat in [
                r"\bSRR\d+\b", r"\bSRP\d+\b", r"\bSRS\d+\b", r"\bSRX\d+\b",
                r"\bERR\d+\b", r"\bERP\d+\b",
                r"\bPRJ[A-Z]{2}\d+\b", r"\bSAM[A-Z]{1,2}\d+\b",
                r"\bGSE\d+\b", r"\bGSM\d+\b",
                r"10\.5061/dryad\.[a-z0-9]+",
                r"10\.5281/zenodo\.\d+",
                r"\b[A-Z]{1,2}\d{5,8}\b",  # GenBank
            ]
        ]

        seq_term_pattern = re.compile(
            r"\b(?:" + "|".join(re.escape(t) for t in sequencing_terms) + r")\b",
            re.IGNORECASE,
        )

        findings: list[Finding] = []
        accession_present = any(pat.search(text) for pat in accession_patterns)

        # Only emit one finding per document for missing accessions
        if seq_term_pattern.search(text) and not accession_present:
            findings.append(Finding(
                checker=self.name,
                rule_id="missing_accession",
                text="sequencing data",
                message=(
                    "Sequencing data is mentioned but no repository accession number "
                    "(SRA, ENA, GEO, Dryad, Zenodo) was found in this section."
                ),
                severity=Severity.MEDIUM,
                alternative="Add accession number, e.g. 'Data deposited at NCBI SRA (SRP123456)'",
                context=None,
            ))

        return findings
