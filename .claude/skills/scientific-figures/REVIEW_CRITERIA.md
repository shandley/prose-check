# Figure Review Criteria

Scored checklist for evaluating scientific figures. Use when reviewing generated or existing figures for publication readiness.

## Scoring

Rate each criterion: **Pass** (meets standard), **Warn** (minor issue), or **Fail** (must fix).

A figure is **publication-ready** when all criteria pass. Figures with any **Fail** require revision. Figures with only **Warn** items may be acceptable depending on journal requirements.

## Criteria

### 1. Content Accuracy

Does the figure accurately represent what the manuscript claims it shows?

| Check | What to look for |
|-------|-----------------|
| Claims match | Figure content corresponds to manuscript text references |
| Data representation | Visual elements correctly represent the described data or concept |
| No misleading elements | Nothing in the figure contradicts manuscript statements |
| Completeness | All components mentioned in the caption are present |

### 2. Text Legibility

Are all text elements readable at final print size?

| Check | Standard |
|-------|----------|
| Axis labels | 8-12 pt at print size, readable without zooming |
| Axis titles | 10-14 pt, slightly larger than labels |
| Panel labels | 10-14 pt, bold, clearly visible |
| Legend text | 8-12 pt minimum |
| Annotations | Readable without squinting at single-column width (85mm) |
| Font choice | Sans-serif (Arial, Helvetica, Calibri) |
| Font consistency | Same font family throughout figure and across figure set |

### 3. Color Accessibility

Is the figure accessible to colorblind readers and usable in grayscale?

| Check | Standard |
|-------|----------|
| No red-green only | Information not conveyed solely by red vs. green |
| Redundant coding | Patterns, shapes, or labels supplement color |
| Sufficient contrast | Adjacent colors distinguishable |
| Grayscale fallback | Key information survives grayscale conversion |
| Recommended palettes | Viridis, ColorBrewer, or Wong palette preferred |

### 4. Panel Labeling

For multi-panel figures, are panels labeled consistently?

| Check | Standard |
|-------|----------|
| Label style | Uppercase bold letters: **A**, **B**, **C** |
| Label position | Upper-left corner of each panel, consistently placed |
| Label size | 10-14 pt bold |
| Placement | Outside plot area when possible |
| Sequential | Labels follow reading order (left-to-right, top-to-bottom) |

### 5. Scale and Units

Are scales and units present where needed?

| Check | Standard |
|-------|----------|
| Axis units | Units in parentheses on all axes: "Length (mm)" |
| Scale bars | Present on micrographs, maps, and images |
| Numerical scale | Appropriate range (starts at zero when meaningful) |
| Log scale labeled | Clearly marked when log scale is used |
| Consistent units | Same units used across panels for comparable data |

### 6. Style Consistency

Does the figure match the style of other figures in the manuscript?

| Check | Standard |
|-------|----------|
| Color scheme | Same palette across all figures |
| Font | Same typeface and sizing conventions |
| Line weights | Consistent thickness across figures |
| Symbol use | Same symbols for same conditions across figures |
| Layout conventions | Consistent margins, spacing, panel sizing |

### 7. Technical Quality

Is the image technically sound for publication?

| Check | Standard |
|-------|----------|
| Resolution | Line art: 600+ DPI, photos: 300+ DPI |
| Clean lines | No jagged edges, pixelation, or compression artifacts |
| No watermarks | Free of any overlay text or watermarks |
| No AI artifacts | No extra fingers, garbled text, or hallucinated elements |
| White background | Clean white (or intentional) background |
| File format | PNG for draft, TIFF/EPS/PDF for final submission |
| File size | Within journal limits (typically 10-50 MB per figure) |

### 8. Caption Alignment

Does the figure content match its caption?

| Check | Standard |
|-------|----------|
| All panels described | Caption mentions every panel (A, B, C...) |
| Content matches | What the caption says matches what the figure shows |
| Abbreviations defined | All abbreviations in figure are defined in caption |
| Statistics noted | Error bar type, significance markers explained |
| Sample sizes | n values included where relevant |
| Standalone | Caption + figure interpretable without reading main text |

## Review Report Template

When reporting review results, use this format:

```
## Figure Review: [filename]

**Overall:** PASS / NEEDS REVISION / FAIL

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Content accuracy | Pass/Warn/Fail | ... |
| Text legibility | Pass/Warn/Fail | ... |
| Color accessibility | Pass/Warn/Fail | ... |
| Panel labeling | Pass/Warn/Fail | ... |
| Scale and units | Pass/Warn/Fail | ... |
| Style consistency | Pass/Warn/Fail | ... |
| Technical quality | Pass/Warn/Fail | ... |
| Caption alignment | Pass/Warn/Fail | ... |

**Action items:**
1. [Specific fix needed]
2. [Specific fix needed]
```

## Revision Strategy: Edit vs Re-generate

Gemini's multi-turn image editing is **conservative** - it preserves the original composition and makes incremental changes. Before building a revision prompt, classify each failed criterion:

### Edit-fixable issues (use `--input-image`)

These work well with multi-turn editing:
- Color changes (e.g., swap red-green to blue-orange)
- Text size adjustments
- Adding small elements (labels, annotations, scale bars)
- Style tweaks (background color, line weight)
- Minor additions that don't change layout

### Re-generate issues (use a new prompt from scratch)

These require a fresh generation with an improved prompt:
- Layout or arrangement changes (e.g., rearranging panels, changing flow direction)
- Structural changes to diagrams (e.g., changing arrow directions, adding/removing major components)
- Fundamentally different composition
- Completely different visual approach

**Rule of thumb:** If the issue is "add/change something within the existing layout," edit. If the issue is "the layout itself is wrong," re-generate with a better prompt.

## Building Revision Prompts from Review

### For edits (surface fixes)

When using `--input-image` for editing:

1. Starting with "Edit this figure:"
2. Listing each failed criterion as a specific instruction
3. Being concrete: "increase axis label font to 12pt" not "make text bigger"
4. Prioritizing: fix Fail items first, then Warn items
5. Keep to 2-3 changes per edit pass - more changes are more likely to be ignored

**Example edit prompt:**
```
Edit this figure: (1) Increase all axis labels to at least 10pt font.
(2) Change the red and green bars to blue and orange for colorblind accessibility.
(3) Add units to the y-axis: "Expression level (TPM)".
```

### For re-generation (structural fixes)

When re-generating from scratch:

1. Start from the original prompt that produced the best version
2. Add the structural fixes directly into the prompt description
3. Be more specific about layout, arrangement, and flow direction
4. Include details you learned from the failed version (what worked, what didn't)

**Example:** If the original prompt produced good content but wrong arrow flow, don't edit - instead re-generate with explicit flow directions baked into the prompt.
