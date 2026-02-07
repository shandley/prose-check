# Prompt Templates for Scientific Figures

Reusable templates for common scientific figure types. Each template includes the scientific style preamble and placeholders (in `{BRACKETS}`) for manuscript-specific content.

## Style Preamble

All scientific figure prompts should start with this preamble (applied automatically by `--style scientific`):

> Create a clean, publication-quality scientific figure. Use a white background, high contrast, and sans-serif font labels (Arial or Helvetica). No watermarks, no decorative elements. Ensure all text is legible at print size (minimum 8pt equivalent). Use a colorblind-safe color palette.

## Architecture / Workflow Diagrams

### Linear Workflow

```
A horizontal workflow diagram with {N} steps flowing left to right.
Step 1: {STEP_1_LABEL} represented by {STEP_1_ICON}.
Step 2: {STEP_2_LABEL} represented by {STEP_2_ICON}.
Step 3: {STEP_3_LABEL} represented by {STEP_3_ICON}.
Connect steps with directional arrows. Each step is in a rounded rectangle
with the label below. Use {COLOR_SCHEME} color scheme. White background,
clean sans-serif labels.
```

**Example:**
```
A horizontal workflow diagram with 4 steps flowing left to right.
Step 1: "Sample Collection" represented by a test tube icon.
Step 2: "DNA Extraction" represented by a double helix icon.
Step 3: "Library Prep" represented by a DNA fragment icon.
Step 4: "Sequencing" represented by a sequencing machine icon.
Connect steps with directional arrows. Each step is in a rounded rectangle
with the label below. Use blue-to-teal gradient color scheme. White background,
clean sans-serif labels.
```

### Branching Pipeline

```
A flowchart showing a bioinformatic pipeline. Start with {INPUT} at the top.
The pipeline branches into {BRANCH_COUNT} parallel paths:
Left path: {LEFT_STEPS}.
Right path: {RIGHT_STEPS}.
Paths converge at {CONVERGENCE_STEP}.
Final output: {OUTPUT}.
Use rectangular boxes for processing steps, diamond shapes for decision points,
and rounded rectangles for inputs/outputs. {COLOR_SCHEME} palette.
```

## Data Visualizations

### Bar Chart

```
A bar chart comparing {VARIABLE} across {N} conditions: {CONDITION_LIST}.
Y-axis: "{Y_LABEL} ({UNITS})". X-axis: "{X_LABEL}".
Include error bars representing {ERROR_TYPE}.
{SIGNIFICANCE_MARKERS}.
Use distinct colors from a colorblind-safe palette for each condition.
Clean white background, no gridlines, sans-serif labels.
```

**Example:**
```
A bar chart comparing gene expression across 3 conditions: Wild Type, Knockout, Rescue.
Y-axis: "Relative Expression (fold change)". X-axis: "Genotype".
Include error bars representing standard error of the mean.
Add significance brackets: ** between WT and KO, ns between WT and Rescue.
Use distinct colors from a colorblind-safe palette for each condition.
Clean white background, no gridlines, sans-serif labels.
```

### Scatter Plot

```
A scatter plot showing the relationship between {X_VARIABLE} and {Y_VARIABLE}.
X-axis: "{X_LABEL} ({X_UNITS})". Y-axis: "{Y_LABEL} ({Y_UNITS})".
Data points colored by {GROUP_VARIABLE}: {GROUP_LIST}.
Include a {TREND_LINE} trend line.
Add R-squared value and p-value in the upper right corner.
Legend in the {LEGEND_POSITION}. Colorblind-safe palette.
```

### Heatmap

```
A heatmap showing {DATA_DESCRIPTION}.
Rows: {ROW_LABELS}. Columns: {COLUMN_LABELS}.
Use the {COLORMAP} colormap (e.g., viridis, plasma, blue-white-red diverging).
Include a color bar with label: "{COLORBAR_LABEL}".
Add dendrograms on {DENDROGRAM_SIDES} for hierarchical clustering.
Row and column labels in {FONT_SIZE}pt sans-serif.
```

## Multi-Panel Comparison Figures

### Two-Panel Side by Side

```
A two-panel figure labeled A and B.
Panel A ({PANEL_A_WIDTH}): {PANEL_A_DESCRIPTION}.
Panel B ({PANEL_B_WIDTH}): {PANEL_B_DESCRIPTION}.
Panel labels in bold uppercase, upper-left corner of each panel.
Consistent font sizes and color scheme across panels.
White background, clean layout with minimal spacing between panels.
```

### Four-Panel Grid

```
A four-panel figure in a 2x2 grid, labeled A-D.
Panel A (top-left): {PANEL_A_DESCRIPTION}.
Panel B (top-right): {PANEL_B_DESCRIPTION}.
Panel C (bottom-left): {PANEL_C_DESCRIPTION}.
Panel D (bottom-right): {PANEL_D_DESCRIPTION}.
Bold uppercase panel labels in upper-left corner.
Shared {SHARED_AXIS} axis where applicable.
Consistent styling, colorblind-safe palette, white background.
```

### Mixed-Size Panels

```
A figure with {N} panels in a mixed layout:
Top row: Panel A ({WIDTH_A}) and Panel B ({WIDTH_B}) side by side.
Bottom: Panel C spanning the full width.
Panel A: {PANEL_A_DESCRIPTION}.
Panel B: {PANEL_B_DESCRIPTION}.
Panel C: {PANEL_C_DESCRIPTION}.
Bold uppercase panel labels. Consistent font sizes throughout.
```

## Phylogenetic Trees

### Basic Tree

```
A phylogenetic tree with {N} terminal taxa.
Tree topology: {TOPOLOGY_DESCRIPTION}.
{TREE_STYLE} tree layout (rectangular/circular/unrooted).
Bootstrap support values shown at major nodes (>70%).
Scale bar showing {SCALE_UNITS}.
{HIGHLIGHT_DESCRIPTION}.
Clean black lines on white background, sans-serif taxon labels.
```

**Example:**
```
A phylogenetic tree with 12 terminal taxa representing beetle families.
Rectangular tree layout with branches of varying length.
Bootstrap support values shown at major nodes (>70%) in small gray text.
Scale bar showing 0.1 substitutions per site.
Highlight the Scarabaeidae clade with a blue background shading.
Mark the branch leading to Scarabaeidae with a red asterisk for positive selection.
Clean black lines on white background, sans-serif taxon labels in 10pt.
```

### Gene Tree with Domain Architecture

```
A phylogenetic tree on the left side with {N} sequences.
To the right of each taxon label, show the protein domain architecture
as colored blocks: {DOMAIN_DESCRIPTIONS}.
Include a domain legend at the bottom.
Scale bar for tree branch lengths.
Align domain architectures to the same starting position.
```

## Protein / Molecular Structures

### Membrane Protein

```
A schematic of {PROTEIN_NAME} embedded in a lipid bilayer membrane.
Show {N} transmembrane helices as colored cylinders spanning the membrane.
The membrane is represented as two parallel lines with lipid tails.
Label key residues: {RESIDUE_LIST}.
Highlight the {BINDING_SITE} binding pocket in {HIGHLIGHT_COLOR}.
N-terminus labeled on the {N_TERM_SIDE} side, C-terminus on the {C_TERM_SIDE} side.
Clean scientific illustration style.
```

### Protein Domain Diagram

```
A linear protein domain diagram for {PROTEIN_NAME} ({LENGTH} amino acids).
Draw as a horizontal bar with domains colored and labeled:
{DOMAIN_1}: positions {START_1}-{END_1}, colored {COLOR_1}.
{DOMAIN_2}: positions {START_2}-{END_2}, colored {COLOR_2}.
Number scale along the bottom showing amino acid positions.
Key mutations marked with arrows: {MUTATION_LIST}.
Clean style, sans-serif labels.
```

## Conceptual / Model Figures

### Signaling Pathway

```
A schematic of the {PATHWAY_NAME} signaling pathway.
Show {COMPONENT_LIST} as labeled shapes.
Arrows indicate activation, flat-headed arrows indicate inhibition.
The pathway flows from {START} at the top to {END} at the bottom.
Highlight the {STEP} step where {INTERVENTION} occurs.
Use a minimal color scheme: activators in {ACT_COLOR}, inhibitors in {INH_COLOR}.
Clean white background, publication-quality.
```

### Study Design Overview

```
A schematic showing the experimental design.
{N} groups: {GROUP_LIST}.
Timeline flows left to right: {TIMELINE_STEPS}.
Sample sizes noted: n = {SAMPLE_SIZES}.
Key timepoints marked: {TIMEPOINTS}.
Use icons for {ICON_ELEMENTS}.
Clean layout with consistent spacing, sans-serif labels throughout.
```

## Three-Section System Diagram

Best for showing systems with input → processing → output flow. This pattern produced excellent results for architecture and provenance diagrams.

```
A clean scientific diagram showing {SYSTEM_NAME} with three connected
sections flowing left to right:

LEFT SECTION - '{LEFT_TITLE}': {LEFT_DESCRIPTION}. Label: '{LEFT_LABEL}'.

CENTER SECTION - '{CENTER_TITLE}': {CENTER_DESCRIPTION}. Include specific
details like {FIELD_NAMES_OR_COMPONENTS}.

RIGHT SECTION - '{RIGHT_TITLE}': {RIGHT_DESCRIPTION}. Show {OUTPUT_ELEMENTS}.

Use a white background, clean lines, sans-serif font (Arial/Helvetica),
minimal color ({ACCENT_COLOR} accent for arrows/highlights), and no
decorative elements. Publication quality for a software paper.
```

**Example (produced a publication-quality figure on first generation):**
```
A clean scientific diagram showing the ggterm plot provenance system
with three connected sections flowing left to right:

LEFT SECTION - 'Plot Creation': Show a terminal window with the command
'gg(data).aes({x: "gene", y: "expression"}).geom(geom_volcano()).render()'
and a small plot icon below. Label: 'Terminal Rendering'.

CENTER SECTION - 'Automatic Persistence': Show a JSON document labeled
'Plot Specification' containing fields: _provenance (id: "2026-01-31-029",
timestamp, dataFile, command, geomTypes), spec (data, aes, geoms, scales).
Below it, a file icon labeled 'history.jsonl' as 'Append-only index'.
Show an arrow from the terminal labeled 'auto-save'.

RIGHT SECTION - 'Search and Retrieval': Show three paths: 'Browse by date'
with a calendar icon, 'Search by type' with filter checkboxes,
'Re-render' with dimension controls and 'Export to Vega-Lite'.

White background, blue accents, sans-serif labels. Publication quality.
```

## Vertical Conversational Workflow

Best for showing iterative user-AI interaction or step-by-step processes. Works well with numbered steps and chat-bubble styling.

```
A clean scientific diagram showing {WORKFLOW_NAME} as a vertical sequence
with {N} steps flowing top to bottom:

STEP 1 - '{STEP_1_TITLE}': Show a chat bubble from the user (left side)
saying '{USER_REQUEST}'. Label: '1. {STEP_1_LABEL}'.

STEP 2 - '{STEP_2_TITLE}': Show a response bubble (right side)
containing {AI_RESPONSE}. Below it show {VISUAL_ELEMENT}. Label: '2. {STEP_2_LABEL}'.

STEP 3 - '{STEP_3_TITLE}': Show another user request '{REFINEMENT}'
and the updated response. Label: '3. {STEP_3_LABEL}'.

STEP 4 - '{STEP_4_TITLE}': Show {FINAL_OUTPUT}. Label: '4. {STEP_4_LABEL}'.

{OPTIONAL_SIDE_ELEMENT} on the right side spanning all steps.

White background, light blue for user bubbles, light gray for AI bubbles.
Sans-serif font. Publication quality.
```

## Tips for Using Templates

1. **Replace all placeholders** - Every `{BRACKET}` value must be filled with manuscript-specific content
2. **Be specific about numbers** - "5 bars" not "several bars"
3. **Name colors explicitly** - "blue and orange" not "different colors"
4. **Specify text content** - Write out the actual labels you want, don't describe them
5. **One concept per figure** - Split complex ideas across panels rather than one dense image
6. **Invest in the prompt, not iteration** - A detailed first prompt consistently beats a vague prompt + multiple edit passes. The first generation is often the final figure.
7. **Use spatial structure** - Always describe layout section-by-section (LEFT/CENTER/RIGHT or STEP 1/2/3). This is the single most effective prompting technique.
8. **Accept small text imperfections** - Gemini hallucinates details in small text (dates, file paths, code). If the text is too small to read at print size, don't waste time trying to fix it.
9. **Generate panels separately for composites** - For multi-panel figures mixing different content types (e.g., Gemini diagrams + real screenshots), generate each panel separately and compose with Python Pillow.
