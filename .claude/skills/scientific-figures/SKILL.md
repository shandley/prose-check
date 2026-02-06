---
name: scientific-figures
description: Generate and review scientific figures using AI. Iteratively creates publication-quality figures aligned with manuscript content using Gemini for generation and Claude vision for review. Works well with submission-prep and manuscript-writing skills.
argument-hint: [figure description or "review figures/" or manuscript path]
---

# Scientific Figures Guide

Generate, review, and align scientific figures with manuscript content. Uses Gemini for image generation and Claude's vision for quality review in an iterative generate-review-revise loop.

## When to Use This Skill

- Generating new scientific figures from manuscript descriptions
- Reviewing existing figures against publication standards
- Aligning figure content with manuscript claims and captions
- Iteratively improving figure quality through AI review

**Combine with:** `submission-prep` for final figure specifications, `manuscript-writing` for figure references in text.

## Three Modes

### Mode 1: Generate

Create a new figure from a text description.

```bash
python .claude/skills/scientific-figures/scripts/generate_figure.py \
  "workflow diagram showing sample collection through bioinformatic analysis pipeline" \
  --style scientific \
  --output figures/fig1_workflow.png
```

**Steps:**
1. Read relevant manuscript sections to understand what the figure should convey
2. Build a detailed prompt incorporating manuscript context, claims, and caption text
3. Run `generate_figure.py` with `--style scientific` for publication-quality defaults
4. Review the generated image using the Read tool (Claude's vision)
5. If revision needed, run `generate_figure.py` with `--input-image` for iterative editing
6. Maximum 3 revision iterations, then present best result

### Mode 2: Review

Evaluate existing figures against publication standards.

**Steps:**
1. Use Glob to find all figures: `figures/*.png`, `figures/*.jpg`, `fig*.png`
2. Read each figure with the Read tool to visually inspect it
3. Score against the checklist in [REVIEW_CRITERIA.md](REVIEW_CRITERIA.md)
4. Report findings with specific, actionable feedback

### Mode 3: Align

Check that figures match manuscript content.

**Steps:**
1. Read the manuscript to identify all figure references (e.g., "Figure 1", "Fig. 2")
2. Extract what each figure reference claims to show
3. Read each figure file with the Read tool
4. Compare figure content against manuscript claims and captions
5. Report misalignments with specific suggestions

## Generate-Review-Revise Loop

```
Generate figure (generate_figure.py --style scientific)
      |
      v
Review image (Read tool - visual inspection)
      |
      v
  Pass? --yes--> Done (report results)
      |
      no (max 3 iterations)
      |
      v
Classify issues: surface vs structural
      |
      +--> Surface issues (colors, text size, small additions):
      |      Edit figure (generate_figure.py --input-image <prev> "fix instructions")
      |
      +--> Structural issues (layout, flow, arrangement):
             Re-generate from scratch with improved prompt
      |
      v
  (loop back to Review)
```

**Iteration rules:**
- Maximum 3 revision attempts per figure
- Each revision prompt must reference specific issues from the review
- After 3 attempts, present the best version and list remaining issues
- Save each iteration (fig1_v1.png, fig1_v2.png, etc.) so the user can compare

**When to edit vs re-generate:**
Gemini's multi-turn editing is conservative - it preserves the original composition strongly. This means:
- **Use `--input-image` editing for:** color changes, text/label tweaks, adding small elements, adjusting styling
- **Re-generate from scratch for:** changing layout structure, rearranging components, modifying arrow/flow direction, changing the overall composition
- When re-generating, incorporate the specific improvements into a more detailed initial prompt rather than trying to edit the structure after the fact

## Generation Script Usage

The `generate_figure.py` script in `scripts/` handles Gemini API calls:

```bash
# New figure with scientific style
python .claude/skills/scientific-figures/scripts/generate_figure.py \
  "bar chart comparing gene expression across three conditions" \
  --style scientific \
  --output figures/fig2.png

# Edit existing figure
python .claude/skills/scientific-figures/scripts/generate_figure.py \
  "increase label font size, add significance asterisks above bars" \
  --input-image figures/fig2.png \
  --output figures/fig2_v2.png

# High-resolution for print
python .claude/skills/scientific-figures/scripts/generate_figure.py \
  "phylogenetic tree of opsin gene family" \
  --style scientific \
  --size 2k \
  --output figures/fig3.png

# Validate API key
python .claude/skills/scientific-figures/scripts/generate_figure.py --validate
```

**Flags:**
- `--style scientific`: Prepends publication-quality instructions (white background, clean lines, sans-serif labels, colorblind-safe colors)
- `--input-image`: Provide existing image for multi-turn editing (best for surface tweaks, not structural changes)
- `--size 1k|2k|4k`: Advisory target resolution (actual output resolution is model-controlled, typically ~1408x768)
- `--output`: Output file path (default: `figure_TIMESTAMP.png`)

The script outputs JSON metadata to stderr with model used, prompt, timing, and success status.

**Important notes:**
- Gemini returns JPEG data regardless of the output file extension. The script detects the actual format and corrects the extension automatically (e.g., `fig1.png` becomes `fig1.jpg` if Gemini returns JPEG).
- Output resolution is controlled by the model, not the `--size` flag. The flag adds resolution hints to the prompt but Gemini may ignore them. Typical output is ~1408x768 at 300 DPI.

## Review Criteria (Quick Reference)

When reviewing figures (either generated or existing), check:

1. **Content accuracy** - Does the figure match what the manuscript claims it shows?
2. **Text legibility** - All labels, axis titles, and annotations readable at print size?
3. **Color accessibility** - Colorblind-safe palette? Works in grayscale?
4. **Panel labeling** - Consistent uppercase bold letters (A, B, C) in upper-left?
5. **Scale and units** - Present where needed (scale bars, axis units)?
6. **Style consistency** - Matches other figures in the manuscript set?
7. **Technical quality** - Clean lines, no artifacts, no watermarks, no AI artifacts?
8. **Caption alignment** - Figure content matches its caption description?

See [REVIEW_CRITERIA.md](REVIEW_CRITERIA.md) for the full scored checklist.

## Prompt Engineering for Scientific Figures

### Always Include

- What the figure shows (the data or concept)
- Layout (single panel, multi-panel with arrangement)
- Label requirements (axes, legends, panel labels)
- Color scheme (specify if important, or use "colorblind-safe palette")
- Style: "clean, publication-quality, white background, sans-serif labels"

### Avoid

- Vague descriptions ("make it look good")
- Requesting real data visualization (Gemini generates illustrative figures, not data plots)
- Overly complex multi-panel layouts (generate panels separately if needed)

### Effective Prompts

**Good:** "A workflow diagram with 4 steps flowing left to right: (1) Sample Collection showing a test tube, (2) DNA Extraction showing a double helix, (3) Sequencing showing a machine icon, (4) Analysis showing a computer with bar chart. Connect steps with arrows. Use blue color scheme, white background, sans-serif labels."

**Poor:** "Make a figure for my methods section."

See [PROMPT_TEMPLATES.md](PROMPT_TEMPLATES.md) for reusable templates by figure type.

## Configuration

The generation script requires a Google API key:

1. Set `GOOGLE_API_KEY` environment variable, or
2. Add `GOOGLE_API_KEY=your_key` to a `.env` file in the project directory

## Related Files

- [REVIEW_CRITERIA.md](REVIEW_CRITERIA.md) - Full scored review checklist
- [PROMPT_TEMPLATES.md](PROMPT_TEMPLATES.md) - Reusable prompt templates by figure type
