"""Tests for prose_check._models."""
from prose_check._models import (
    CheckResult, DocumentContext, Finding, Severity, SectionType, StudyType,
)


class TestSeverityEnum:
    def test_values(self):
        assert Severity.HIGH.value == "high"
        assert Severity.MEDIUM.value == "medium"
        assert Severity.LOW.value == "low"

    def test_str_comparison(self):
        assert Severity.HIGH == "high"


class TestSectionTypeEnum:
    def test_all_values_exist(self):
        for name in ("introduction", "methods", "results", "discussion", "abstract", "unknown"):
            assert SectionType(name) is not None

    def test_unknown_is_default(self):
        ctx = DocumentContext()
        assert ctx.section_type == SectionType.UNKNOWN


class TestDocumentContext:
    def test_defaults(self):
        ctx = DocumentContext()
        assert ctx.section_type == SectionType.UNKNOWN
        assert ctx.study_type == StudyType.UNKNOWN
        assert ctx.journal is None
        assert ctx.technical is True

    def test_custom_values(self):
        ctx = DocumentContext(
            section_type=SectionType.RESULTS,
            study_type=StudyType.OBSERVATIONAL,
            journal="molecular_ecology",
            technical=False,
        )
        assert ctx.section_type == SectionType.RESULTS
        assert ctx.study_type == StudyType.OBSERVATIONAL
        assert ctx.journal == "molecular_ecology"
        assert ctx.technical is False


class TestFinding:
    def test_required_fields(self):
        f = Finding(
            checker="ai_patterns",
            rule_id="llm_word_delve",
            text="delve",
            message="AI word",
            severity=Severity.HIGH,
        )
        assert f.checker == "ai_patterns"
        assert f.rule_id == "llm_word_delve"
        assert f.text == "delve"
        assert f.severity == Severity.HIGH
        assert f.alternative is None
        assert f.context is None

    def test_optional_fields(self):
        f = Finding(
            checker="test",
            rule_id="test_rule",
            text="word",
            message="msg",
            severity=Severity.MEDIUM,
            alternative="better word",
            context="...surrounding text...",
        )
        assert f.alternative == "better word"
        assert f.context == "...surrounding text..."


class TestCheckResult:
    def _make_result(self):
        findings = [
            Finding("a", "r1", "t1", "m", Severity.HIGH),
            Finding("a", "r2", "t2", "m", Severity.MEDIUM),
            Finding("a", "r3", "t3", "m", Severity.LOW),
            Finding("b", "r4", "t4", "m", Severity.HIGH),
        ]
        return CheckResult(
            findings=findings, score=50, word_count=100,
            section_type=SectionType.UNKNOWN,
        )

    def test_high_property(self):
        result = self._make_result()
        assert len(result.high) == 2
        assert all(f.severity == Severity.HIGH for f in result.high)

    def test_medium_property(self):
        result = self._make_result()
        assert len(result.medium) == 1

    def test_low_property(self):
        result = self._make_result()
        assert len(result.low) == 1

    def test_by_checker(self):
        result = self._make_result()
        assert len(result.by_checker("a")) == 3
        assert len(result.by_checker("b")) == 1
        assert len(result.by_checker("nonexistent")) == 0
