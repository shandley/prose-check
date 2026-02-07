# Citation Format Detection

Reference for identifying citation and bibliography formats in manuscripts.

## Inline Citation Systems

### Author-Year Systems

**APA style** — parenthetical with comma:
```
(Smith, 2024)
(Smith & Jones, 2024)
(Smith et al., 2024)
```

**Harvard style** — parenthetical without comma:
```
(Smith 2024)
(Smith and Jones 2024)
(Smith et al. 2024)
```

**Narrative (integral) citations** — author as grammatical subject:
```
Smith (2024) demonstrated...
Smith and Jones (2024) found...
According to Smith et al. (2024),...
```

**Detection patterns:**
- Look for `(Surname, YYYY)` or `(Surname YYYY)` in body text
- Multiple citations: `(Smith, 2024; Jones, 2023)` or `(Smith 2024; Jones 2023)`
- Narrative form: `Surname (YYYY)` followed by a verb

### Numbered Systems

**Vancouver / NLM** — bracketed numbers:
```
...as shown previously [1].
...reported in several studies [1,2].
...across the literature [1-3].
```

**Superscript** — raised numbers:
```
...as shown previously.¹
...reported in several studies.¹,²
...across the literature.¹⁻³
```

**Detection patterns:**
- Look for `[N]`, `[N,N]`, or `[N-N]` in body text
- Superscript Unicode characters: `¹²³⁴⁵⁶⁷⁸⁹⁰`
- Numbers appear sequentially (first citation is [1], next new one is [2], etc.)

### Less Common Systems

**Footnote-based (Chicago Notes):**
- Superscript numbers linked to footnotes at page bottom
- Full citation in first footnote, shortened form thereafter

**Author-number hybrid:**
- `Smith [1]` — author name with bracketed number

## Bibliography Format Detection

### Numbered List (Vancouver Style)

```markdown
1. Smith J, Jones K. Article title. Journal Name. 2024;12(3):45-50.
2. Johnson A. Book Title. Publisher; 2023.
```

Pattern: Lines starting with `N.` followed by author names.

### Hanging Indent / Author-Year List (APA/Harvard)

```markdown
Smith, J., & Jones, K. (2024). Article title. *Journal Name*, *12*(3), 45-50.
Johnson, A. (2023). *Book Title*. Publisher.
```

Pattern: Lines starting with `Surname, Initial.` followed by `(YYYY)`.

### Bullet List (Informal Markdown)

```markdown
- Smith, J. (2024). Article title. Journal Name, 12(3), 45-50.
- Johnson, A. (2023). Book Title. Publisher.
```

Pattern: Lines starting with `-` or `*` followed by citation content.

### BibTeX Blocks

```bibtex
@article{smith2024,
  author = {Smith, John and Jones, Karen},
  title = {Article Title},
  journal = {Journal Name},
  year = {2024},
  volume = {12},
  pages = {45--50}
}
```

Pattern: Lines starting with `@type{key,` — typically in a separate `.bib` file.

## Building the Citation–Bibliography Map

### Step 1: Identify the Citation System

Read the first 3-5 inline citations. Determine system from this table:

| Pattern Found | System | Bibliography Expects |
|---------------|--------|---------------------|
| `(Smith, 2024)` | APA author-year | Author-year reference list |
| `(Smith 2024)` | Harvard author-year | Author-year reference list |
| `Smith (2024)` | Narrative author-year | Author-year reference list |
| `[1]` or `[1,2]` | Vancouver numbered | Numbered reference list |
| Superscript `¹` | Superscript numbered | Numbered reference list |

### Step 2: Extract Inline Citations

**For author-year systems:**
1. Scan body text for all parenthetical citations: `(Surname...YYYY)`
2. Scan for narrative citations: `Surname (YYYY)`
3. Normalize each to a key: `Smith2024`, `SmithJones2024`, `Smithetal2024`
4. Record location (section, paragraph) for each occurrence

**For numbered systems:**
1. Scan body text for all bracket references: `[N]`
2. Record the number and location of each
3. Note the highest number used — bibliography should have at least that many entries

### Step 3: Extract Bibliography Entries

1. Find the References/Bibliography section
2. Parse each entry to extract:
   - Author surname(s)
   - Year of publication
   - Title (for disambiguation)
3. Generate matching keys: `Smith2024`, `SmithJones2024`
4. For numbered systems, record the entry number

### Step 4: Cross-Reference

Build two lists and compare:

```
INLINE CITATIONS (from body)     BIBLIOGRAPHY ENTRIES (from ref list)
├── Smith2024        ──────────► ├── Smith2024           ✓ matched
├── Jones2023        ──────────► ├── Jones2023           ✓ matched
├── Lee2024          ─── ✗       │                       ✗ cited but not listed
│                                ├── Adams2022           ✗ listed but not cited
└── Wangetal2023     ──────────► └── Wangetal2023        ✓ matched
```

## Informal Mention Detection

### What to Look For

Informal mentions are author names in body text without a formal citation:

```
❌ "As Tufte argued, data-ink ratio matters."          ← no citation
✓  "As Tufte (2001) argued, data-ink ratio matters."   ← proper citation
```

### Detection Procedure

1. **Build a surname list** from the bibliography entries
2. **Scan body text** for each surname appearing outside of:
   - Parenthetical citations `(...)`
   - The bibliography/references section itself
   - Author contribution statements
   - Acknowledgments
3. **Flag instances** where a surname appears in running text without an adjacent formal citation
4. **Check context** — some mentions are legitimate:
   - "the Smith method" (referring to a well-known method, citation may be elsewhere)
   - Author names in tables or figure legends (may cite differently)

### Common Informal Mention Patterns

| Pattern | Example | Action |
|---------|---------|--------|
| Name + claim, no citation | "Tufte argued that..." | Add citation |
| Name + possessive | "Smith's framework" | Add citation if first mention |
| "According to Name" | "According to Lee,..." | Add citation |
| Name in apposition | "...the approach of Wang..." | Add citation |
| Name as adjective | "Bayesian methods" | Skip — not a citation need |
