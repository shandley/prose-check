# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Methodology documentation (`docs/methodology.md`)
- PROJECT.yaml for project tracking
- CITATION.cff for academic citations
- This CHANGELOG

### Changed
- Repository renamed from `claude-style-guide` to `prose-check`
- Updated GitHub URLs in pyproject.toml

## [0.1.0] - 2026-01-21

### Added
- Initial release of prose-check
- Statistical analysis pipeline (`run_pipeline.py`)
  - Prompt generation for diverse writing samples
  - Multi-model sample generation (Opus 4.5, Sonnet 4, Sonnet 3.7, Haiku 3)
  - Human corpus fetching from Wikipedia/OpenWebText
  - Log-odds ratio analysis with confidence intervals
  - Styleguide report generation
- Document checker CLI (`check_writing.py`)
  - Score calculation (0-100 scale)
  - Multiple output formats (text, JSON, HTML)
  - Interactive fixing mode
  - Configuration file support (`.prose-check.yaml`)
  - Technical term exclusion
- Pre-trained markers (2,954 patterns)
  - 1,781 high severity markers
  - 684 medium severity markers
- Multi-model comparison capability
- Pre-commit hook integration
- GitHub Action for PR checks
- Claude Code skill (`/human-writing`)

### Detection Categories
- Lexical: words, bigrams, trigrams
- Punctuation: em dashes, colons, semicolons
- Sentence starters: formulaic openings
- Structure: paragraph length, list density
- Hedging: qualifying language

### Key Findings
- Em dash overuse is Opus 4.5 specific (16.8x human rate)
- AI paragraphs average 16 words vs human 210 words
- AI uses 9.5 list items/doc vs near zero for humans
- Different Claude models have different word quirks

[Unreleased]: https://github.com/shandley/prose-check/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/shandley/prose-check/releases/tag/v0.1.0
