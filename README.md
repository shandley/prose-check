# prose-check

Scientific prose quality checker and writing skills for Claude Code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Two components:

1. **Writing skills** — Claude Code skills that guide natural, human-like prose for scientific manuscripts
2. **`prose_check` package** — a Python CLI and library that checks documents for AI writing patterns, statistical language problems, and bioinformatics methods gaps

---

## Writing Skills

### Install

```bash
# Install to current project
curl -fsSL https://raw.githubusercontent.com/shandley/prose-check/main/install-skills.sh | bash

# Install globally (all projects)
curl -fsSL https://raw.githubusercontent.com/shandley/prose-check/main/install-skills.sh | bash -s -- --global
```

Skills activate automatically when you write with Claude Code, or invoke them directly:

| Skill | Invoke | Use For |
|-------|--------|---------|
| **human-writing** | `/human-writing` | Essays, papers, documentation, articles |
| **manuscript-writing** | `/manuscript-writing` | Research papers, IMRaD structure, abstracts |
| **revision-workflow** | `/revision-workflow` | Peer review responses, change tracking |
| **submission-prep** | `/submission-prep` | Cover letters, submission checklists |
| **scientific-style** | `/scientific-style` | Citations, hedging, claim calibration |
| **scientific-figures** | `/scientific-figures` | Figure generation, visual review |
| **bibliography** | `/bibliography` | Citation cross-referencing, orphan detection |

```
Writing Phase:      manuscript-writing + human-writing + scientific-style
Figures Phase:      scientific-figures + manuscript-writing
Submission Phase:   submission-prep + bibliography + human-writing
Revision Phase:     revision-workflow + scientific-style + human-writing
```

---

## prose_check Package

### Install

```bash
pip install git+https://github.com/shandley/prose-check.git
```

Or with uv:

```bash
uv tool install git+https://github.com/shandley/prose-check.git
```

### Check a document

```bash
# Basic check
prose-check manuscript.md

# With scientific writing context (activates context-sensitive checkers)
prose-check manuscript.md --section results --study-type observational

# Multiple files
prose-check introduction.md methods.md results.md

# JSON output (for programmatic use or Margin integration)
prose-check manuscript.md --format json

# HTML report
prose-check manuscript.md --format html > report.html

# Interactive mode — review findings and apply fixes
prose-check manuscript.md --interactive

# Read from stdin
cat manuscript.md | prose-check --stdin --section discussion
```

### CLI flags

| Flag | Description |
|------|-------------|
| `--section` | Section type: `introduction`, `methods`, `results`, `discussion`, `abstract` |
| `--study-type` | Study design: `observational`, `experimental`, `review`, `methods-paper` |
| `--checkers` | Comma-separated list of checkers to run (default: all) |
| `--format {text,json,html}` | Output format (default: text) |
| `--interactive`, `-i` | Review findings and apply fixes one by one |
| `--verbose`, `-v` | Show medium-severity findings and category breakdown |
| `--no-technical` | Stricter mode — don't suppress technical term matches |
| `--stdin` | Read from stdin |
| `--min-score` | Exit code 1 if score falls below this threshold (default: 60) |

### Checkers

prose_check runs five checkers, each covering a different class of problem:

**`ai_patterns`** — LLM-characteristic vocabulary and structure

Flags words statistically overrepresented in Claude samples vs human text: "delve", "comprehensive", "robust", "nuanced", "paradigm", "tapestry", and ~110 others. Also checks em-dash overuse, hedging density, and formulaic sentence openers ("This document...", "Let's dive into...").

**`stat_phrases`** — Problematic statistical language

Flags phrases that soften non-significant results ("marginally significant", "all but significant", "approaching significance"), binary significance framing without exact p-values, and threshold-only reporting ("p < 0.05" as a final value rather than "p = 0.032"). Based on analysis of 568,000 published RCTs.

**`causal_lang`** — Causal verbs in observational contexts

Flags causal verbs ("drives", "causes", "determines", "demonstrates", "proves") when `--section` is `results` or `discussion` and `--study-type` is `observational`. Suggests associational alternatives ("is associated with", "predicts", "suggests"). Does not fire in methods or introduction sections, or for experimental designs.

**`structure`** — Paragraph and list structure

Flags paragraph fragmentation (AI averages 16 words per paragraph; human writing averages 210) and bullet overuse (AI uses ~9.5 list items per response; human prose uses near zero).

**`bio_methods`** — Bioinformatics methods completeness

Flags known bioinformatics tools (GATK, BWA, DESeq2, ADMIXTURE, IQ-TREE, and 80+ others) used without version numbers, "available upon request" data statements (rejected by eLife, PLOS Biology, Genome Biology), and sequencing data mentions without SRA/ENA/Dryad accession numbers.

### Configuration

Create `.prose-check.yaml` in your project:

```yaml
min_score: 70
technical: true
exclude:
  - "CHANGELOG.md"
  - "vendor/**"
ignore_patterns:
  - "robust"   # suppress specific patterns
```

### Library API

The package is importable as a Python library:

```python
from prose_check import check_text, DocumentContext, SectionType, StudyType

result = check_text(
    text="Temperature drives species richness across latitudes.",
    context=DocumentContext(
        section_type=SectionType.RESULTS,
        study_type=StudyType.OBSERVATIONAL,
    ),
)

print(result.score)          # 0-100
print(result.grade)          # "Fair - Some AI patterns"
for f in result.high:        # list[Finding]
    print(f.checker, f.text, f.alternative)
```

`check_text` accepts an optional `checkers` list to run a subset:

```python
result = check_text(text, checkers=["ai_patterns", "stat_phrases"])
```

### CI integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: prose-check
        name: Check prose
        entry: prose-check
        language: python
        types: [markdown]
        args: [--min-score, "70"]
```

---

## Margin Integration

prose_check is integrated into [Margin](https://github.com/shandley/agentic-md-editor) as two MCP tools:

**`margin_check_prose`** — runs prose_check on a Margin document, posts high-severity findings as annotation threads visible in the editor sidebar, and returns a structured quality report.

```
margin_check_prose(docId, sectionType="results", studyType="observational")
→ score: 52/100, 3 high, 4 medium findings, 3 annotation threads posted
```

**`margin_rewrite_section`** — returns the section text alongside a prioritised rewrite brief. Claude Code reads the output, rewrites the section, and calls `margin_update_document`. No additional API call is needed from the MCP server.

```
margin_rewrite_section(docId, sectionType="results", studyType="observational")
→ section text + rewrite instructions → Claude Code rewrites → margin_update_document
```

---

## Key Findings

### Em dash overuse is model-specific

| Model | Em Dash vs Human |
|-------|------------------|
| Haiku 3 | 0.0x |
| Sonnet 3.7 | 0.8x |
| Sonnet 4 | 0.9x |
| **Opus 4.5** | **16.8x** |

### Each model has different word quirks

| Word | Worst offender |
|------|----------------|
| "robust" | Haiku 3 (43x) |
| "nuanced" | Sonnet 4 (56x) |
| "comprehensive" | Haiku 3 (40x) |
| "paradigm" | Sonnet 4 (37x) |

### Counterintuitive findings

- **Passive voice:** AI uses less (4.7%) than humans (14.9%) — don't over-correct
- **Transitions:** AI uses fewer formal transitions than humans — "however" is more common in human writing
- **Paragraph length:** AI averages 16 words; humans average 210

---

## How the Markers Were Built

The AI pattern checker (`ai_patterns`) uses a hand-curated database of 119 markers drawn from statistical corpus analysis and recent corpus linguistics research (2024-2025). Ratios come from comparing 201 Claude Opus 4.5 samples (~47,000 words) to 6,000 human texts (~1.2M words).

The statistical method: log-odds ratio analysis identifies patterns where AI rate exceeds human rate by at least 2x with a statistically significant 95% confidence interval. The original corpus analysis produced ~2,954 candidate markers; these were curated down to 119 that reflect writing style differences rather than domain differences between the two corpora.

The other four checkers (`stat_phrases`, `causal_lang`, `structure`, `bio_methods`) are rule-based, drawing on published corpus linguistics literature rather than the corpus analysis pipeline.

To rebuild the marker database from fresh samples:

```bash
# Regenerate prose_check/data/markers.json
uv run python scripts/build_curated_markers.py

# Or regenerate from a new corpus via the analysis pipeline (~$1-2 API cost)
uv run python run_pipeline.py all --verbose
```

### Limitations

- **Model-specific:** Marker ratios are from Claude Opus 4.5; patterns differ across model versions and may not apply to other LLMs
- **Corpus mismatch:** Human baseline is English web text (Wikipedia, OpenWebText), not scientific journals
- **Context-blind:** The `ai_patterns` checker can't determine if a flagged pattern is contextually appropriate — use `--section` and `--study-type` to reduce false positives
- **Static:** Markers don't update automatically as models change; run the pipeline to refresh

---

## Project Structure

```
prose-check/
├── install-skills.sh          # Skill installer
├── .claude/skills/            # Claude Code skills
│   ├── human-writing/
│   ├── manuscript-writing/
│   ├── revision-workflow/
│   ├── submission-prep/
│   ├── scientific-style/
│   ├── scientific-figures/
│   └── bibliography/
├── prose_check/               # Python package
│   ├── __init__.py            # Public API: check_text()
│   ├── checkers/
│   │   ├── ai_patterns.py
│   │   ├── stat_phrases.py
│   │   ├── causal_lang.py
│   │   ├── structure.py
│   │   └── bio_methods.py
│   ├── data/                  # Bundled marker databases
│   │   ├── markers.json
│   │   ├── stat_phrases.json
│   │   ├── causal_verbs.json
│   │   └── bio_tools.json
│   ├── cli.py                 # Entry point
│   └── formatter.py
├── scripts/
│   └── build_curated_markers.py
├── run_pipeline.py            # Analysis pipeline CLI
├── src/                       # Pipeline modules
└── docs/
    └── methodology.md
```

## License

MIT

## Citation

```bibtex
@software{handley2026prosecheck,
  author = {Handley, Scott A.},
  title = {prose-check: Scientific Prose Quality Checker},
  year = {2026},
  url = {https://github.com/shandley/prose-check}
}
```
