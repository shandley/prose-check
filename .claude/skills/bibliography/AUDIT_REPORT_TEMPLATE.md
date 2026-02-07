# Bibliography Audit Report Template

Use this template to structure audit output. Fill in each section systematically.

## Report Template

```markdown
# Bibliography Audit Report

**Manuscript:** [filename]
**Citation system detected:** [APA author-year / Harvard author-year / Vancouver numbered / other]
**Date:** [YYYY-MM-DD]

## Summary

| Metric | Count |
|--------|-------|
| Inline citations (unique) | X |
| Bibliography entries | X |
| Matched (citation ↔ entry) | X |
| Cited but not listed | X |
| Listed but not cited | X |
| Informal mentions | X |
| Formatting issues | X |

**Status:** [PASS / NEEDS ATTENTION / FAIL]

- **PASS** — All citations matched, no orphans, formatting consistent
- **NEEDS ATTENTION** — Minor issues (1-3 formatting inconsistencies, or 1-2 orphans)
- **FAIL** — Structural problems (missing entries, uncited references, format mix)

---

## 1. Cited but Not Listed

References cited in body text with no matching bibliography entry.

| # | Citation | Location | Suggested Action |
|---|----------|----------|-----------------|
| 1 | Smith (2024) | Methods, para 3 | Add to bibliography |
| 2 | [example] | [section] | [action] |

_If none: "No issues found."_

## 2. Listed but Not Cited

Bibliography entries with no matching inline citation.

| # | Entry | Suggested Action |
|---|-------|-----------------|
| 1 | Adams, J. (2022). Title... | Add citation where relevant OR remove |
| 2 | [example] | [action] |

_If none: "No issues found."_

## 3. Informal Mentions

Author names appearing in body text without formal citations.

| # | Mention | Context | Suggested Action |
|---|---------|---------|-----------------|
| 1 | "Tufte argued that..." | Results, para 2 | Add Tufte (YYYY) citation |
| 2 | [example] | [section] | [action] |

_If none: "No issues found."_

## 4. Formatting Issues

Inconsistencies in reference formatting.

| # | Entry | Issue | Fix |
|---|-------|-------|-----|
| 1 | Smith, J. (2024)... | Title in Title Case, should be sentence case (APA) | Lowercase non-proper nouns |
| 2 | [example] | [issue] | [fix] |

_If none: "No issues found."_

---

## Verification Checklist

- [ ] Every inline citation has a matching bibliography entry
- [ ] Every bibliography entry has at least one inline citation
- [ ] No author names appear in body text without formal citations
- [ ] All entries follow the same reference style
- [ ] Entries are ordered correctly (alphabetical or by appearance)
- [ ] Author name format is consistent across entries
- [ ] Year format is consistent
- [ ] Journal names consistently formatted (abbreviated or full)
- [ ] DOIs included where available
```

## Status Criteria

| Status | Conditions |
|--------|-----------|
| **PASS** | 0 cited-but-not-listed AND 0 listed-but-not-cited AND 0 informal mentions AND ≤1 formatting issue |
| **NEEDS ATTENTION** | 1-2 orphans in either direction OR 1-3 informal mentions OR 2-4 formatting issues |
| **FAIL** | 3+ orphans OR mixed citation systems OR systematic formatting problems |

## Worked Example

Given a manuscript with these inline citations:
```
Body text mentions: (Smith, 2024), (Jones, 2023), Lee (2024),
                    (Wang et al., 2023), "Tufte argued..."
```

And this bibliography:
```
1. Smith, J. (2024). Title A. Journal X, 12, 1-10.
2. Jones, K. (2023). Title B. Journal Y, 8, 20-30.
3. Wang, F., et al. (2023). Title C. Journal Z, 5, 40-50.
4. Adams, R. (2022). Title D. Journal W, 3, 60-70.
5. Brown, H. (2021). Title E. Journal V, 1, 80-90.
```

The audit report would show:

| Metric | Count |
|--------|-------|
| Inline citations (unique) | 4 |
| Bibliography entries | 5 |
| Matched | 3 |
| Cited but not listed | 1 (Lee 2024) |
| Listed but not cited | 2 (Adams 2022, Brown 2021) |
| Informal mentions | 1 (Tufte) |

**Status: FAIL** — 1 missing entry + 2 uncited entries + 1 informal mention.

## Notes for Report Generation

- Count each unique citation once, even if it appears multiple times in the text
- For numbered systems, verify that numbers are sequential and that the highest number does not exceed the bibliography length
- When listing "location," use section name and paragraph number (e.g., "Methods, para 3")
- For informal mentions, include enough surrounding context (5-10 words) to locate the passage
- If the manuscript uses a `.bib` file, audit both the `.bib` file and the rendered bibliography
