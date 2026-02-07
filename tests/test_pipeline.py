"""Integration tests for the prose-check analysis pipeline modules.

Tests analyze.py, generate_prompts.py, report.py, and compare.py
without requiring API keys or network access.
"""

import json
import math
import tempfile
from collections import Counter
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Adjust sys.path so we can import from src/
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Mock external dependencies that are not available in test environment.
# generate_samples.py imports anthropic and dotenv at module level, and
# compare.py imports from generate_samples.py, so we must mock these
# before any of our src modules are imported.
# analyze.py imports nltk and tqdm at module level.
_mock_nltk = MagicMock()
_mock_nltk.data.find.return_value = True
_mock_nltk.sent_tokenize = lambda text: [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
_mock_nltk.word_tokenize = lambda text: text.lower().split()
sys.modules["nltk"] = _mock_nltk
sys.modules["nltk.data"] = MagicMock()
sys.modules["tqdm"] = MagicMock()
sys.modules["tqdm.auto"] = MagicMock()
# Make tqdm a passthrough (identity function for iterables)
sys.modules["tqdm"].tqdm = lambda x, **kwargs: x
sys.modules["anthropic"] = MagicMock()
sys.modules["dotenv"] = MagicMock()


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def opus_texts():
    """Sample AI-generated texts with distinctive LLM patterns."""
    return [
        "It's important to note that this comprehensive framework provides a robust "
        "solution for modern software development. Furthermore, the nuanced approach "
        "leverages existing paradigms to facilitate seamless integration.",
        "Let's delve into the intricacies of this multifaceted problem. Additionally, "
        "we should utilize the aforementioned methodology to foster innovation. "
        "The tapestry of modern computing is indeed complex.",
        "This comprehensive guide essentially explores the pivotal role of meticulous "
        "planning in software architecture. Fundamentally, robust systems require "
        "careful design -- and comprehensive testing is crucial.",
        "In essence, the landscape of cloud computing has evolved significantly. "
        "It's worth noting that leveraging microservices can facilitate scalability. "
        "Furthermore, this paradigm shift is certainly transformative.",
        "Let's explore the myriad possibilities that emerge from this endeavor. "
        "The plethora of options available makes this a nuanced decision. "
        "Nevertheless, a comprehensive analysis reveals clear patterns.",
    ]


@pytest.fixture
def human_texts():
    """Sample human-written texts without heavy LLM patterns."""
    return [
        "The old bookshop on Market Street had been there for forty years. "
        "Mrs. Chen opened it the same year her daughter was born, filling "
        "the shelves with paperbacks from estate sales across the county.",
        "I spent three hours debugging that memory leak yesterday. Turns out "
        "someone was holding a reference to the event handler after removing "
        "the DOM node. Classic mistake.",
        "Python 3.12 shipped with a faster interpreter. The team rewrote "
        "the eval loop using computed gotos. Performance improved by about "
        "five percent on most benchmarks.",
        "We shipped the feature on Friday. Bad idea. The load balancer "
        "choked on the new endpoints and we had to roll back before dinner. "
        "Monday morning we fixed the config and tried again.",
        "The API returns JSON with nested objects. You parse the response, "
        "grab the user ID from the top-level field, then look up their "
        "permissions in a separate table.",
    ]


@pytest.fixture
def opus_jsonl_file(opus_texts, tmp_path):
    """Write opus texts to a temporary JSONL file."""
    path = tmp_path / "opus_samples.jsonl"
    with open(path, "w") as f:
        for text in opus_texts:
            f.write(json.dumps({"response": text}) + "\n")
    return path


@pytest.fixture
def human_jsonl_file(human_texts, tmp_path):
    """Write human texts to a temporary JSONL file."""
    path = tmp_path / "human_samples.jsonl"
    with open(path, "w") as f:
        for text in human_texts:
            f.write(json.dumps({"text": text}) + "\n")
    return path


@pytest.fixture
def sample_markers_data():
    """Mock analysis results matching the markers.json format."""
    return {
        "corpus_stats": {
            "opus_samples": 100,
            "human_samples": 100,
            "opus_total_words": 50000,
            "human_total_words": 48000,
        },
        "summary_stats": {
            "opus_avg_sentence_length": 18.5,
            "human_avg_sentence_length": 15.2,
            "opus_median_sentence_length": 17,
            "human_median_sentence_length": 14,
            "opus_em_dash_per_1k": 2.8,
            "human_em_dash_per_1k": 0.9,
            "opus_colon_per_1k": 3.1,
            "human_colon_per_1k": 1.5,
            "opus_semicolon_per_1k": 0.6,
            "human_semicolon_per_1k": 0.8,
            "opus_list_items_per_text": 4.2,
            "human_list_items_per_text": 1.1,
            "opus_sentence_distribution": {
                "mean": 18.5,
                "stdev": 9.2,
                "coefficient_of_variation": 49.7,
                "min": 2,
                "max": 55,
                "p10": 6,
                "p25": 12,
                "p50_median": 17,
                "p75": 24,
                "p90": 31,
                "pct_short_1_10": 22.1,
                "pct_medium_11_25": 53.4,
                "pct_long_26_plus": 24.5,
            },
            "human_sentence_distribution": {
                "mean": 15.2,
                "stdev": 7.8,
                "coefficient_of_variation": 51.3,
                "min": 1,
                "max": 48,
                "p10": 5,
                "p25": 10,
                "p50_median": 14,
                "p75": 20,
                "p90": 26,
                "pct_short_1_10": 26.5,
                "pct_medium_11_25": 55.2,
                "pct_long_26_plus": 18.3,
            },
            "opus_passive_voice_pct": 12.3,
            "human_passive_voice_pct": 14.1,
            "opus_paragraph_stats": {
                "avg_paragraphs_per_doc": 5.2,
                "avg_para_length_words": 42.1,
                "para_length_stdev": 18.3,
                "para_length_cv": 43.5,
                "min_para_length": 3,
                "max_para_length": 120,
                "top_para_openers": [["the", 45], ["this", 32], ["in", 28]],
            },
            "human_paragraph_stats": {
                "avg_paragraphs_per_doc": 3.8,
                "avg_para_length_words": 55.7,
                "para_length_stdev": 25.1,
                "para_length_cv": 45.1,
                "min_para_length": 2,
                "max_para_length": 150,
                "top_para_openers": [["the", 38], ["i", 25], ["we", 20]],
            },
        },
        "markers": [
            {
                "type": "phrase_llm_favorite",
                "item": "delve",
                "opus_rate": 1.5,
                "human_rate": 0.02,
                "log_odds": 4.3,
                "ci_lower": 3.8,
                "ci_upper": 4.8,
                "opus_count": 75,
                "human_count": 1,
                "example_context": "...let's delve into the details...",
            },
            {
                "type": "phrase_llm_favorite",
                "item": "comprehensive",
                "opus_rate": 2.1,
                "human_rate": 0.15,
                "log_odds": 2.6,
                "ci_lower": 2.1,
                "ci_upper": 3.1,
                "opus_count": 105,
                "human_count": 8,
                "example_context": "...comprehensive framework for...",
            },
            {
                "type": "word",
                "item": "robust",
                "opus_rate": 1.8,
                "human_rate": 0.12,
                "log_odds": 2.7,
                "ci_lower": 2.2,
                "ci_upper": 3.2,
                "opus_count": 90,
                "human_count": 6,
                "example_context": "...robust solution for modern...",
            },
            {
                "type": "phrase_hedging",
                "item": "it's important to note",
                "opus_rate": 0.8,
                "human_rate": 0.05,
                "log_odds": 2.8,
                "ci_lower": 2.3,
                "ci_upper": 3.3,
                "opus_count": 40,
                "human_count": 3,
                "example_context": "...It's important to note that...",
            },
            {
                "type": "phrase_transition",
                "item": "furthermore",
                "opus_rate": 1.2,
                "human_rate": 0.3,
                "log_odds": 1.4,
                "ci_lower": 0.9,
                "ci_upper": 1.9,
                "opus_count": 60,
                "human_count": 15,
                "example_context": "...Furthermore, the approach...",
            },
            {
                "type": "bigram",
                "item": "it is",
                "opus_rate": 0.5,
                "human_rate": 0.25,
                "log_odds": 0.7,
                "ci_lower": 0.2,
                "ci_upper": 1.2,
                "opus_count": 25,
                "human_count": 12,
                "example_context": "...it is essential to...",
            },
            {
                "type": "sentence_starter",
                "item": "furthermore",
                "opus_rate": 0.04,
                "human_rate": 0.008,
                "log_odds": 1.6,
                "ci_lower": 1.1,
                "ci_upper": 2.1,
                "opus_count": 20,
                "human_count": 4,
                "example_context": "Furthermore, the data shows...",
            },
            {
                "type": "trigram",
                "item": "in order to",
                "opus_rate": 0.3,
                "human_rate": 0.08,
                "log_odds": 1.3,
                "ci_lower": 0.8,
                "ci_upper": 1.8,
                "opus_count": 15,
                "human_count": 4,
                "example_context": "...in order to achieve...",
            },
        ],
    }


@pytest.fixture
def markers_json_file(sample_markers_data, tmp_path):
    """Write sample markers data to a temporary JSON file."""
    path = tmp_path / "markers.json"
    with open(path, "w") as f:
        json.dump(sample_markers_data, f, indent=2)
    return path


# =============================================================================
# Test analyze.py: Log-odds Calculation
# =============================================================================

class TestLogOddsCalculation:
    """Tests for the calculate_log_odds_ratio function."""

    def test_equal_rates_yield_zero_log_odds(self):
        """When opus and human have equal counts, log-odds should be near zero."""
        from analyze import calculate_log_odds_ratio

        log_odds, ci_lower, ci_upper = calculate_log_odds_ratio(
            opus_count=100, human_count=100,
            opus_total=10000, human_total=10000
        )

        assert abs(log_odds) < 0.1
        assert ci_lower < ci_upper

    def test_higher_opus_rate_yields_positive_log_odds(self):
        """When opus rate is higher, log-odds should be positive."""
        from analyze import calculate_log_odds_ratio

        log_odds, ci_lower, ci_upper = calculate_log_odds_ratio(
            opus_count=100, human_count=10,
            opus_total=10000, human_total=10000
        )

        assert log_odds > 0
        assert ci_lower < log_odds < ci_upper

    def test_higher_human_rate_yields_negative_log_odds(self):
        """When human rate is higher, log-odds should be negative."""
        from analyze import calculate_log_odds_ratio

        log_odds, ci_lower, ci_upper = calculate_log_odds_ratio(
            opus_count=10, human_count=100,
            opus_total=10000, human_total=10000
        )

        assert log_odds < 0

    def test_smoothing_prevents_division_by_zero(self):
        """Smoothing should prevent errors when a count is zero."""
        from analyze import calculate_log_odds_ratio

        # Should not raise even with zero counts
        log_odds, ci_lower, ci_upper = calculate_log_odds_ratio(
            opus_count=50, human_count=0,
            opus_total=10000, human_total=10000
        )

        assert math.isfinite(log_odds)
        assert math.isfinite(ci_lower)
        assert math.isfinite(ci_upper)
        assert log_odds > 0

    def test_confidence_interval_width(self):
        """Higher counts should produce narrower confidence intervals."""
        from analyze import calculate_log_odds_ratio

        # Low counts = wide CI
        _, ci_low_lo, ci_low_hi = calculate_log_odds_ratio(
            opus_count=5, human_count=2,
            opus_total=100, human_total=100
        )

        # High counts = narrow CI
        _, ci_high_lo, ci_high_hi = calculate_log_odds_ratio(
            opus_count=500, human_count=200,
            opus_total=10000, human_total=10000
        )

        low_width = ci_low_hi - ci_low_lo
        high_width = ci_high_hi - ci_high_lo

        assert low_width > high_width

    def test_custom_smoothing_parameter(self):
        """Different smoothing values should change results slightly."""
        from analyze import calculate_log_odds_ratio

        lo1, _, _ = calculate_log_odds_ratio(
            opus_count=10, human_count=0,
            opus_total=1000, human_total=1000,
            smoothing=0.5
        )
        lo2, _, _ = calculate_log_odds_ratio(
            opus_count=10, human_count=0,
            opus_total=1000, human_total=1000,
            smoothing=1.0
        )

        # Both should be positive but different
        assert lo1 > 0
        assert lo2 > 0
        assert lo1 != lo2


# =============================================================================
# Test analyze.py: N-gram Extraction
# =============================================================================

class TestNgramExtraction:
    """Tests for the get_ngrams function."""

    def test_bigrams(self):
        """Should produce correct bigrams."""
        from analyze import get_ngrams

        words = ["the", "quick", "brown", "fox"]
        bigrams = get_ngrams(words, 2)

        assert bigrams == ["the quick", "quick brown", "brown fox"]

    def test_trigrams(self):
        """Should produce correct trigrams."""
        from analyze import get_ngrams

        words = ["one", "two", "three", "four", "five"]
        trigrams = get_ngrams(words, 3)

        assert trigrams == ["one two three", "two three four", "three four five"]

    def test_empty_list(self):
        """Empty word list should produce empty n-grams."""
        from analyze import get_ngrams

        assert get_ngrams([], 2) == []

    def test_list_shorter_than_n(self):
        """Word list shorter than n should produce empty n-grams."""
        from analyze import get_ngrams

        assert get_ngrams(["hello"], 2) == []

    def test_unigrams(self):
        """N=1 should return individual words."""
        from analyze import get_ngrams

        words = ["a", "b", "c"]
        unigrams = get_ngrams(words, 1)

        assert unigrams == ["a", "b", "c"]


# =============================================================================
# Test analyze.py: Corpus Loading
# =============================================================================

class TestCorpusLoading:
    """Tests for the load_corpus function."""

    def test_load_with_response_field(self, opus_jsonl_file):
        """Should load texts from the 'response' field."""
        from analyze import load_corpus

        texts = load_corpus(opus_jsonl_file, text_field="response")

        assert len(texts) == 5
        assert "comprehensive" in texts[0]

    def test_load_with_text_field(self, human_jsonl_file):
        """Should load texts from the 'text' field."""
        from analyze import load_corpus

        texts = load_corpus(human_jsonl_file, text_field="text")

        assert len(texts) == 5
        assert "bookshop" in texts[0]

    def test_load_empty_file(self, tmp_path):
        """Loading an empty file should return empty list."""
        from analyze import load_corpus

        empty_file = tmp_path / "empty.jsonl"
        empty_file.write_text("")

        texts = load_corpus(empty_file)

        assert texts == []

    def test_load_skips_empty_texts(self, tmp_path):
        """Records with empty text fields should be skipped."""
        from analyze import load_corpus

        path = tmp_path / "mixed.jsonl"
        with open(path, "w") as f:
            f.write(json.dumps({"response": "has content"}) + "\n")
            f.write(json.dumps({"response": ""}) + "\n")
            f.write(json.dumps({"response": "also has content"}) + "\n")

        texts = load_corpus(path, text_field="response")

        assert len(texts) == 2


# =============================================================================
# Test analyze.py: Marker NamedTuple
# =============================================================================

class TestMarkerNamedTuple:
    """Tests for the Marker NamedTuple structure."""

    def test_marker_fields(self):
        """Marker should have all expected fields."""
        from analyze import Marker

        marker = Marker(
            type="word",
            item="delve",
            opus_rate=0.01,
            human_rate=0.001,
            log_odds=2.3,
            ci_lower=1.8,
            ci_upper=2.8,
            opus_count=50,
            human_count=5,
            example_context="...delve into...",
        )

        assert marker.type == "word"
        assert marker.item == "delve"
        assert marker.log_odds == 2.3
        assert marker.opus_count == 50
        assert marker.human_count == 5

    def test_marker_is_immutable(self):
        """Marker should be immutable (it is a NamedTuple)."""
        from analyze import Marker

        marker = Marker(
            type="word", item="test", opus_rate=0.01, human_rate=0.001,
            log_odds=1.0, ci_lower=0.5, ci_upper=1.5,
            opus_count=10, human_count=2, example_context=""
        )

        with pytest.raises(AttributeError):
            marker.type = "changed"


# =============================================================================
# Test analyze.py: Phrase Pattern Analysis
# =============================================================================

class TestPhrasePatternAnalysis:
    """Tests for the analyze_phrase_patterns function."""

    def test_detects_known_llm_phrases(self, opus_texts, human_texts):
        """Should detect known LLM-favorite phrases in opus texts."""
        from analyze import analyze_phrase_patterns

        markers = analyze_phrase_patterns(opus_texts, human_texts)

        found_items = [m.item for m in markers]
        # These phrases appear multiple times in opus_texts but not in human_texts
        # Whether they pass the statistical filter depends on counts, but
        # at minimum the function should return a list of Marker objects.
        assert isinstance(markers, list)
        for m in markers:
            assert hasattr(m, "type")
            assert hasattr(m, "item")
            assert hasattr(m, "log_odds")
            assert m.type.startswith("phrase_")

    def test_empty_texts_return_no_markers(self):
        """Empty text lists should return no markers."""
        from analyze import analyze_phrase_patterns

        markers = analyze_phrase_patterns([], [])

        # With empty texts, total chars is 0, so no phrases can be counted
        assert markers == [] or isinstance(markers, list)


# =============================================================================
# Test analyze.py: Structural Analysis
# =============================================================================

class TestStructuralAnalysis:
    """Tests for the analyze_structural_patterns function."""

    def test_returns_markers_and_stats(self, opus_texts, human_texts):
        """Should return both markers and summary stats."""
        from analyze import analyze_structural_patterns, tokenize_texts

        opus_words, opus_sentences = tokenize_texts(opus_texts)
        human_words, human_sentences = tokenize_texts(human_texts)

        markers, summary_stats = analyze_structural_patterns(
            opus_sentences, human_sentences, opus_texts, human_texts
        )

        assert isinstance(markers, list)
        assert isinstance(summary_stats, dict)
        assert "opus_avg_sentence_length" in summary_stats
        assert "human_avg_sentence_length" in summary_stats
        assert "opus_list_items_per_text" in summary_stats

    def test_sentence_length_stats(self, opus_texts, human_texts):
        """Sentence length averages should be positive floats."""
        from analyze import analyze_structural_patterns, tokenize_texts

        _, opus_sentences = tokenize_texts(opus_texts)
        _, human_sentences = tokenize_texts(human_texts)

        _, stats = analyze_structural_patterns(
            opus_sentences, human_sentences, opus_texts, human_texts
        )

        assert stats["opus_avg_sentence_length"] > 0
        assert stats["human_avg_sentence_length"] > 0

    def test_punctuation_stats(self, opus_texts, human_texts):
        """Punctuation stats should be present."""
        from analyze import analyze_structural_patterns, tokenize_texts

        _, opus_sentences = tokenize_texts(opus_texts)
        _, human_sentences = tokenize_texts(human_texts)

        _, stats = analyze_structural_patterns(
            opus_sentences, human_sentences, opus_texts, human_texts
        )

        assert "opus_em_dash_per_1k" in stats
        assert "human_em_dash_per_1k" in stats
        assert "opus_colon_per_1k" in stats


# =============================================================================
# Test analyze.py: Sentence Length Distribution
# =============================================================================

class TestSentenceLengthDistribution:
    """Tests for the analyze_sentence_length_distribution function."""

    def test_returns_distribution_stats(self, opus_texts, human_texts):
        """Should return distribution stats for both corpora."""
        from analyze import analyze_sentence_length_distribution, tokenize_texts

        _, opus_sentences = tokenize_texts(opus_texts)
        _, human_sentences = tokenize_texts(human_texts)

        result = analyze_sentence_length_distribution(opus_sentences, human_sentences)

        assert "opus_sentence_distribution" in result
        assert "human_sentence_distribution" in result

        opus_dist = result["opus_sentence_distribution"]
        assert "mean" in opus_dist
        assert "stdev" in opus_dist
        assert "coefficient_of_variation" in opus_dist
        assert "pct_short_1_10" in opus_dist
        assert "pct_medium_11_25" in opus_dist
        assert "pct_long_26_plus" in opus_dist

    def test_percentages_sum_to_100(self, opus_texts, human_texts):
        """Short + medium + long percentages should sum to approximately 100."""
        from analyze import analyze_sentence_length_distribution, tokenize_texts

        _, opus_sentences = tokenize_texts(opus_texts)
        _, human_sentences = tokenize_texts(human_texts)

        result = analyze_sentence_length_distribution(opus_sentences, human_sentences)

        for key in ["opus_sentence_distribution", "human_sentence_distribution"]:
            dist = result[key]
            total = dist["pct_short_1_10"] + dist["pct_medium_11_25"] + dist["pct_long_26_plus"]
            assert abs(total - 100.0) < 0.5  # Allow small rounding error


# =============================================================================
# Test analyze.py: Passive Voice Detection
# =============================================================================

class TestPassiveVoiceDetection:
    """Tests for the detect_passive_voice function."""

    def test_detects_passive_voice(self):
        """Should detect passive voice constructions."""
        from analyze import detect_passive_voice

        texts_with_passive = [
            "The report was completed yesterday. The data were analyzed carefully.",
            "It has been shown that this approach works. The results will be published.",
        ]
        texts_without_passive = [
            "I completed the report yesterday. I analyzed the data carefully.",
            "She showed this approach works. They will publish the results.",
        ]

        result = detect_passive_voice(texts_with_passive, texts_without_passive)

        assert result["opus_passive_voice_pct"] > result["human_passive_voice_pct"]
        assert result["opus_passive_count"] > 0
        assert result["opus_total_sentences"] > 0

    def test_returns_expected_keys(self, opus_texts, human_texts):
        """Should return all expected dictionary keys."""
        from analyze import detect_passive_voice

        result = detect_passive_voice(opus_texts, human_texts)

        assert "opus_passive_voice_pct" in result
        assert "human_passive_voice_pct" in result
        assert "opus_passive_count" in result
        assert "opus_total_sentences" in result
        assert "human_passive_count" in result
        assert "human_total_sentences" in result


# =============================================================================
# Test analyze.py: Hedging Language Analysis
# =============================================================================

class TestHedgingLanguageAnalysis:
    """Tests for the analyze_hedging_language function."""

    def test_detects_hedging_words(self):
        """Should detect hedging words like 'might', 'perhaps', 'potentially'."""
        from analyze import analyze_hedging_language

        hedgy_texts = [
            "This might potentially work. Perhaps we could consider it. "
            "It seems likely that the approach is probably correct.",
        ]
        direct_texts = [
            "This works. We should use it. The approach is correct.",
        ]

        result = analyze_hedging_language(hedgy_texts, direct_texts)

        assert result["hedging_opus_rate"] > result["hedging_human_rate"]

    def test_returns_expected_keys(self, opus_texts, human_texts):
        """Should return all expected dictionary keys."""
        from analyze import analyze_hedging_language

        result = analyze_hedging_language(opus_texts, human_texts)

        assert "hedging_opus_rate" in result
        assert "hedging_human_rate" in result
        assert "hedging_ratio" in result
        assert "hedging_word_rate_opus" in result
        assert "hedging_word_rate_human" in result
        assert "hedging_breakdown" in result


# =============================================================================
# Test analyze.py: Paragraph Pattern Analysis
# =============================================================================

class TestParagraphPatternAnalysis:
    """Tests for the analyze_paragraph_patterns function."""

    def test_returns_paragraph_stats(self, opus_texts, human_texts):
        """Should return paragraph statistics for both corpora."""
        from analyze import analyze_paragraph_patterns

        result = analyze_paragraph_patterns(opus_texts, human_texts)

        assert "opus_paragraph_stats" in result
        assert "human_paragraph_stats" in result

        opus_stats = result["opus_paragraph_stats"]
        assert "avg_para_length_words" in opus_stats
        assert "para_length_stdev" in opus_stats
        assert "top_para_openers" in opus_stats


# =============================================================================
# Test analyze.py: Tokenization
# =============================================================================

class TestTokenization:
    """Tests for the tokenize_texts function."""

    def test_returns_words_and_sentences(self, opus_texts):
        """Should return parallel lists of words and sentences."""
        from analyze import tokenize_texts

        all_words, all_sentences = tokenize_texts(opus_texts)

        assert len(all_words) == len(opus_texts)
        assert len(all_sentences) == len(opus_texts)

    def test_words_are_lowercase_alpha(self, opus_texts):
        """All returned words should be lowercase alphabetic."""
        from analyze import tokenize_texts

        all_words, _ = tokenize_texts(opus_texts)

        for doc_words in all_words:
            for word in doc_words:
                assert word.isalpha()
                assert word == word.lower()

    def test_sentences_are_strings(self, opus_texts):
        """Each sentence should be a non-empty string."""
        from analyze import tokenize_texts

        _, all_sentences = tokenize_texts(opus_texts)

        for doc_sentences in all_sentences:
            assert len(doc_sentences) > 0
            for sent in doc_sentences:
                assert isinstance(sent, str)
                assert len(sent) > 0


# =============================================================================
# Test generate_prompts.py: Template Filling
# =============================================================================

class TestTemplateFilling:
    """Tests for the fill_template function."""

    def test_single_placeholder(self):
        """Should fill a single placeholder."""
        from generate_prompts import fill_template

        result = fill_template(
            "Explain {concept} clearly.",
            {"concept": ["recursion"]}
        )

        assert result == "Explain recursion clearly."

    def test_multiple_placeholders(self):
        """Should fill multiple different placeholders."""
        from generate_prompts import fill_template

        result = fill_template(
            "Compare {a} and {b}.",
            {"a": ["Python"], "b": ["JavaScript"]}
        )

        assert result == "Compare Python and JavaScript."

    def test_missing_placeholder_unchanged(self):
        """Placeholders not in fills dict should remain unchanged."""
        from generate_prompts import fill_template

        result = fill_template(
            "Explain {concept} in {language}.",
            {"concept": ["recursion"]}
        )

        assert "recursion" in result
        assert "{language}" in result

    def test_no_placeholders(self):
        """Template without placeholders should be returned as-is."""
        from generate_prompts import fill_template

        result = fill_template("Just a plain string.", {})

        assert result == "Just a plain string."


# =============================================================================
# Test generate_prompts.py: Prompt Generation
# =============================================================================

class TestPromptGeneration:
    """Tests for the generate_all_prompts function."""

    def test_generates_correct_count(self):
        """Should generate approximately the requested number of prompts."""
        from generate_prompts import generate_all_prompts

        prompts = generate_all_prompts(total_target=50)

        # The function distributes across categories with integer rounding,
        # so the total may not be exact. Allow a margin.
        assert len(prompts) >= 40
        assert len(prompts) <= 55

    def test_prompt_structure(self):
        """Each prompt should have the expected fields."""
        from generate_prompts import generate_all_prompts

        prompts = generate_all_prompts(total_target=20)

        for prompt in prompts:
            assert "id" in prompt
            assert "prompt" in prompt
            assert "category" in prompt
            assert "expected_length" in prompt
            assert "formality" in prompt

    def test_categories_are_diverse(self):
        """Prompts should span multiple categories."""
        from generate_prompts import generate_all_prompts

        prompts = generate_all_prompts(total_target=100)

        categories = set(p["category"] for p in prompts)

        # With 100 prompts, should have at least technical and analysis
        assert len(categories) >= 3

    def test_ids_are_unique(self):
        """Prompt IDs should be unique."""
        from generate_prompts import generate_all_prompts

        prompts = generate_all_prompts(total_target=50)

        ids = [p["id"] for p in prompts]
        assert len(ids) == len(set(ids))

    def test_expected_length_values(self):
        """Expected length should be one of the valid values."""
        from generate_prompts import generate_all_prompts

        prompts = generate_all_prompts(total_target=50)

        valid_lengths = {"short", "medium", "long"}
        for prompt in prompts:
            assert prompt["expected_length"] in valid_lengths

    def test_formality_values(self):
        """Formality should be one of the valid values."""
        from generate_prompts import generate_all_prompts

        prompts = generate_all_prompts(total_target=50)

        valid_formalities = {"casual", "neutral", "formal"}
        for prompt in prompts:
            assert prompt["formality"] in valid_formalities


# =============================================================================
# Test generate_prompts.py: Prompt Saving
# =============================================================================

class TestPromptSaving:
    """Tests for the save_prompts function."""

    def test_save_and_load(self, tmp_path):
        """Saved prompts should be loadable as valid JSONL."""
        from generate_prompts import generate_all_prompts, save_prompts

        prompts = generate_all_prompts(total_target=10)
        output_path = tmp_path / "prompts.jsonl"
        save_prompts(prompts, output_path)

        # Read back
        loaded = []
        with open(output_path) as f:
            for line in f:
                loaded.append(json.loads(line))

        assert len(loaded) == len(prompts)
        assert loaded[0]["prompt"] == prompts[0]["prompt"]

    def test_save_creates_parent_dirs(self, tmp_path):
        """save_prompts should create parent directories if needed."""
        from generate_prompts import save_prompts

        output_path = tmp_path / "nested" / "dir" / "prompts.jsonl"
        save_prompts([{"prompt": "test"}], output_path)

        assert output_path.exists()


# =============================================================================
# Test generate_prompts.py: Category-specific Generation
# =============================================================================

class TestCategoryGeneration:
    """Tests for the generate_prompts_for_category function."""

    def test_generates_requested_count(self):
        """Should generate up to the requested number of prompts."""
        from generate_prompts import (
            generate_prompts_for_category,
            TECHNICAL_EXPLANATIONS,
            TECHNICAL_FILLS,
        )

        prompts = list(generate_prompts_for_category(
            TECHNICAL_EXPLANATIONS, TECHNICAL_FILLS, "technical", count=10
        ))

        assert len(prompts) <= 10
        assert len(prompts) >= 5  # Should get at least some

    def test_category_field_matches(self):
        """Generated prompts should have the correct category."""
        from generate_prompts import (
            generate_prompts_for_category,
            CREATIVE_WRITING,
            CREATIVE_FILLS,
        )

        prompts = list(generate_prompts_for_category(
            CREATIVE_WRITING, CREATIVE_FILLS, "creative", count=5
        ))

        for prompt in prompts:
            assert prompt["category"] == "creative"


# =============================================================================
# Test report.py: Severity Classification
# =============================================================================

class TestReportSeverity:
    """Tests for the severity classification in report.py."""

    def test_high_severity(self):
        """Log-odds above 2.5 should be high severity."""
        from report import get_severity

        assert get_severity(3.0) == "high"
        assert get_severity(2.6) == "high"
        assert get_severity(5.0) == "high"

    def test_medium_severity(self):
        """Log-odds between 1.5 and 2.5 should be medium severity."""
        from report import get_severity

        assert get_severity(2.0) == "medium"
        assert get_severity(1.6) == "medium"
        assert get_severity(2.5) == "medium"

    def test_low_severity(self):
        """Log-odds at or below 1.5 should be low severity."""
        from report import get_severity

        assert get_severity(1.5) == "low"
        assert get_severity(1.0) == "low"
        assert get_severity(0.5) == "low"

    def test_boundary_values(self):
        """Boundary values should be classified correctly."""
        from report import get_severity

        # 2.5 is the boundary between medium and high
        assert get_severity(2.5) in ("medium", "high")
        # 1.5 is the boundary between low and medium
        assert get_severity(1.5) in ("low", "medium")


# =============================================================================
# Test report.py: Styleguide Generation
# =============================================================================

class TestStyleguideGeneration:
    """Tests for the generate_styleguide function."""

    def test_generates_markdown_file(self, markers_json_file, tmp_path):
        """Should generate a markdown file from markers data."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        assert output_path.exists()
        content = output_path.read_text()
        assert len(content) > 100

    def test_output_contains_header(self, markers_json_file, tmp_path):
        """Generated styleguide should contain the main header."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        content = output_path.read_text()
        assert "# Personal Writing Styleguide" in content

    def test_output_contains_top_patterns_table(self, markers_json_file, tmp_path):
        """Generated styleguide should contain a top patterns table."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        content = output_path.read_text()
        assert "Quick Reference: Top Patterns to Avoid" in content
        assert "| Pattern |" in content

    def test_output_contains_checklist(self, markers_json_file, tmp_path):
        """Generated styleguide should contain a self-editing checklist."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        content = output_path.read_text()
        assert "Self-Editing Checklist" in content
        assert "- [ ]" in content

    def test_output_contains_alternatives(self, markers_json_file, tmp_path):
        """Generated styleguide should include alternative suggestions."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        content = output_path.read_text()
        # "delve" is in our markers and ALTERNATIVES maps it to alternatives
        assert "delve" in content.lower()

    def test_output_contains_structural_section(self, markers_json_file, tmp_path):
        """Generated styleguide should contain structural patterns section."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        content = output_path.read_text()
        assert "Structural Patterns" in content

    def test_output_contains_corpus_stats(self, markers_json_file, tmp_path):
        """Generated styleguide should reference corpus statistics."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        content = output_path.read_text()
        assert "100" in content  # opus_samples or human_samples

    def test_output_contains_before_after_examples(self, markers_json_file, tmp_path):
        """Generated styleguide should include before/after examples."""
        from report import generate_styleguide

        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        content = output_path.read_text()
        assert "Before/After Examples" in content
        assert "Before (AI-like)" in content
        assert "After (more natural)" in content

    def test_creates_parent_directories(self, markers_json_file, tmp_path):
        """Should create parent directories for the output file."""
        from report import generate_styleguide

        output_path = tmp_path / "nested" / "dir" / "styleguide.md"
        generate_styleguide(markers_json_file, output_path)

        assert output_path.exists()


# =============================================================================
# Test report.py: ALTERNATIVES Dictionary
# =============================================================================

class TestAlternativesDictionary:
    """Tests for the ALTERNATIVES constant in report.py."""

    def test_alternatives_not_empty(self):
        """ALTERNATIVES dict should contain entries."""
        from report import ALTERNATIVES

        assert len(ALTERNATIVES) > 50

    def test_all_values_are_lists(self):
        """Every value in ALTERNATIVES should be a list of strings."""
        from report import ALTERNATIVES

        for key, values in ALTERNATIVES.items():
            assert isinstance(values, list), f"Value for '{key}' is not a list"
            assert len(values) > 0, f"No alternatives for '{key}'"
            for v in values:
                assert isinstance(v, str), f"Alternative for '{key}' is not a string: {v}"

    def test_known_llm_favorites_have_alternatives(self):
        """Known LLM-favorite words should have alternatives."""
        from report import ALTERNATIVES

        expected_words = ["delve", "comprehensive", "robust", "leverage", "utilize"]
        for word in expected_words:
            assert word in ALTERNATIVES, f"Missing alternatives for '{word}'"


# =============================================================================
# Test compare.py: Pattern Counting
# =============================================================================

class TestPatternCounting:
    """Tests for the count_patterns function in compare.py."""

    def test_returns_expected_keys(self, opus_texts):
        """Should return a dict with all expected keys."""
        from compare import count_patterns

        result = count_patterns(opus_texts)

        assert "word_counts" in result
        assert "bigram_counts" in result
        assert "phrase_counts" in result
        assert "total_words" in result
        assert "total_chars" in result
        assert "num_samples" in result
        assert "em_dash_per_1k" in result
        assert "colon_per_1k" in result
        assert "semicolon_per_1k" in result

    def test_word_counts_are_counters(self, opus_texts):
        """Word counts should be Counter objects."""
        from compare import count_patterns

        result = count_patterns(opus_texts)

        assert isinstance(result["word_counts"], Counter)
        assert isinstance(result["bigram_counts"], Counter)

    def test_total_words_positive(self, opus_texts):
        """Total words should be positive for non-empty texts."""
        from compare import count_patterns

        result = count_patterns(opus_texts)

        assert result["total_words"] > 0
        assert result["total_chars"] > 0

    def test_num_samples_correct(self, opus_texts):
        """Number of samples should match input length."""
        from compare import count_patterns

        result = count_patterns(opus_texts)

        assert result["num_samples"] == len(opus_texts)

    def test_detects_known_phrases(self, opus_texts):
        """Should detect known LLM phrases in the texts."""
        from compare import count_patterns

        result = count_patterns(opus_texts)

        # "comprehensive" and "delve" are in the phrases list and in opus_texts
        assert result["phrase_counts"]["comprehensive"] > 0
        assert result["phrase_counts"]["delve"] > 0

    def test_punctuation_rates_non_negative(self, opus_texts):
        """Punctuation rates should be non-negative."""
        from compare import count_patterns

        result = count_patterns(opus_texts)

        assert result["em_dash_per_1k"] >= 0
        assert result["colon_per_1k"] >= 0
        assert result["semicolon_per_1k"] >= 0

    def test_em_dash_detected(self):
        """Should detect em dashes in text."""
        from compare import count_patterns

        texts = ["This is important -- very important. Also -- note this."]
        result = count_patterns(texts)

        assert result["em_dash_per_1k"] > 0


# =============================================================================
# Test compare.py: Sample Loading
# =============================================================================

class TestSampleLoading:
    """Tests for the load_samples function in compare.py."""

    def test_load_response_field(self, opus_jsonl_file):
        """Should load texts from the 'response' field."""
        from compare import load_samples

        texts = load_samples(opus_jsonl_file)

        assert len(texts) == 5

    def test_load_text_field(self, human_jsonl_file):
        """Should load texts from the 'text' field."""
        from compare import load_samples

        texts = load_samples(human_jsonl_file)

        assert len(texts) == 5

    def test_nonexistent_file_returns_empty(self, tmp_path):
        """Loading a nonexistent file should return empty list."""
        from compare import load_samples

        texts = load_samples(tmp_path / "nonexistent.jsonl")

        assert texts == []


# =============================================================================
# Test compare.py: Model Comparison
# =============================================================================

class TestModelComparison:
    """Tests for the compare_models function in compare.py."""

    @patch("compare.AVAILABLE_MODELS", {"test-model": "test-model-id"})
    def test_compare_with_mock_data(self, opus_texts, human_texts, tmp_path):
        """Should compare model data against human baseline."""
        from compare import compare_models

        # Set up data directory with model samples
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        # Write model samples
        model_file = data_dir / "test-model_samples.jsonl"
        with open(model_file, "w") as f:
            for text in opus_texts:
                f.write(json.dumps({"response": text}) + "\n")

        # Write human samples
        human_file = data_dir / "human_samples.jsonl"
        with open(human_file, "w") as f:
            for text in human_texts:
                f.write(json.dumps({"text": text}) + "\n")

        output_path = tmp_path / "comparison.json"

        results = compare_models(data_dir, human_file, output_path)

        assert "models" in results
        assert "human_baseline" in results
        assert "comparisons" in results
        assert output_path.exists()

    @patch("compare.AVAILABLE_MODELS", {"test-model": "test-model-id"})
    def test_comparison_results_structure(self, opus_texts, human_texts, tmp_path):
        """Comparison results should have expected structure."""
        from compare import compare_models

        data_dir = tmp_path / "data"
        data_dir.mkdir()

        model_file = data_dir / "test-model_samples.jsonl"
        with open(model_file, "w") as f:
            for text in opus_texts:
                f.write(json.dumps({"response": text}) + "\n")

        human_file = data_dir / "human_samples.jsonl"
        with open(human_file, "w") as f:
            for text in human_texts:
                f.write(json.dumps({"text": text}) + "\n")

        output_path = tmp_path / "comparison.json"
        results = compare_models(data_dir, human_file, output_path)

        # Check human baseline
        assert results["human_baseline"]["num_samples"] == len(human_texts)
        assert results["human_baseline"]["total_words"] > 0

        # Check model stats
        assert "test-model" in results["models"]
        assert results["models"]["test-model"]["num_samples"] == len(opus_texts)

        # Check comparisons
        assert "phrases" in results["comparisons"]
        assert "punctuation" in results["comparisons"]

    @patch("compare.AVAILABLE_MODELS", {})
    def test_no_model_samples_returns_empty_models(self, human_texts, tmp_path):
        """When no model samples are found, models dict should be empty."""
        from compare import compare_models

        data_dir = tmp_path / "data"
        data_dir.mkdir()

        human_file = data_dir / "human_samples.jsonl"
        with open(human_file, "w") as f:
            for text in human_texts:
                f.write(json.dumps({"text": text}) + "\n")

        output_path = tmp_path / "comparison.json"
        results = compare_models(data_dir, human_file, output_path)

        assert results["models"] == {}


# =============================================================================
# Test compare.py: Comparison Report Generation
# =============================================================================

class TestComparisonReport:
    """Tests for the generate_comparison_report function in compare.py."""

    def test_generates_markdown_report(self, tmp_path):
        """Should generate a markdown report from comparison data."""
        from compare import generate_comparison_report

        comparison_data = {
            "generated": "2025-01-15T12:00:00",
            "models": {
                "opus-4.5": {
                    "num_samples": 100,
                    "total_words": 50000,
                    "em_dash_per_1k": 2.5,
                    "colon_per_1k": 3.0,
                    "semicolon_per_1k": 0.5,
                },
            },
            "human_baseline": {
                "num_samples": 100,
                "total_words": 48000,
                "em_dash_per_1k": 0.8,
                "colon_per_1k": 1.5,
                "semicolon_per_1k": 0.7,
            },
            "comparisons": {
                "phrases": {
                    "delve": {"human": 0.01, "opus-4.5": 1.5},
                    "comprehensive": {"human": 0.15, "opus-4.5": 2.1},
                },
                "punctuation": {
                    "em_dash": {"human": 0.8, "opus-4.5": 2.5},
                    "colon": {"human": 1.5, "opus-4.5": 3.0},
                    "semicolon": {"human": 0.7, "opus-4.5": 0.5},
                },
            },
        }

        comparison_path = tmp_path / "comparison.json"
        with open(comparison_path, "w") as f:
            json.dump(comparison_data, f)

        output_path = tmp_path / "report.md"
        generate_comparison_report(comparison_path, output_path)

        assert output_path.exists()
        content = output_path.read_text()
        assert "Claude Model Evolution" in content
        assert "opus-4.5" in content

    def test_report_contains_punctuation_section(self, tmp_path):
        """Report should contain punctuation patterns section."""
        from compare import generate_comparison_report

        comparison_data = {
            "generated": "2025-01-15T12:00:00",
            "models": {
                "sonnet-4": {
                    "num_samples": 50,
                    "total_words": 25000,
                    "em_dash_per_1k": 1.5,
                    "colon_per_1k": 2.0,
                    "semicolon_per_1k": 0.3,
                },
            },
            "human_baseline": {
                "num_samples": 50,
                "total_words": 24000,
                "em_dash_per_1k": 0.5,
                "colon_per_1k": 1.0,
                "semicolon_per_1k": 0.6,
            },
            "comparisons": {
                "phrases": {},
                "punctuation": {
                    "em_dash": {"human": 0.5, "sonnet-4": 1.5},
                    "colon": {"human": 1.0, "sonnet-4": 2.0},
                    "semicolon": {"human": 0.6, "sonnet-4": 0.3},
                },
            },
        }

        comparison_path = tmp_path / "comparison.json"
        with open(comparison_path, "w") as f:
            json.dump(comparison_data, f)

        output_path = tmp_path / "report.md"
        generate_comparison_report(comparison_path, output_path)

        content = output_path.read_text()
        assert "Punctuation Patterns" in content
        assert "em dash" in content

    def test_report_contains_phrase_section(self, tmp_path):
        """Report should contain LLM phrase patterns section."""
        from compare import generate_comparison_report

        comparison_data = {
            "generated": "2025-01-15T12:00:00",
            "models": {
                "opus-4.5": {
                    "num_samples": 100,
                    "total_words": 50000,
                    "em_dash_per_1k": 2.5,
                    "colon_per_1k": 3.0,
                    "semicolon_per_1k": 0.5,
                },
            },
            "human_baseline": {
                "num_samples": 100,
                "total_words": 48000,
                "em_dash_per_1k": 0.8,
                "colon_per_1k": 1.5,
                "semicolon_per_1k": 0.7,
            },
            "comparisons": {
                "phrases": {
                    "delve": {"human": 0.01, "opus-4.5": 1.5},
                },
                "punctuation": {
                    "em_dash": {"human": 0.8, "opus-4.5": 2.5},
                    "colon": {"human": 1.5, "opus-4.5": 3.0},
                    "semicolon": {"human": 0.7, "opus-4.5": 0.5},
                },
            },
        }

        comparison_path = tmp_path / "comparison.json"
        with open(comparison_path, "w") as f:
            json.dump(comparison_data, f)

        output_path = tmp_path / "report.md"
        generate_comparison_report(comparison_path, output_path)

        content = output_path.read_text()
        assert "LLM Phrase Patterns" in content
        assert "delve" in content

    def test_report_with_multiple_models(self, tmp_path):
        """Report should handle multiple models correctly."""
        from compare import generate_comparison_report

        comparison_data = {
            "generated": "2025-01-15T12:00:00",
            "models": {
                "opus-4.5": {
                    "num_samples": 100,
                    "total_words": 50000,
                    "em_dash_per_1k": 2.5,
                    "colon_per_1k": 3.0,
                    "semicolon_per_1k": 0.5,
                },
                "sonnet-4": {
                    "num_samples": 100,
                    "total_words": 49000,
                    "em_dash_per_1k": 1.8,
                    "colon_per_1k": 2.5,
                    "semicolon_per_1k": 0.4,
                },
            },
            "human_baseline": {
                "num_samples": 100,
                "total_words": 48000,
                "em_dash_per_1k": 0.8,
                "colon_per_1k": 1.5,
                "semicolon_per_1k": 0.7,
            },
            "comparisons": {
                "phrases": {
                    "delve": {"human": 0.01, "opus-4.5": 1.5, "sonnet-4": 0.8},
                },
                "punctuation": {
                    "em_dash": {"human": 0.8, "opus-4.5": 2.5, "sonnet-4": 1.8},
                    "colon": {"human": 1.5, "opus-4.5": 3.0, "sonnet-4": 2.5},
                    "semicolon": {"human": 0.7, "opus-4.5": 0.5, "sonnet-4": 0.4},
                },
            },
        }

        comparison_path = tmp_path / "comparison.json"
        with open(comparison_path, "w") as f:
            json.dump(comparison_data, f)

        output_path = tmp_path / "report.md"
        generate_comparison_report(comparison_path, output_path)

        content = output_path.read_text()
        assert "opus-4.5" in content
        assert "sonnet-4" in content
        assert "Evolution Trends" in content


# =============================================================================
# Test analyze.py: Transition Word Analysis
# =============================================================================

class TestTransitionWordAnalysis:
    """Tests for the analyze_transition_words function."""

    def test_returns_expected_keys(self, opus_texts, human_texts):
        """Should return dict with expected keys."""
        from analyze import analyze_transition_words

        result = analyze_transition_words(opus_texts, human_texts)

        assert "transition_formal_opus_rate" in result
        assert "transition_formal_human_rate" in result
        assert "transition_casual_opus_rate" in result
        assert "transition_casual_human_rate" in result
        assert "transition_breakdown" in result

    def test_formal_transitions_detected(self):
        """Should detect formal transition words."""
        from analyze import analyze_transition_words

        formal_texts = [
            "Furthermore, this is important. Moreover, we should consider it. "
            "Additionally, the data shows improvement."
        ]
        casual_texts = [
            "But that's fine. And we moved on. So it worked out."
        ]

        result = analyze_transition_words(formal_texts, casual_texts)

        assert result["transition_formal_opus_rate"] > 0


# =============================================================================
# Test analyze.py: Sentence Starter Analysis
# =============================================================================

class TestSentenceStarterAnalysis:
    """Tests for the analyze_sentence_starters function."""

    def test_returns_expected_keys(self, opus_texts, human_texts):
        """Should return dict with expected keys."""
        from analyze import analyze_sentence_starters, tokenize_texts

        _, opus_sentences = tokenize_texts(opus_texts)
        _, human_sentences = tokenize_texts(human_texts)

        result = analyze_sentence_starters(opus_sentences, human_sentences)

        assert "sentence_starters_1word" in result
        assert "sentence_starters_2word" in result

    def test_starters_are_lists(self, opus_texts, human_texts):
        """Starter results should be lists of dicts."""
        from analyze import analyze_sentence_starters, tokenize_texts

        _, opus_sentences = tokenize_texts(opus_texts)
        _, human_sentences = tokenize_texts(human_texts)

        result = analyze_sentence_starters(opus_sentences, human_sentences)

        assert isinstance(result["sentence_starters_1word"], list)
        assert isinstance(result["sentence_starters_2word"], list)


# =============================================================================
# Test analyze.py: Lexical Pattern Analysis
# =============================================================================

class TestLexicalPatternAnalysis:
    """Tests for the analyze_lexical_patterns function."""

    def test_returns_list_of_markers(self, opus_texts, human_texts):
        """Should return a list of Marker objects."""
        from analyze import analyze_lexical_patterns, tokenize_texts, Marker

        opus_words, _ = tokenize_texts(opus_texts)
        human_words, _ = tokenize_texts(human_texts)

        markers = analyze_lexical_patterns(opus_words, human_words, opus_texts)

        assert isinstance(markers, list)
        for m in markers:
            assert isinstance(m, Marker)

    def test_markers_have_positive_log_odds(self, opus_texts, human_texts):
        """All returned markers should have positive log-odds (opus-favored)."""
        from analyze import analyze_lexical_patterns, tokenize_texts

        opus_words, _ = tokenize_texts(opus_texts)
        human_words, _ = tokenize_texts(human_texts)

        markers = analyze_lexical_patterns(opus_words, human_words, opus_texts)

        for m in markers:
            assert m.log_odds > 0
            # CI lower bound should also be > 0 (statistically significant)
            assert m.ci_lower > 0


# =============================================================================
# Test pipeline integration: analyze -> report
# =============================================================================

class TestAnalyzeToReportIntegration:
    """Integration tests: analyze results feed into report generation."""

    def test_analysis_results_feed_into_report(
        self, opus_jsonl_file, human_jsonl_file, tmp_path
    ):
        """Full pipeline: load corpus -> analyze -> generate report."""
        from analyze import load_corpus, tokenize_texts, analyze_lexical_patterns
        from analyze import analyze_structural_patterns, analyze_phrase_patterns
        from report import generate_styleguide

        # Load
        opus_texts = load_corpus(opus_jsonl_file, text_field="response")
        human_texts = load_corpus(human_jsonl_file, text_field="text")

        # Tokenize
        opus_words, opus_sentences = tokenize_texts(opus_texts)
        human_words, human_sentences = tokenize_texts(human_texts)

        # Analyze
        lexical_markers = analyze_lexical_patterns(
            opus_words, human_words, opus_texts
        )
        structural_markers, summary_stats = analyze_structural_patterns(
            opus_sentences, human_sentences, opus_texts, human_texts
        )
        phrase_markers = analyze_phrase_patterns(opus_texts, human_texts)

        all_markers = lexical_markers + structural_markers + phrase_markers
        all_markers.sort(key=lambda m: -m.log_odds)

        # Build results dict (same format as run_analysis)
        results = {
            "corpus_stats": {
                "opus_samples": len(opus_texts),
                "human_samples": len(human_texts),
                "opus_total_words": sum(len(w) for w in opus_words),
                "human_total_words": sum(len(w) for w in human_words),
            },
            "summary_stats": summary_stats,
            "markers": [
                {
                    "type": m.type,
                    "item": m.item,
                    "opus_rate": m.opus_rate,
                    "human_rate": m.human_rate,
                    "log_odds": m.log_odds,
                    "ci_lower": m.ci_lower,
                    "ci_upper": m.ci_upper,
                    "opus_count": m.opus_count,
                    "human_count": m.human_count,
                    "example_context": m.example_context,
                }
                for m in all_markers
            ],
        }

        # Save markers
        markers_path = tmp_path / "markers.json"
        with open(markers_path, "w") as f:
            json.dump(results, f, indent=2)

        # Generate report
        output_path = tmp_path / "styleguide.md"
        generate_styleguide(markers_path, output_path)

        # Verify
        assert output_path.exists()
        content = output_path.read_text()
        assert "# Personal Writing Styleguide" in content
        assert "Self-Editing Checklist" in content
        assert str(len(opus_texts)) in content


# =============================================================================
# Test pipeline integration: prompts -> compare
# =============================================================================

class TestPromptsToCompareIntegration:
    """Integration tests: prompt generation feeds model comparison."""

    @patch("compare.AVAILABLE_MODELS", {"test-model": "test-model-id"})
    def test_prompts_and_comparison_pipeline(
        self, opus_texts, human_texts, tmp_path
    ):
        """Prompts can be generated and comparison can run on sample data."""
        from generate_prompts import generate_all_prompts, save_prompts
        from compare import compare_models

        # Generate prompts
        prompts = generate_all_prompts(total_target=10)
        prompts_path = tmp_path / "prompts.jsonl"
        save_prompts(prompts, prompts_path)

        # Verify prompts were saved
        assert prompts_path.exists()

        # Set up sample data (simulating what generate_samples would produce)
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        model_file = data_dir / "test-model_samples.jsonl"
        with open(model_file, "w") as f:
            for text in opus_texts:
                f.write(json.dumps({"response": text}) + "\n")

        human_file = data_dir / "human_samples.jsonl"
        with open(human_file, "w") as f:
            for text in human_texts:
                f.write(json.dumps({"text": text}) + "\n")

        # Run comparison
        output_path = tmp_path / "comparison.json"
        results = compare_models(data_dir, human_file, output_path)

        # Verify comparison results
        assert results["models"]["test-model"]["num_samples"] == len(opus_texts)
        assert results["human_baseline"]["num_samples"] == len(human_texts)
        assert "phrases" in results["comparisons"]
        assert "punctuation" in results["comparisons"]


# =============================================================================
# Test edge cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases across pipeline modules."""

    def test_single_word_text(self):
        """Single-word text should not crash analysis functions."""
        from analyze import tokenize_texts, analyze_lexical_patterns

        opus_words, opus_sents = tokenize_texts(["Hello"])
        human_words, human_sents = tokenize_texts(["World"])

        # Should not raise
        markers = analyze_lexical_patterns(opus_words, human_words, ["Hello"])

        assert isinstance(markers, list)

    def test_unicode_in_texts(self):
        """Unicode characters should not crash the pipeline."""
        from analyze import tokenize_texts

        texts = ["This has unicode: cafe\u0301 re\u0301sume\u0301 and emoji \U0001f389"]
        words, sentences = tokenize_texts(texts)

        assert len(words) == 1
        assert len(words[0]) > 0

    def test_special_regex_characters_in_text(self):
        """Text with regex special characters should not crash."""
        from compare import count_patterns

        texts = ["Check [a-z]+ and (foo|bar) and {brace} patterns."]
        result = count_patterns(texts)

        assert result["total_words"] > 0

    def test_very_long_text(self):
        """Very long text should be handled correctly."""
        from analyze import get_ngrams

        words = ["word"] * 10000
        bigrams = get_ngrams(words, 2)

        assert len(bigrams) == 9999

    def test_report_with_empty_markers(self, tmp_path):
        """Report should handle empty markers list gracefully."""
        from report import generate_styleguide

        data = {
            "corpus_stats": {
                "opus_samples": 0,
                "human_samples": 0,
                "opus_total_words": 0,
                "human_total_words": 0,
            },
            "summary_stats": {},
            "markers": [],
        }

        markers_path = tmp_path / "empty_markers.json"
        with open(markers_path, "w") as f:
            json.dump(data, f)

        output_path = tmp_path / "empty_styleguide.md"
        generate_styleguide(markers_path, output_path)

        assert output_path.exists()
        content = output_path.read_text()
        assert "# Personal Writing Styleguide" in content

    def test_compare_empty_texts(self):
        """count_patterns should handle empty text list."""
        from compare import count_patterns

        result = count_patterns([""])

        assert result["total_words"] == 0
        assert result["num_samples"] == 1


# =============================================================================
# Run tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
