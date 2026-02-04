# Change Tracking

Guidelines for managing manuscript versions and tracking changes during revision.

## File Naming Conventions

### Basic Pattern
```
[ShortTitle]_[Version]_[Type].[ext]

Examples:
ClimateAdaptation_R1_tracked.docx
ClimateAdaptation_R1_clean.docx
ClimateAdaptation_R1_response.docx
ClimateAdaptation_R2_tracked.docx
```

### Version Labels
| Label | Meaning |
|-------|---------|
| v1, v2, v3 | Internal drafts (pre-submission) |
| submitted | Initial submission |
| R1 | First revision |
| R2 | Second revision |
| R3 | Third revision (rare) |
| accepted | Final accepted version |
| proofs | Page proofs |

### File Types
| Suffix | Content |
|--------|---------|
| _tracked | Manuscript with track changes visible |
| _clean | Manuscript with all changes accepted |
| _response | Response to reviewers letter |
| _cover | Cover letter |
| _diff | Comparison document |
| _supp | Supplementary materials |

## Directory Structure

```
project/
├── manuscript/
│   ├── submitted/
│   │   ├── Manuscript_submitted.docx
│   │   └── Figures_submitted/
│   ├── R1/
│   │   ├── Manuscript_R1_tracked.docx
│   │   ├── Manuscript_R1_clean.docx
│   │   ├── Response_R1.docx
│   │   ├── Reviews_R1.pdf
│   │   └── Figures_R1/
│   └── R2/
│       ├── Manuscript_R2_tracked.docx
│       └── ...
└── analysis/
    └── [analysis files]
```

## Track Changes Best Practices

### What to Track
- Text additions and deletions
- Moved text (if software supports)
- Formatting changes that affect meaning
- Figure/table modifications (note in caption)

### What Not to Track
- Minor formatting fixes (spacing, fonts)
- Reference reformatting
- Line number changes
- Pagination changes

### Track Changes Settings (Word)
- Use "Simple Markup" view while editing for readability
- Switch to "All Markup" before saving tracked version
- Set to show insertions and deletions
- Consider hiding formatting changes (clutters document)

### Color Coding (if multiple authors)
- Assign distinct colors to each author
- Note color assignments in response letter if helpful

## Creating Tracked and Clean Versions

### Workflow
1. Start from clean submitted version
2. Turn on track changes
3. Make all revisions
4. Save as `_tracked` version
5. Accept all changes
6. Save as `_clean` version
7. Verify both versions are consistent

### Verification Checklist
- [ ] Tracked version shows all changes
- [ ] Clean version has no visible markup
- [ ] Both versions have same final text
- [ ] Page/line numbers in response letter match clean version
- [ ] Figures/tables are consistent across versions

## Cross-Referencing Changes

### In Response Letter
Reference format:
```
Changes made: Page X, lines Y-Z.
Changes made: Page 12, lines 234-238.
Changes made: Methods section, paragraph 3.
Changes made: Figure 2 and its caption.
Changes made: Table 1, column 3.
Changes made: Supplementary Figure S2.
```

### For Multiple Locations
```
Changes made:
- Page 3, lines 45-52 (Methods)
- Page 7, lines 156-160 (Results)
- Page 12, lines 289-295 (Discussion)
```

### For Large-Scale Changes
```
Changes made: Throughout the manuscript. Key locations include
pages 3-4 (Methods), pages 7-9 (Results), and page 12 (Discussion).
See tracked changes document for complete details.
```

## Version Control for Collaborative Revision

### Simple Approach (Small Team)
1. One person holds the "master" document
2. Others send comments/edits via email or comments
3. Master-holder incorporates changes
4. Periodic snapshots saved with date suffixes

### Cloud-Based Approach
- Use Google Docs or OneDrive for real-time collaboration
- Export to Word for final tracked changes version
- Maintain version history through platform

### Git-Based Approach (Advanced)
- Write in Markdown or LaTeX
- Use git for version control
- Generate diff for reviewer-friendly comparison
- Export to required format for submission

## Handling Multiple Revision Rounds

### R1 to R2 Tracking
Two approaches:

**Option A: Cumulative tracking (from original)**
- Continue tracking from submitted version
- All changes from submission visible
- Pro: Shows complete revision history
- Con: Can be overwhelming if many changes

**Option B: Fresh tracking (from R1)**
- Start fresh from accepted R1 version
- Only R2 changes visible
- Pro: Cleaner, focused on new changes
- Con: Loses revision history

**Recommendation:** Use Option B unless journal requires otherwise. Note in cover letter: "Track changes show modifications since Revision 1."

### Maintaining Revision History
Keep all previous versions:
```
R1/
├── Manuscript_R1_tracked.docx    (changes from submitted)
├── Manuscript_R1_clean.docx
└── Response_R1.docx

R2/
├── Manuscript_R2_tracked.docx    (changes from R1)
├── Manuscript_R2_clean.docx
└── Response_R2.docx
```

## LaTeX-Specific Guidance

### Using latexdiff
```bash
latexdiff old.tex new.tex > diff.tex
pdflatex diff.tex
```

### Manual Markup
```latex
\usepackage{changes}
\added{new text}
\deleted{old text}
\replaced{new text}{old text}
```

### Track Changes Package
```latex
\usepackage[markup=underlined]{changes}
\definechangesauthor[color=blue]{reviewer1}
\added[id=reviewer1]{Added text in response to R1}
```

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| Track changes makes doc unreadable | Use "Simple Markup" view; consider summary instead |
| Changes span entire paragraphs | Describe change in response letter; mark start/end |
| Reviewer wants to see old version | Provide both; explain in cover letter |
| Different software shows changes differently | Export to PDF with markup visible |
| Lost track of what changed | Recreate from version history; diff tools |
