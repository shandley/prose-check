# prose-check

Writing skills for Claude Code that produce natural, human-like prose.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Quick Start

**Install skills to your project:**

```bash
curl -fsSL https://raw.githubusercontent.com/shandley/prose-check/main/install-skills.sh | bash
```

**Or install globally (all projects):**

```bash
curl -fsSL https://raw.githubusercontent.com/shandley/prose-check/main/install-skills.sh | bash -s -- --global
```

That's it. Skills activate automatically when you write with Claude Code.

## Skills Overview

| Skill | Invoke | Use For |
|-------|--------|---------|
| **human-writing** | `/human-writing` | Essays, papers, documentation, articles |
| **manuscript-writing** | `/manuscript-writing` | Research papers, IMRaD structure, abstracts |
| **revision-workflow** | `/revision-workflow` | Peer review responses, change tracking |
| **submission-prep** | `/submission-prep` | Cover letters, submission checklists |
| **scientific-style** | `/scientific-style` | Citations, hedging, claim calibration |

### Workflow Integration

```
Writing Phase:      manuscript-writing + human-writing + scientific-style
Submission Phase:   submission-prep + human-writing
Revision Phase:     revision-workflow + scientific-style + human-writing
```

## Skill Details

### human-writing

Write in natural, human style by avoiding common AI patterns.

**What it covers:**
- Words and phrases that signal AI writing (with alternatives)
- Punctuation patterns (em dash overuse is 16.8x human rate in Opus 4.5)
- Structural issues (paragraph length, bullet overuse)
- Model-specific quirks (different Claude versions have different tells)

**Based on:** Statistical analysis of 200+ Claude samples vs 6,000 human texts.

### manuscript-writing

Structure academic research papers using IMRaD format.

**What it covers:**
- Section-by-section guidance (Introduction, Methods, Results, Discussion)
- Title construction patterns
- Abstract templates (structured and unstructured) with word budgets
- Transition phrases between sections

### revision-workflow

Respond to peer review and manage manuscript revisions.

**What it covers:**
- Response letter structure and tone
- Templates for agreement, disagreement, cannot-address
- Strategies for common reviewer concerns
- Version control and change tracking

### submission-prep

Prepare manuscripts for journal submission.

**What it covers:**
- Cover letter templates (initial and resubmission)
- Pre-submission checklist
- Figure specifications (resolution, formats, sizing)
- Table formatting guidelines

### scientific-style

Calibrate scientific claims and integrate citations properly.

**What it covers:**
- Claim strength ladder (certain → speculative)
- When hedging IS appropriate (complements human-writing)
- Citation patterns (integral vs non-integral)
- Reporting verbs and their connotations
- Tense usage by section

## Installation Options

### Option 1: Install Script (Recommended)

```bash
# Install to current project
./install-skills.sh

# Install globally
./install-skills.sh --global

# List available skills
./install-skills.sh --list
```

### Option 2: Manual Copy

```bash
# Clone the repo
git clone https://github.com/shandley/prose-check.git

# Copy skills to your project
cp -r prose-check/.claude/skills/human-writing .claude/skills/
cp -r prose-check/.claude/skills/manuscript-writing .claude/skills/
cp -r prose-check/.claude/skills/revision-workflow .claude/skills/
cp -r prose-check/.claude/skills/submission-prep .claude/skills/
cp -r prose-check/.claude/skills/scientific-style .claude/skills/

# Or copy to global location
cp -r prose-check/.claude/skills/* ~/.claude/skills/
```

### Option 3: Git Submodule

```bash
# Add as submodule
git submodule add https://github.com/shandley/prose-check.git .prose-check

# Symlink skills directory
ln -s .prose-check/.claude/skills .claude/skills
```

## Verifying Installation

After installation, skills should appear when you run Claude Code:

```
Available skills:
  - human-writing
  - manuscript-writing
  - revision-workflow
  - submission-prep
  - scientific-style
```

Invoke any skill directly:
```
/human-writing Write an introduction about climate change
/manuscript-writing Help me structure my Methods section
```

Or let them activate automatically based on context.

---

## CLI Tool (Optional)

prose-check also includes a CLI for checking existing text against AI patterns.

### Install CLI

```bash
pip install git+https://github.com/shandley/prose-check.git
```

### Check Your Writing

```bash
# Check a document
prose-check document.md

# Multiple files
prose-check README.md docs/*.md

# Different output formats
prose-check document.md --format json
prose-check document.md --format html > report.html

# Interactive mode - review and fix findings
prose-check document.md --interactive

# Verbose (include low-severity)
prose-check document.md --verbose
```

Output includes a score (0-100, higher = more human-like) and flags for:
- Overused punctuation (em dashes, colons, semicolons)
- AI-favored words and phrases
- Structural issues (short paragraphs, bullet overuse)

### CLI Options

| Flag | Description |
|------|-------------|
| `--format {text,json,html}` | Output format (default: text) |
| `--interactive`, `-i` | Review findings and apply fixes |
| `--verbose`, `-v` | Include low-severity findings |
| `--no-technical` | Stricter mode for essays/articles |
| `--stdin` | Read from stdin |

### Configuration

Create `.prose-check.yaml` in your project:

```yaml
min_score: 70
technical: true
exclude:
  - "CHANGELOG.md"
  - "vendor/**"
ignore_patterns:
  - "comprehensive"
```

### CI Integration

**Pre-commit hook:**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: prose-check
        name: Check prose for AI patterns
        entry: prose-check
        language: python
        types: [markdown]
```

**GitHub Action:** See `.github/workflows/prose-check.yml`

---

## Analysis Pipeline (Advanced)

Regenerate markers from fresh Claude samples.

### Setup

```bash
git clone https://github.com/shandley/prose-check.git
cd prose-check
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
```

### Run Pipeline

```bash
# Full pipeline (~$1-2 API cost)
python run_pipeline.py all --verbose

# Individual steps
python run_pipeline.py generate-prompts --n 300
python run_pipeline.py generate-samples --n 200
python run_pipeline.py fetch-human-corpus --n 10000
python run_pipeline.py analyze
python run_pipeline.py report
```

### Multi-Model Comparison

```bash
# Generate samples from different models
python run_pipeline.py generate-samples --model sonnet-4 --n 50
python run_pipeline.py generate-samples --model haiku-3 --n 50

# Compare patterns across models
python run_pipeline.py compare-models --verbose
```

Available models: `opus-4.5`, `sonnet-4`, `sonnet-3.7`, `haiku-3.5`, `haiku-3`

---

## Key Findings

### Em Dash Overuse is Opus 4.5-Specific

| Model | Em Dash vs Human |
|-------|------------------|
| Haiku 3 | 0.0x |
| Sonnet 3.7 | 0.8x |
| Sonnet 4 | 0.9x |
| **Opus 4.5** | **16.8x** |

### Each Model Has Different Word Quirks

| Word | Worst Offender |
|------|----------------|
| "robust" | Haiku 3 (43x) |
| "nuanced" | Sonnet 4 (56x) |
| "comprehensive" | Haiku 3 (40x) |
| "paradigm" | Sonnet 4 (37x) |

### Counterintuitive Findings

- **Passive voice:** AI uses LESS (4.7%) than humans (14.9%)
- **Transitions:** AI uses FEWER formal transitions than humans
- **Paragraph length:** AI averages 16 words; humans average 210 words

---

## How the Skills Were Created

The writing guidance in these skills is based on **statistical corpus analysis**, not conventional wisdom.

### Data Sources

**AI Corpus:**
- 201 Claude Opus 4.5 samples (~47,000 words)
- Generated from 300+ diverse prompts (technical docs, professional writing, general prose)
- Additional samples from Sonnet 4, Sonnet 3.7, Haiku 3.5, Haiku 3 for comparison

**Human Baseline:**
- 6,000 texts (~1.2M words)
- Sources: Wikipedia (40%), OpenWebText (30%), C4 dataset (20%), The Pile (10%)
- Filtered to match AI sample characteristics (length, genre)

### Statistical Method

**Log-odds ratio analysis** identifies patterns that are statistically overrepresented in AI text:

```
Pattern is flagged if:
1. Appears ≥5 times in AI corpus
2. AI rate ≥ 2x human rate
3. 95% confidence interval doesn't cross zero (statistically significant)
```

**Example:**
- "comprehensive" appears 24.4x more in Opus 4.5 than human text (CI: 3.08–3.32)
- Em dashes: 4.78 per 1k chars (AI) vs 0.28 (human) = 16.9x overuse

### From Statistics to Guidance

The analysis produces ~2,954 markers across categories:

| Category | Detection | Skill Guidance |
|----------|-----------|----------------|
| **Lexical** | "comprehensive" 24x, "robust" 43x (Haiku) | Word alternatives table |
| **Punctuation** | Em dash 16.9x, colon 4.1x, semicolon 3.1x | Avoid overuse guidance |
| **Structure** | Paragraphs 16 words (AI) vs 210 (human) | Combine related ideas |
| **Hedging** | "typically" 9.6x, "often" 4.9x | Be direct guidance |
| **Sentence starters** | "This document..." 623x | Avoid formulaic openings |

### Why This Matters

Traditional style guides are based on conventions and expert opinion. These skills are based on measurable differences between AI and human writing. Some findings contradict common advice:

- **Passive voice:** AI uses less, not more → don't over-correct
- **Transitions:** AI uses fewer "however," "furthermore" → don't avoid them entirely
- **Hedging:** Context matters → scientific writing exceptions in `scientific-style` skill

### Limitations

- **Model-specific:** Trained primarily on Claude (Opus 4.5); patterns may differ for GPT, other LLMs
- **Corpus bias:** Human baseline is primarily English web text, not academic journals or fiction
- **Static patterns:** Markers don't auto-update as models evolve
- **Context-blind:** Can't determine if a flagged pattern is contextually appropriate

### Learn More

- **[Full Methodology](docs/methodology.md)** - Statistical approach, confidence intervals, filtering criteria
- **[Model Comparison](results/model_comparison.md)** - How patterns differ across Claude versions
- **[Markers Database](results/markers.json)** - All 2,954 detected patterns with statistics

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
│   └── scientific-style/
├── check_writing.py           # CLI tool
├── run_pipeline.py            # Analysis pipeline
├── src/                       # Pipeline modules
├── results/                   # Generated analysis
│   ├── markers.json           # Pre-trained patterns
│   ├── styleguide.md          # Writing guide
│   └── model_comparison.md    # Cross-model analysis
└── docs/
    └── methodology.md         # Statistical approach
```

## License

MIT

## Citation

```bibtex
@software{handley2026prosecheck,
  author = {Handley, Scott A.},
  title = {prose-check: Writing Skills for Natural Prose},
  year = {2026},
  url = {https://github.com/shandley/prose-check}
}
```
