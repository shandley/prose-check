# Reference Style Guide

Formatting rules for three common academic reference styles.

## Identifying Your Target Style

Check these in order:
1. **Journal instructions** — "References should follow APA 7th edition format"
2. **Sample references** in recent articles from the target journal
3. **Inline citations** — the inline format constrains the bibliography format:

| Inline Format | Likely Style |
|---------------|-------------|
| `(Smith, 2024)` with `&` | APA |
| `(Smith 2024)` with `and` | Harvard / Chicago |
| `[1]` numbered | Vancouver |

## Quick Comparison

| Feature | APA 7th | Vancouver | Chicago Author-Date |
|---------|---------|-----------|-------------------|
| Inline format | (Smith, 2024) | [1] | (Smith 2024) |
| List order | Alphabetical | Order of appearance | Alphabetical |
| Author limit | List up to 20 | List up to 6, then et al. | List up to 10 |
| Year placement | After authors, in parens | At end, after journal | After authors, in parens |
| Title case | Sentence case (articles) | Sentence case | Title case (books), sentence (articles) |
| Journal name | Italicized | Abbreviated, not italic | Italicized |
| DOI | As URL: https://doi.org/... | Optional | As URL: https://doi.org/... |
| "et al." inline | 3+ authors | 3+ authors | 4+ authors |

## APA 7th Edition

### Journal Article

**Template:**
```
Surname, I. N., Surname, I. N., & Surname, I. N. (YYYY). Article title in sentence case. Journal Name in Title Case and Italics, Volume(Issue), Pages. https://doi.org/xxxxx
```

**Example:**
```
Wickham, H. (2014). Tidy data. Journal of Statistical Software, 59(10), 1-23. https://doi.org/10.18637/jss.v059.i10
```

**Multiple authors (2-20):**
```
Smith, J. A., Jones, K. B., & Lee, C. D. (2024). Title here. Journal Name, 12(3), 45-50.
```

**21+ authors:**
```
Smith, J. A., Jones, K. B., Lee, C. D., Wang, F., Adams, G., Brown, H., Clark, I., Davis, J., Evans, K., Fisher, L., Garcia, M., Harris, N., Jackson, O., King, P., Lewis, Q., Martin, R., Nelson, S., Owen, T., Parker, U., ... Zimmerman, Z. (2024). Title here. Journal Name, 12(3), 45-50.
```

### Book

**Template:**
```
Surname, I. N. (YYYY). Book title in sentence case and italics. Publisher.
```

**Example:**
```
Tufte, E. R. (2001). The visual display of quantitative information (2nd ed.). Graphics Press.
```

### Book Chapter

**Template:**
```
Surname, I. N. (YYYY). Chapter title in sentence case. In I. N. Editor (Ed.), Book title in italics (pp. XX-XX). Publisher.
```

### Website / Software

**Template:**
```
Surname, I. N. (YYYY). Title of work. Site Name. https://url
```

**R package example:**
```
Wickham, H. (2016). ggplot2: Elegant graphics for data analysis. Springer-Verlag. https://ggplot2.tidyverse.org
```

### Common APA Mistakes

| Mistake | Correct |
|---------|---------|
| Title Case for Article Titles | Sentence case for article titles |
| Missing period after DOI | No period after DOI URL |
| `Smith, J., Jones, K. and Lee, C.` | `Smith, J., Jones, K., & Lee, C.` (use `&`) |
| `(Smith, et al., 2024)` | `(Smith et al., 2024)` (no comma after Smith) |
| Missing italics on journal name | *Journal Name* in italics |
| `Vol. 12, No. 3, pp. 45-50` | `12(3), 45-50` (compact form) |
| Year at end | Year after authors: `Smith, J. (2024).` |

## Vancouver / NLM

### Journal Article

**Template:**
```
Surname IN, Surname IN. Article title. Abbreviated Journal Name. YYYY;Volume(Issue):Pages.
```

**Example:**
```
Wickham H. Tidy data. J Stat Softw. 2014;59(10):1-23.
```

**Up to 6 authors — list all:**
```
Smith JA, Jones KB, Lee CD. Title here. J Name. 2024;12(3):45-50.
```

**7+ authors — first 6 then et al.:**
```
Smith JA, Jones KB, Lee CD, Wang F, Adams G, Brown H, et al. Title here. J Name. 2024;12(3):45-50.
```

### Book

**Template:**
```
Surname IN. Book Title. Edition. Place: Publisher; YYYY.
```

**Example:**
```
Tufte ER. The Visual Display of Quantitative Information. 2nd ed. Cheshire: Graphics Press; 2001.
```

### Website

**Template:**
```
Author/Organization. Title [Internet]. Place: Publisher; YYYY [cited YYYY Mon DD]. Available from: URL
```

### Common Vancouver Mistakes

| Mistake | Correct |
|---------|---------|
| Full journal name | Abbreviated journal name (J Stat Softw) |
| `Smith, J.A.` (with periods/commas) | `Smith JA` (no punctuation in initials) |
| Alphabetical reference list | Numbered in order of first appearance |
| `and` between authors | No conjunction, just commas |
| Italicized journal name | Not italicized |
| Missing semicolon before year | `J Name. 2024;12:45.` |

## Chicago Author-Date (17th Edition)

### Journal Article

**Template:**
```
Surname, First Name, and First Name Surname. YYYY. "Article Title in Title Case." Journal Name Volume (Issue): Pages. https://doi.org/xxxxx.
```

**Example:**
```
Wickham, Hadley. 2014. "Tidy Data." Journal of Statistical Software 59 (10): 1-23. https://doi.org/10.18637/jss.v059.i10.
```

**2-3 authors:**
```
Smith, John A., and Karen B. Jones. 2024. "Title Here." Journal Name 12 (3): 45-50.
```

**4+ authors:**
```
Smith, John A., Karen B. Jones, Chris D. Lee, and Fei Wang. 2024. "Title Here." Journal Name 12 (3): 45-50.
```

**11+ authors:**
```
Smith, John A., Karen B. Jones, Chris D. Lee, Fei Wang, Grace Adams, Henry Brown, Iris Clark, et al. 2024. "Title Here." Journal Name 12 (3): 45-50.
```

### Book

**Template:**
```
Surname, First Name. YYYY. Book Title in Italics. Place: Publisher.
```

**Example:**
```
Tufte, Edward R. 2001. The Visual Display of Quantitative Information. 2nd ed. Cheshire, CT: Graphics Press.
```

### Common Chicago Mistakes

| Mistake | Correct |
|---------|---------|
| `Smith, J.` (initials only) | `Smith, John` (full first name) |
| Year at end | Year after authors: `Smith, John. 2024.` |
| Article title not in quotes | "Article Title in Quotes" |
| Missing period after DOI | Period after DOI URL in Chicago |
| `Smith, John, Jones, Karen` | `Smith, John, and Karen Jones` (first author inverted only) |
| `&` between authors | `and` between authors |

## Validating a Reference List

### Checklist by Style

**For any style:**
- [ ] All entries use the same style consistently
- [ ] Author names formatted uniformly
- [ ] Year/date present in every entry
- [ ] Journal names consistently abbreviated (Vancouver) or spelled out (APA/Chicago)
- [ ] Punctuation pattern is consistent across entries
- [ ] DOIs included where available
- [ ] No duplicate entries

**APA-specific:**
- [ ] Sentence case for article titles
- [ ] Italic journal names and volume numbers
- [ ] `&` before last author (not `and`)
- [ ] Hanging indent format
- [ ] Entries alphabetized by first author surname

**Vancouver-specific:**
- [ ] Entries numbered sequentially
- [ ] Numbers match order of first appearance in text
- [ ] No punctuation in author initials
- [ ] Abbreviated journal names (NLM catalog)
- [ ] Semicolon between journal abbreviation period and year

**Chicago-specific:**
- [ ] Full first names (not initials)
- [ ] Article titles in quotation marks
- [ ] `and` before last author (not `&`)
- [ ] Only first author name inverted
- [ ] Entries alphabetized by first author surname
