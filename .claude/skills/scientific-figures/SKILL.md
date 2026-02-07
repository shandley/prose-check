---
name: scientific-figures
description: Generate and review scientific figures using AI. Creates publication-quality figures aligned with manuscript content using Gemini for generation and Claude vision for review. Works well with submission-prep and manuscript-writing skills.
argument-hint: [figure description or "review figures/" or manuscript path]
---

# Scientific Figures Guide

Generate, review, and align scientific figures with manuscript content. Uses Gemini for image generation and Claude's vision for quality review following a **plan-generate-report** pipeline.

## Core Principle: Plan Once, Generate Once

Automated revision loops (generate → critique → re-generate) **do not improve results**. Gemini generates a new image each time — it cannot surgically fix specific elements. Iteration typically degrades quality or introduces new errors. Testing with both direct Gemini calls and multi-agent frameworks (PaperBanana) confirmed this: iteration 1 consistently outperforms iteration 2+.

Instead, invest effort in building a detailed, spatially-structured prompt. The first generation with a good prompt is almost always the best result.

## When to Use This Skill

- Generating new scientific figures from manuscript descriptions
- Reviewing existing figures against publication standards
- Aligning figure content with manuscript claims and captions

**Combine with:** `submission-prep` for final figure specifications, `manuscript-writing` for figure references in text.

## When to Use Gemini vs Real Screenshots

Gemini excels at **conceptual and architectural diagrams** — workflow figures, system architecture, taxonomy charts, process flows. These consistently come out publication-quality on the first try with detailed prompts.

**Do NOT use Gemini for:**
- Screenshots of actual tool output (terminal renderings, code output, UI screenshots). These will be illustrative approximations, not authentic. Use real screenshots instead.
- Figures that require precise data representation. Gemini generates illustrative figures, not data-driven plots.
- Figures where exact text content matters at readable size. Gemini hallucinates details in small text (dates, file paths, code snippets). Accept this when the text is decorative/too small to read, but avoid Gemini when the text must be accurate and legible.

**For multi-panel figures with mixed content** (e.g., real tool output alongside diagrams), generate or capture each panel separately and compose them with Python Pillow. See "Composing Multi-Panel Figures" below.

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
2. Build a detailed, spatially-structured prompt (see "Prompt Engineering" below)
3. Run `generate_figure.py` with `--style scientific` for publication-quality defaults
4. Review the generated image using the Read tool (Claude's vision)
5. Report results to the user: what looks good, what has issues, and whether to accept or re-generate with an improved prompt

**If the result has issues:**
- **Accept minor issues** — small text hallucinations (wrong dates, garbled paths) in text too small to read at print size are not worth re-generating for
- **Re-generate with a better prompt** — if the layout or content is wrong, improve the prompt and generate fresh. Do not use `--input-image` editing, which is unreliable
- **Let the user decide** — present the figure with a clear list of issues and let them choose

### Mode 2: Review

Evaluate existing figures against publication standards.

**Steps:**
1. Use Glob to find all figures: `figures/*.png`, `figures/*.jpg`, `fig*.png`
2. Read each figure with the Read tool to visually inspect it
3. Score against the checklist in [REVIEW_CRITERIA.md](REVIEW_CRITERIA.md)
4. **Review all figures together** for cross-figure consistency (background colors, palettes, fonts, border styles, label conventions)
5. Report findings with specific, actionable feedback

### Mode 3: Align

Check that figures match manuscript content.

**Steps:**
1. Read the manuscript to identify all figure references (e.g., "Figure 1", "Fig. 2")
2. Extract what each figure reference claims to show
3. Read each figure file with the Read tool
4. Compare figure content against manuscript claims and captions
5. Report misalignments with specific suggestions

## Generation Script Usage

The `generate_figure.py` script in `scripts/` handles Gemini API calls:

```bash
# New figure with scientific style
python .claude/skills/scientific-figures/scripts/generate_figure.py \
  "bar chart comparing gene expression across three conditions" \
  --style scientific \
  --output figures/fig2.png

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
- `--input-image`: Provide existing image for multi-turn editing. **Use sparingly** — only for minor color/style tweaks. Never for text changes.
- `--size 1k|2k|4k`: Advisory target resolution (actual output resolution is model-controlled, typically ~1408x768)
- `--output`: Output file path (default: `figure_TIMESTAMP.png`)

The script outputs JSON metadata to stderr with model used, prompt, timing, and success status.

**Important notes:**
- Gemini returns JPEG data regardless of the output file extension. The script detects the actual format and corrects the extension automatically (e.g., `fig1.png` becomes `fig1.jpg` if Gemini returns JPEG).
- Output resolution is controlled by the model, not the `--size` flag. The flag adds resolution hints to the prompt but Gemini may ignore them. Typical output is ~1408x768 at 300 DPI.

## Why Not Iterate?

Automated critique-and-revise loops sound appealing but fail in practice:

1. **Gemini cannot surgically edit** — each "revision" generates a completely new image. It may fix one issue while introducing three others.
2. **Text editing introduces errors** — attempting to fix "2028" → "2026" produced "2038" instead. Editing text content within images is actively harmful.
3. **The critic identifies real issues but the tool can't fix them** — tested with both manual review + re-generation and PaperBanana's automated Critic agent. In both cases, iteration 1 was better than iteration 2.
4. **Prompt quality dominates** — the variance between a good prompt and a bad prompt far exceeds the variance between iteration 1 and iteration 2 of the same prompt.

The `--input-image` editing flag is retained for rare cases where a minor color or style tweak is needed, but it should not be part of a standard workflow.

## Review Criteria (Quick Reference)

When reviewing figures (either generated or existing), check:

1. **Content accuracy** — Does the figure match what the manuscript claims it shows?
2. **Text legibility** — All labels, axis titles, and annotations readable at print size?
3. **Color accessibility** — Colorblind-safe palette? Works in grayscale?
4. **Panel labeling** — Consistent uppercase bold letters (A, B, C) in upper-left?
5. **Scale and units** — Present where needed (scale bars, axis units)?
6. **Style consistency** — Matches other figures in the manuscript set?
7. **Technical quality** — Clean lines, no artifacts, no watermarks, no AI artifacts?
8. **Caption alignment** — Figure content matches its caption description?

See [REVIEW_CRITERIA.md](REVIEW_CRITERIA.md) for the full scored checklist.

## Prompt Engineering for Scientific Figures

### The Most Important Rule

**Invest in prompt quality, not iteration.** A detailed, well-structured prompt consistently produces better results than a vague prompt followed by multiple edit passes. The first generation with a good prompt is almost always the final figure.

### Structure Prompts Spatially

The most effective pattern is to describe the figure section-by-section with explicit spatial layout:

```
A clean scientific diagram with three sections flowing left to right:

LEFT SECTION - 'Input': [detailed description of what appears here]

CENTER SECTION - 'Processing': [detailed description with specific labels,
field names, data values to include]

RIGHT SECTION - 'Output': [detailed description of output elements]

Use a white background, clean lines, sans-serif font. Blue accent color
for arrows and highlights. Publication quality.
```

This spatial structuring works for:
- Horizontal flows (LEFT / CENTER / RIGHT)
- Vertical sequences (STEP 1 / STEP 2 / STEP 3)
- Grid layouts (TOP-LEFT / TOP-RIGHT / BOTTOM-LEFT / BOTTOM-RIGHT)

### Always Include

- What the figure shows (the data or concept)
- Explicit spatial layout with section labels
- Specific content for each section (actual labels, field names, values)
- Color scheme (specify if important, or use "colorblind-safe palette")
- Style: "clean, publication-quality, white background, sans-serif labels"

### Avoid

- Vague descriptions ("make it look good")
- Requesting real data visualization (Gemini generates illustrative figures, not data plots)
- Overly complex multi-panel layouts (generate panels separately and compose)
- Expecting accurate small text (dates, code, paths will be hallucinated)

### Effective Prompts

**Good:** "A diagram with three connected sections flowing left to right: LEFT SECTION - 'Plot Creation': Show a terminal window with the command 'gg(data).aes({x: \"gene\"}).render()' and a small plot below. CENTER SECTION - 'Automatic Persistence': Show a JSON document labeled 'Plot Specification' with fields: _provenance (id, timestamp, dataFile), spec (data, aes, geoms, scales). RIGHT SECTION - 'Search and Retrieval': Show three paths: browse by date, search by type, re-render at different dimensions. White background, blue accents, sans-serif labels."

**Poor:** "Make a figure for my methods section."

See [PROMPT_TEMPLATES.md](PROMPT_TEMPLATES.md) for reusable templates by figure type.

## Composing Multi-Panel Figures

When you need a composite figure from separate images (e.g., multiple screenshots, or a mix of Gemini-generated and real output), use Python Pillow:

```python
from PIL import Image

# Load panels
panels = [Image.open(f) for f in ["panel_a.png", "panel_b.png", "panel_c.png"]]

# Normalize to same height
target_h = 1000
resized = []
for img in panels:
    ratio = target_h / img.height
    resized.append(img.resize((int(img.width * ratio), target_h), Image.LANCZOS))

# Compose side by side
pad = 30
total_w = sum(p.width for p in resized) + pad * (len(resized) - 1)
canvas = Image.new("RGB", (total_w, target_h), (0, 0, 0))  # background color

x = 0
for p in resized:
    canvas.paste(p, (x, 0))
    x += p.width + pad

canvas.save("composite.png", dpi=(300, 300))
```

**Background color tips:**
- Use **black** for dark terminal screenshots (blends seamlessly)
- Use **white** for Gemini-generated diagrams on white backgrounds
- Match the background to the dominant panel style

## Configuration

The generation script requires a Google API key:

1. Set `GOOGLE_API_KEY` environment variable, or
2. Add `GOOGLE_API_KEY=your_key` to a `.env` file in the project directory

## Related Files

- [REVIEW_CRITERIA.md](REVIEW_CRITERIA.md) - Full scored review checklist
- [PROMPT_TEMPLATES.md](PROMPT_TEMPLATES.md) - Reusable prompt templates by figure type
