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
| Small text accuracy | Dates, paths, code in small text may be hallucinated by Gemini — verify any text that is legible at print size |
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

## Cross-Figure Consistency Review

After reviewing individual figures, review the **entire figure set together**. This catches issues that per-figure review misses.

| Check | What to look for |
|-------|-----------------|
| Background colors | All conceptual diagrams should share the same background (typically white). Tool output screenshots may use dark backgrounds — note this in captions. |
| Color palette | Same accent color family across conceptual figures (e.g., all use blue accents). Data figures should use the same palette for the same variables. |
| Border/box style | Rounded vs sharp rectangles should be consistent across similar figure types. |
| Font family | Same sans-serif font across all Gemini-generated figures. |
| Figure sizing | Wide-aspect figures (e.g., 3-panel composites) need full-width placement. Verify the paper layout supports this. |
| Label conventions | Panel labels (A, B, C) should use the same style, size, and position across all figures — or be consistently absent if added manually later. |

## When Review Finds Issues

After review identifies problems, **do not attempt automated revision loops**. Instead:

1. **Accept minor issues** — small text hallucinations (wrong dates, garbled paths) in text too small to read at print size are cosmetic and not worth re-generating for.

2. **Re-generate with a better prompt** — if content or layout is wrong, improve the prompt and generate fresh. Incorporate what you learned from the failed version:
   - Be more specific about layout and spatial arrangement
   - Add explicit details that were missing or wrong
   - Include the exact text content you need at readable size

3. **Let the user decide** — present the figure with a clear issue list. The user may accept it, manually fix it in an image editor, or ask for re-generation.

**Do not use `--input-image` editing to fix issues from review.** Testing shows that Gemini's image editing is unreliable for corrections — it often introduces new errors while failing to fix the original ones. This applies to both manual edit attempts and automated critic agents (e.g., PaperBanana's Critic loop).
