---
name: bibliography
description: Audit, fix, and format bibliographies for academic manuscripts. Cross-references inline citations against the reference list to find orphans in both directions. Complements scientific-style (citation prose quality) and submission-prep (formatting checklists).
argument-hint: [audit manuscript.md or format --style apa manuscript.md]
---

# Bibliography Skill

Audit, fix, and format bibliographies for academic manuscripts.

## When to Use This Skill

- Checking that every inline citation has a matching bibliography entry
- Finding bibliography entries that are never cited in the text
- Catching informal author mentions that lack formal citations
- Standardizing reference formatting to a target style (APA, Vancouver, Chicago)
- Preparing a manuscript for submission (pair with `submission-prep`)

**Combine with:** `scientific-style` for citation prose quality (reporting verbs, integral vs. non-integral), `submission-prep` for journal-specific formatting requirements.

## Three Modes

### 1. Audit Mode (default)

Perform a bidirectional cross-reference check. This is the core function.

**Invoke with:** `/bibliography audit manuscript.md`

**Procedure:**

1. **Identify the citation system** — Read the first 3-5 inline citations. Classify as author-year (APA/Harvard), numbered (Vancouver), or other. See [CITATION_FORMATS.md](CITATION_FORMATS.md).

2. **Extract all inline citations** — Scan the entire body text (everything above the References/Bibliography section). For author-year systems, capture both parenthetical `(Smith, 2024)` and narrative `Smith (2024)` forms. For numbered systems, capture all `[N]` references. Normalize each to a lookup key.

3. **Extract all bibliography entries** — Parse the References section. Extract author surname(s), year, and title from each entry. Generate matching lookup keys.

4. **Cross-reference: citations → bibliography** — For each inline citation, find the matching bibliography entry. Record any citations that have no match ("cited but not listed").

5. **Cross-reference: bibliography → citations** — For each bibliography entry, find at least one matching inline citation. Record any entries with no match ("listed but not cited").

6. **Scan for informal mentions** — Build a surname list from the bibliography. Scan body text for these surnames appearing outside of formal citations. Flag instances like "Tufte argued that..." where a formal citation is missing.

7. **Generate the audit report** — Use the template in [AUDIT_REPORT_TEMPLATE.md](AUDIT_REPORT_TEMPLATE.md). Include counts, status assessment, and specific issues with locations.

**The bidirectional check:**

```
  BODY TEXT                          BIBLIOGRAPHY
  ─────────                          ────────────
  (Smith, 2024)  ──────────────────► Smith, J. (2024)...     ✓
  (Jones, 2023)  ──────────────────► Jones, K. (2023)...     ✓
  Lee (2024)     ───── ? ──────────►                         ✗ CITED BUT NOT LISTED
                                     Adams, R. (2022)...     ✗ LISTED BUT NOT CITED
  "Tufte argued" ─── informal ─────►                         ⚠ INFORMAL MENTION
```

### 2. Fix Mode

Resolve issues found during audit. Always run audit first.

**Invoke with:** `/bibliography fix manuscript.md`

**Procedure:**

1. **Run audit** (if not already done) to identify all issues.

2. **Cited but not listed** — For each missing entry:
   - Search for the full reference details in the manuscript context (footnotes, supplementary material, or related files)
   - If details are available, add a properly formatted entry to the bibliography
   - If details are unknown, add a placeholder: `[TODO: Complete reference for Smith (2024)]`
   - Place the entry in correct order (alphabetical for author-year, sequential for numbered)

3. **Listed but not cited** — For each orphaned entry:
   - Read the entry's title and topic
   - Scan the manuscript for passages where this reference is relevant
   - If a relevant passage exists, add an inline citation at the appropriate location
   - If no relevant passage exists, flag the entry for potential removal but do NOT remove automatically — the author may intend to cite it in a future revision

4. **Informal mentions** — For each informal mention:
   - Identify the referenced work (match to bibliography or determine the needed reference)
   - Convert to a formal citation: "Tufte argued..." → "Tufte (2001) argued..."
   - If the work is not in the bibliography, add it (see step 2)

5. **Re-run audit** to verify all issues are resolved. Report the before/after comparison.

### 3. Format Mode

Validate and standardize reference formatting to a target style.

**Invoke with:** `/bibliography format --style apa manuscript.md`

**Procedure:**

1. **Identify the target style** — Use the `--style` flag (apa, vancouver, chicago) or detect from the manuscript. See [REFERENCE_STYLES.md](REFERENCE_STYLES.md).

2. **Check each bibliography entry** against the target style rules:
   - Author name format (initials vs. full names, punctuation)
   - Year placement
   - Title capitalization (sentence case vs. title case)
   - Journal name formatting (italics, abbreviation)
   - Volume/issue/page format
   - DOI format
   - Punctuation and ordering

3. **Check inline citations** for style consistency:
   - Correct use of `&` vs. `and`
   - Correct et al. threshold
   - Correct punctuation within parenthetical citations

4. **Report issues** with specific entries and the required corrections.

5. **Apply corrections** if requested, preserving the semantic content while fixing formatting.

## Boundary with Other Skills

| Concern | Skill |
|---------|-------|
| Whether a citation exists and is linked to a bibliography entry | **bibliography** |
| Reference formatting correctness (APA, Vancouver, etc.) | **bibliography** |
| How to integrate a citation into prose (integral vs. non-integral) | scientific-style |
| Reporting verb choice ("found" vs. "demonstrated") | scientific-style |
| Overall submission checklist (figures, cover letter, etc.) | submission-prep |
| Claim calibration (hedging strength) | scientific-style |

## Common Problems

| Problem | Detection | Fix |
|---------|-----------|-----|
| Cited but not listed | Citation in text, no matching bibliography entry | Add bibliography entry |
| Listed but not cited | Bibliography entry, no inline citation | Add citation or flag for removal |
| Informal mention | Author surname in text without `(YYYY)` | Convert to formal citation |
| Duplicate entries | Same work listed twice with slight variations | Merge into single entry |
| Inconsistent style | Mix of APA and Vancouver formatting | Standardize to one style |
| Wrong et al. usage | Too few authors for et al. (APA: need 3+) | List all authors or use correct threshold |
| Broken numbering | Vancouver numbers skip or repeat | Renumber sequentially |
| Year mismatch | Inline says 2024, bibliography says 2023 | Verify correct year and fix |
| Author name mismatch | Inline says "Smith" but entry is "Smyth" | Verify correct spelling |

## Handling Edge Cases

### Multiple Works by Same Author in Same Year
- APA: `(Smith, 2024a)` and `(Smith, 2024b)` — add letter suffixes
- Vancouver: separate numbers, no special handling needed
- Chicago: `(Smith 2024a)` and `(Smith 2024b)`

### Secondary Citations (Citing Through Another Work)
- APA: `(Smith, 2020, as cited in Jones, 2024)` — only Jones appears in bibliography
- Flag if Smith also appears in bibliography (redundant)

### Works with No Author
- APA: Use title in citation: `("Article Title," 2024)`
- Vancouver: Organization name or title
- Match carefully — these are easy to miss in cross-referencing

### Manuscripts with .bib Files
- Check the `.bib` file for all entries
- Also check the rendered bibliography (some `.bib` entries may not be `\cite`d)
- Keys like `\cite{smith2024}` map to `@article{smith2024,...}` in the `.bib` file

## Quality Checks

Before finalizing any bibliography work:

- [ ] Every inline citation matches exactly one bibliography entry
- [ ] Every bibliography entry is cited at least once
- [ ] No informal author mentions without formal citations
- [ ] Entries follow a single, consistent style
- [ ] Entry ordering matches the style (alphabetical or by appearance)
- [ ] Author names are spelled consistently between inline citations and bibliography
- [ ] Years match between inline citations and bibliography entries
- [ ] For numbered systems: numbers are sequential with no gaps or duplicates
- [ ] For author-year systems: entries with same author/year have letter suffixes (a, b, c)
- [ ] DOIs are included where available

## Related Files

- [CITATION_FORMATS.md](CITATION_FORMATS.md) — Detection patterns for citation and bibliography formats
- [REFERENCE_STYLES.md](REFERENCE_STYLES.md) — APA, Vancouver, Chicago formatting rules
- [AUDIT_REPORT_TEMPLATE.md](AUDIT_REPORT_TEMPLATE.md) — Structured output template for audit results
