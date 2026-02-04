# Methodology: How prose-check Detects AI Writing Patterns

This document explains the statistical approach used to identify LLM writing signatures.

## Overview

prose-check uses **corpus comparison** to identify patterns that are statistically overrepresented in AI-generated text compared to human writing. It is not a machine learning classifier—it's a statistical analysis tool that measures stylistic similarity to known AI output patterns.

## Training Data

### Corpora

| Corpus | Samples | Words | Source |
|--------|---------|-------|--------|
| **AI (Opus 4.5)** | 201 | ~47,000 | Generated responses to diverse prompts |
| **Human** | 6,000 | ~1.2M | Wikipedia, OpenWebText, C4 |

The human corpus is intentionally larger to provide stable baseline rates for rare patterns.

### Prompt Generation

AI samples are generated from diverse prompts covering:
- Technical documentation (40%)
- Professional writing (30%)
- Creative/general (30%)

Prompts are designed to elicit the same types of content humans write, not conversational responses.

## Statistical Method

### Log-Odds Ratio

For each pattern (word, phrase, n-gram), we calculate the **log-odds ratio**:

```
log_odds = log(opus_rate / human_rate)
```

Where:
- `opus_rate` = (count in AI text + 0.5) / (total AI words + 1)
- `human_rate` = (count in human text + 0.5) / (total human words + 1)

The 0.5 smoothing (Laplace) prevents division by zero for patterns not seen in one corpus.

### Confidence Intervals

We use the **Agresti-Coull method** to calculate 95% confidence intervals:

```python
se = sqrt(1/(opus_count + 0.5) + 1/(opus_total - opus_count + 0.5) +
          1/(human_count + 0.5) + 1/(human_total - human_count + 0.5))

ci_lower = log_odds - 1.96 * se
ci_upper = log_odds + 1.96 * se
```

### Filtering Criteria

A pattern is included as a marker only if:

1. **Minimum frequency**: Appears at least 5 times (unigrams) or 3 times (n-grams) in AI corpus
2. **Meaningful difference**: AI rate is at least 2x the human rate
3. **Statistical significance**: 95% CI lower bound > 0 (doesn't cross zero)

## Severity Thresholds

| Severity | Log-Odds | Interpretation |
|----------|----------|----------------|
| **High** | ≥ 2.5 | Strong AI signal (12x+ more common) |
| **Medium** | ≥ 1.5 | Moderate AI signal (4.5x+ more common) |
| **Low** | < 1.5 | Weak signal (shown only in verbose mode) |

These thresholds were calibrated empirically to balance sensitivity and false positives.

## Pattern Categories

### Lexical Patterns

| Type | Description | Example |
|------|-------------|---------|
| **Unigrams** | Single words | "comprehensive" (24x) |
| **Bigrams** | Two-word phrases | "comprehensive guide" (922x) |
| **Trigrams** | Three-word phrases | "let me walk" (768x) |

### Structural Patterns

| Pattern | AI Average | Human Average | Detection |
|---------|------------|---------------|-----------|
| **Paragraph length** | 16 words | 210 words | Flag if avg < 40 words |
| **List items per doc** | 9.5 | ~0 | Flag if > 1 item per 100 words |
| **Em dashes per 1k chars** | 4.78 | 0.28 | Flag if > 1.0 per 1k |

### Sentence Starters

Formulaic openings are detected at sentence boundaries:
- "This document..." (623x human rate)
- "Comprehensive..." (680x human rate)
- "Let's explore..." (high ratio)

### Hedging Language

Words that qualify statements excessively:
- "typically" (9.6x), "often" (4.9x), "sometimes" (4.2x)

## Score Calculation

The final score (0-100, higher = more human-like) is calculated as:

```python
high_penalty = high_severity_count * 10
medium_penalty = medium_severity_count * 3

penalty_per_100_words = (high_penalty + medium_penalty) / (total_words / 100)

score = max(0, min(100, 100 - penalty_per_100_words))
```

### Grade Interpretation

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | Excellent | Very human-like writing |
| 75-89 | Good | Minor AI patterns |
| 60-74 | Fair | Some noticeable AI patterns |
| 40-59 | Needs work | Notable AI patterns throughout |
| 0-39 | High AI signal | Strongly AI-like writing |

## Technical Mode

When `technical: true` (default), the following are excluded from detection:
- Programming languages (python, javascript, etc.)
- Technical terms (api, database, endpoint, etc.)
- Common programming concepts (function, class, variable, etc.)
- Technical phrases (error handling, rate limiting, etc.)

This prevents false positives in technical documentation.

## Multi-Model Findings

Different Claude models have different patterns:

| Pattern | Opus 4.5 | Sonnet 4 | Sonnet 3.7 | Haiku 3 |
|---------|----------|----------|------------|---------|
| Em dash overuse | **16.8x** | 0.9x | 0.8x | 0.0x |
| "robust" | 3.1x | 7.7x | 6.5x | **43.2x** |
| "comprehensive" | 24.4x | 37.9x | 30.1x | **39.5x** |

The current markers are primarily trained on **Opus 4.5** output.

## Limitations

1. **Model-specific**: Patterns are learned from Claude; may not generalize to other LLMs
2. **Corpus bias**: Human corpus is primarily English Wikipedia/web text
3. **No context awareness**: Cannot determine if a flagged word is appropriate in context
4. **Static patterns**: Does not adapt to new AI writing patterns automatically
5. **Technical documents**: Short paragraphs and bullet points may be appropriate

## Retraining

To regenerate markers with fresh data:

```bash
# Generate new AI samples (requires ANTHROPIC_API_KEY)
python run_pipeline.py generate-samples --n 200

# Fetch fresh human corpus
python run_pipeline.py fetch-human-corpus --n 6000

# Run analysis
python run_pipeline.py analyze

# Check new markers
python run_pipeline.py report
```

## References

- Agresti, A., & Coull, B. A. (1998). Approximate is better than "exact" for interval estimation of binomial proportions. *The American Statistician*, 52(2), 119-126.
- Monroe, B. L., Colaresi, M. P., & Quinn, K. M. (2008). Fightin' words: Lexical feature selection and evaluation for identifying the content of political conflict. *Political Analysis*, 16(4), 372-403.
