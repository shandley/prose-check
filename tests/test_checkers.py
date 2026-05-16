"""Tests for prose_check checkers and public API."""
import pytest
from prose_check import check_text, DocumentContext, Severity, SectionType, StudyType
from prose_check.checkers.ai_patterns import AIPatternChecker
from prose_check.checkers.stat_phrases import StatPhraseChecker
from prose_check.checkers.causal_lang import CausalLangChecker
from prose_check.checkers.structure import StructureChecker
from prose_check.checkers.bio_methods import BioMethodsChecker


# -- Fixtures ------------------------------------------------------------------

@pytest.fixture
def default_ctx():
    return DocumentContext()

@pytest.fixture
def results_observational():
    return DocumentContext(
        section_type=SectionType.RESULTS,
        study_type=StudyType.OBSERVATIONAL,
    )

@pytest.fixture
def methods_ctx():
    return DocumentContext(section_type=SectionType.METHODS)

@pytest.fixture
def ai_text():
    return (
        "This comprehensive guide provides a robust framework. "
        "Furthermore, it is important to note that a nuanced approach "
        "is pivotal for seamlessly leveraging these paradigms."
    )

@pytest.fixture
def clean_text():
    return (
        "The bookshop on Market Street had been there for forty years. "
        "Mrs. Chen opened it the same year her daughter was born. "
        "The smell of old pages mixed with the tea she kept brewing."
    )


# -- check_text() public API ---------------------------------------------------

class TestCheckText:
    def test_returns_check_result(self, ai_text, default_ctx):
        from prose_check import CheckResult
        result = check_text(ai_text, default_ctx)
        assert isinstance(result, CheckResult)

    def test_ai_text_scores_low(self, ai_text):
        result = check_text(ai_text)
        assert result.score < 80

    def test_clean_text_scores_high(self, clean_text):
        result = check_text(clean_text)
        assert result.score >= 80

    def test_empty_text_returns_100(self):
        result = check_text("")
        assert result.score == 100
        assert result.findings == []

    def test_word_count(self, ai_text):
        result = check_text(ai_text)
        assert result.word_count == len(ai_text.split())

    def test_specific_checkers(self, ai_text):
        result_all = check_text(ai_text)
        result_one = check_text(ai_text, checkers=["ai_patterns"])
        # Running only one checker should produce <= findings as running all
        assert len(result_one.findings) <= len(result_all.findings)

    def test_section_type_propagated(self):
        ctx = DocumentContext(section_type=SectionType.METHODS)
        result = check_text("Some text.", ctx)
        assert result.section_type == SectionType.METHODS


# -- AIPatternChecker ----------------------------------------------------------

class TestAIPatternChecker:
    def test_flags_llm_words(self, default_ctx):
        checker = AIPatternChecker()
        findings = checker.check("This is a comprehensive and robust solution.", default_ctx)
        texts = [f.text.lower() for f in findings]
        assert "comprehensive" in texts
        assert "robust" in texts

    def test_technical_mode_suppresses_tech_terms(self):
        checker = AIPatternChecker()
        tech_ctx = DocumentContext(technical=True)
        strict_ctx = DocumentContext(technical=False)
        text = "The Python API uses TypeScript for the frontend."
        tech_findings = checker.check(text, tech_ctx)
        strict_findings = checker.check(text, strict_ctx)
        assert len(tech_findings) <= len(strict_findings)

    def test_em_dash_flagged(self, default_ctx):
        checker = AIPatternChecker()
        findings = checker.check(
            "This is important — very important — especially now — and later.", default_ctx
        )
        rule_ids = [f.rule_id for f in findings]
        assert "em_dash_overuse" in rule_ids

    def test_clean_text_no_high_findings(self, clean_text, default_ctx):
        checker = AIPatternChecker()
        findings = checker.check(clean_text, default_ctx)
        high = [f for f in findings if f.severity == Severity.HIGH]
        assert len(high) == 0

    def test_findings_have_alternatives(self, default_ctx):
        checker = AIPatternChecker()
        # Use words that are in ALTERNATIVES; exclude "Let's" which is flagged but has no alt
        findings = checker.check("Please delve into this comprehensive framework.", default_ctx)
        ai_findings = [f for f in findings if f.rule_id.startswith("marker_")]
        # Filter to only findings that have an alternative (not all markers do)
        flagged_with_alts = [f for f in ai_findings if f.text.lower() in ("delve", "comprehensive")]
        assert len(flagged_with_alts) > 0
        assert all(f.alternative is not None for f in flagged_with_alts)


# -- StatPhraseChecker ---------------------------------------------------------

class TestStatPhraseChecker:
    def test_flags_marginally_significant(self, default_ctx):
        checker = StatPhraseChecker()
        findings = checker.check(
            "The effect was marginally significant in both groups.", default_ctx
        )
        assert any(f.rule_id == "marginal_sig" for f in findings)
        assert any(f.severity == Severity.HIGH for f in findings)

    def test_flags_all_but_significant(self, default_ctx):
        checker = StatPhraseChecker()
        findings = checker.check("Results were all but significant.", default_ctx)
        assert any(f.rule_id == "marginal_sig" for f in findings)

    def test_threshold_pvalue_in_results(self):
        checker = StatPhraseChecker()
        ctx = DocumentContext(section_type=SectionType.RESULTS)
        findings = checker.check("The association was significant (p < 0.05).", ctx)
        assert any(f.rule_id == "threshold_pvalue" for f in findings)

    def test_threshold_pvalue_not_in_methods(self):
        checker = StatPhraseChecker()
        ctx = DocumentContext(section_type=SectionType.METHODS)
        findings = checker.check("We set the significance threshold to p < 0.05.", ctx)
        # Should not flag a threshold definition in Methods
        threshold_findings = [f for f in findings if f.rule_id == "threshold_pvalue"]
        assert len(threshold_findings) == 0

    def test_clean_stats_no_findings(self, default_ctx):
        checker = StatPhraseChecker()
        findings = checker.check(
            "The association was significant (p = 0.032, OR = 1.45, 95% CI [1.12, 1.88]).",
            default_ctx,
        )
        # Exact p-value present -- binary_sig should not fire
        assert not any(f.rule_id == "binary_sig" for f in findings)


# -- CausalLangChecker ---------------------------------------------------------

class TestCausalLangChecker:
    def test_flags_causal_verb_in_results_observational(self, results_observational):
        checker = CausalLangChecker()
        findings = checker.check(
            "Temperature drives species richness across latitudes.",
            results_observational,
        )
        assert any(f.rule_id == "causal_verb" for f in findings)

    def test_no_findings_in_methods(self):
        checker = CausalLangChecker()
        ctx = DocumentContext(section_type=SectionType.METHODS)
        findings = checker.check(
            "Temperature drives species richness across latitudes.", ctx
        )
        assert findings == []

    def test_no_findings_for_experimental(self):
        checker = CausalLangChecker()
        ctx = DocumentContext(
            section_type=SectionType.RESULTS,
            study_type=StudyType.EXPERIMENTAL,
        )
        findings = checker.check(
            "The treatment causes an increase in expression.", ctx
        )
        assert findings == []

    def test_suggests_associational_alternative(self, results_observational):
        checker = CausalLangChecker()
        findings = checker.check("The gene drives adaptation.", results_observational)
        causal = [f for f in findings if f.rule_id == "causal_verb"]
        assert all(f.alternative is not None for f in causal)

    def test_no_findings_for_associational_language(self, results_observational):
        checker = CausalLangChecker()
        findings = checker.check(
            "Temperature is associated with species richness.", results_observational
        )
        assert findings == []


# -- StructureChecker ----------------------------------------------------------

class TestStructureChecker:
    def test_flags_short_paragraphs(self, default_ctx):
        checker = StructureChecker()
        # Many 3-word paragraphs
        text = "\n\n".join(["Very short paragraph."] * 10)
        findings = checker.check(text, default_ctx)
        assert any(f.rule_id == "short_paragraphs" for f in findings)

    def test_no_flag_for_long_paragraphs(self, default_ctx):
        checker = StructureChecker()
        text = " ".join(["word"] * 200)  # single long paragraph
        findings = checker.check(text, default_ctx)
        assert not any(f.rule_id == "short_paragraphs" for f in findings)

    def test_flags_bullet_overuse(self, default_ctx):
        checker = StructureChecker()
        bullets = "\n".join([f"- Item {i}" for i in range(20)])
        findings = checker.check(bullets, default_ctx)
        assert any(f.rule_id == "bullet_overuse" for f in findings)

    def test_empty_text_no_findings(self, default_ctx):
        checker = StructureChecker()
        assert checker.check("", default_ctx) == []


# -- BioMethodsChecker ---------------------------------------------------------

class TestBioMethodsChecker:
    def test_flags_data_unavailable(self, default_ctx):
        checker = BioMethodsChecker()
        findings = checker.check(
            "Raw sequencing data are available upon request.", default_ctx
        )
        assert any(f.rule_id == "data_unavailable" for f in findings)
        assert any(f.severity == Severity.HIGH for f in findings)

    def test_flags_tool_without_version(self, methods_ctx):
        checker = BioMethodsChecker()
        findings = checker.check(
            "Reads were mapped using BWA to the reference genome.", methods_ctx
        )
        assert any(f.rule_id == "tool_no_version" for f in findings)

    def test_no_flag_when_version_present(self, methods_ctx):
        checker = BioMethodsChecker()
        findings = checker.check(
            "Reads were mapped using BWA v0.7.17 to the reference genome.", methods_ctx
        )
        version_findings = [f for f in findings if f.rule_id == "tool_no_version"]
        assert len(version_findings) == 0

    def test_flags_missing_accession(self, methods_ctx):
        checker = BioMethodsChecker()
        findings = checker.check(
            "RNA-seq data were generated from 20 samples.", methods_ctx
        )
        assert any(f.rule_id == "missing_accession" for f in findings)

    def test_no_accession_flag_when_present(self, methods_ctx):
        checker = BioMethodsChecker()
        findings = checker.check(
            "RNA-seq data were deposited in NCBI SRA (SRP123456).", methods_ctx
        )
        assert not any(f.rule_id == "missing_accession" for f in findings)

    def test_data_unavailable_fires_everywhere(self):
        checker = BioMethodsChecker()
        for section in (SectionType.RESULTS, SectionType.DISCUSSION, SectionType.INTRODUCTION):
            ctx = DocumentContext(section_type=section)
            findings = checker.check("Data available upon request.", ctx)
            assert any(f.rule_id == "data_unavailable" for f in findings), \
                f"Should fire in {section}"
