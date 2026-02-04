# Figure and Table Guidelines

Technical specifications and best practices for figures and tables.

## Figure Specifications

### Resolution Requirements

| Image Type | Minimum DPI | Preferred DPI | Use Case |
|------------|-------------|---------------|----------|
| Line art | 600 | 1200 | Graphs, diagrams, flowcharts |
| Halftone | 300 | 600 | Photographs, micrographs |
| Combination | 600 | 1200 | Photos with text/lines |

**How to check resolution:**
- Photoshop: Image → Image Size → Resolution
- GIMP: Image → Print Size → Resolution
- Preview (Mac): Tools → Show Inspector

### File Formats

| Format | Best For | Notes |
|--------|----------|-------|
| TIFF | Final submission | Uncompressed, universally accepted |
| EPS | Vector graphics | Scalable, editable |
| PDF | Vector graphics | Scalable, widely supported |
| PNG | Web/draft | Lossless compression |
| JPEG | Photos only | Lossy; use maximum quality (12/12) |

**Avoid:**
- PowerPoint files (low resolution)
- Word-embedded images (compression issues)
- GIF (limited colors)
- BMP (unnecessarily large)

### Size Guidelines

| Width | Pixels at 300 DPI | Pixels at 600 DPI | Typical Use |
|-------|-------------------|-------------------|-------------|
| Single column (85mm) | 1000 | 2000 | Simple graphs |
| 1.5 column (114mm) | 1350 | 2700 | Medium complexity |
| Full width (170mm) | 2000 | 4000 | Multi-panel, complex |

**Maximum file sizes:** Typically 10-50 MB per figure (check journal)

### Color Specifications

**Color modes:**
- RGB: For online publication
- CMYK: For print publication
- Check journal requirements (often RGB accepted, converted by publisher)

**Color accessibility:**
- Avoid red-green combinations alone
- Use patterns/shapes in addition to color
- Test with colorblind simulator
- Consider grayscale compatibility

**Recommended palettes:**
- Viridis, plasma, inferno (perceptually uniform)
- ColorBrewer palettes (designed for accessibility)
- Wong color palette (colorblind-safe)

### Text in Figures

| Element | Size Range | Notes |
|---------|------------|-------|
| Axis labels | 8-12 pt | Must be readable at print size |
| Axis titles | 10-14 pt | Slightly larger than labels |
| Panel labels | 10-14 pt, bold | A, B, C consistently positioned |
| Legends | 8-12 pt | May be smaller |

**Font recommendations:**
- Sans-serif: Arial, Helvetica, Calibri
- Match manuscript font when possible
- Embed fonts in PDF/EPS

---

## Figure Best Practices

### Composition

**Do:**
- Keep designs simple and focused
- Use white space effectively
- Align elements consistently
- Group related panels logically
- Include scale bars on images

**Don't:**
- Add unnecessary 3D effects
- Use distracting backgrounds
- Include too many elements
- Use inconsistent styling across panels

### Multi-Panel Figures

**Layout options:**
```
Single row:     [A] [B] [C]

Two rows:       [A] [B]
                [C] [D]

Mixed sizes:    [A] [B]
                [  C  ]
```

**Panel labeling:**
- Position: Upper left corner, consistently
- Style: Bold, capital letters (A, B, C)
- Size: 10-14 pt
- Outside plot area when possible

### Graphs and Charts

**Axis guidelines:**
- Start at zero when meaningful
- Use appropriate scale (linear vs. log)
- Limit decimal places
- Include units in axis titles

**Data presentation:**
- Show individual data points when n < 30
- Error bars: specify type (SD, SEM, 95% CI)
- Use consistent symbols/colors across figures

**Legend placement:**
- Within figure area if space permits
- In figure caption if complex
- Consistent position across panels

### Statistical Information

**On figures:**
- Significance markers: *, **, ***, NS
- Define in caption: *p < 0.05, **p < 0.01, ***p < 0.001

**In captions:**
- Sample sizes
- Error bar definitions
- Statistical tests used
- Significance thresholds

---

## Table Specifications

### Formatting Standards

**Structure:**
```
Table 1. Descriptive title that explains the table content.
─────────────────────────────────────────────────────────
Column 1        Column 2 (unit)      Column 3 (unit)
─────────────────────────────────────────────────────────
Row 1           Value ± Error        Value (95% CI)
Row 2           Value ± Error        Value (95% CI)
Row 3           Value ± Error        Value (95% CI)
─────────────────────────────────────────────────────────
Abbreviations and footnotes below table.
```

**Rules:**
- Horizontal lines: Top, below header, bottom
- No vertical lines (typically)
- No internal horizontal lines (usually)

### Content Guidelines

**Headers:**
- Clear, concise labels
- Units in parentheses
- Abbreviations defined in footnotes

**Data cells:**
- Consistent decimal places within columns
- Align decimals vertically
- Use appropriate significant figures
- Missing data indicated (—, NA, or footnote)

**Footnotes:**
- Ordered by appearance: a, b, c or 1, 2, 3 or *, †, ‡
- Define abbreviations
- Explain special formatting
- Note statistical details

### Numerical Formatting

| Data Type | Format Example | Notes |
|-----------|----------------|-------|
| Counts | 42 | No decimals |
| Percentages | 42.3% | 1 decimal typical |
| Means ± SD | 3.45 ± 0.67 | Match precision |
| CI | (3.12–3.78) | En dash for ranges |
| P-values | 0.023, <0.001 | 3 decimals max |
| Ratios | 2.3 (1.5–3.4) | With CI if available |

### Common Table Types

**Demographic/descriptive:**
- Variable names in rows
- Groups in columns
- Include n for each group

**Results table:**
- Clear outcome variable
- Effect sizes with CI
- P-values appropriately formatted

**Comparison table:**
- Consistent structure
- Clear what's being compared
- Statistical comparisons noted

---

## Figure Caption Guidelines

### Structure
```
Figure 1. Brief title stating the main message.
(A) Description of panel A. (B) Description of panel B.
Abbreviations defined here. Statistical details: test used,
significance thresholds. Error bars represent [SD/SEM/95% CI].
n = X per group.
```

### Content Checklist
- [ ] Standalone description (interpretable without text)
- [ ] All panels described
- [ ] All abbreviations defined
- [ ] Statistical markers explained
- [ ] Sample sizes included
- [ ] Error bar type specified
- [ ] Scale bar described (if present)

---

## Table Title Guidelines

### Structure
```
Table 1. Descriptive title summarizing table contents
```

### Content
- Self-explanatory
- Indicates what is being compared
- Includes sample information if relevant
- No period at end (typically)

---

## Quality Checklist

### Figures
- [ ] Resolution sufficient for print
- [ ] Correct file format
- [ ] Size appropriate for column width
- [ ] Text readable at final size
- [ ] Colors accessible
- [ ] All elements labeled
- [ ] Scale bars included
- [ ] Consistent styling across all figures

### Tables
- [ ] Clear, descriptive title
- [ ] Logical organization
- [ ] Consistent formatting
- [ ] Appropriate precision
- [ ] Units included
- [ ] Abbreviations defined
- [ ] Statistical details included
- [ ] No unnecessary complexity

### Final Review
- [ ] Figures match descriptions in text
- [ ] Tables match descriptions in text
- [ ] Numbering is sequential
- [ ] Cross-references are correct
- [ ] File names follow guidelines
