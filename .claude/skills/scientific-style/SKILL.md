---
name: scientific-style
description: Calibrate scientific claims and integrate citations properly. Use when adjusting claim strength, adding hedging language, integrating literature, or matching evidence to conclusions. Complements human-writing by addressing when hedging IS appropriate.
argument-hint: [text to review or claim to calibrate]
---

# Scientific Style Guide

This guide covers claim calibration, citation integration, and scientific hedging.

## When to Use This Skill

- Calibrating claim strength to match evidence
- Integrating citations smoothly
- Adding appropriate hedging (or removing excessive hedging)
- Matching tense to context
- Avoiding overclaiming or underclaiming

**Relationship to human-writing:** The `human-writing` skill flags excessive hedging as an AI pattern. Scientific writing is an exception where measured hedging IS appropriate. This skill explains when and how to hedge in scientific contexts.

## Hedging in Scientific Writing

### Why Hedge?

Scientific hedging serves legitimate purposes:
- Acknowledges uncertainty inherent in empirical findings
- Distinguishes between data and interpretation
- Protects against overgeneralization
- Signals epistemic humility
- Follows disciplinary conventions

### The Calibration Problem

| Too little hedging | Appropriate hedging | Too much hedging |
|-------------------|---------------------|------------------|
| "X causes Y" (when correlational) | "X is associated with Y" | "X may possibly be related to Y in some cases" |
| "This proves..." | "These results suggest..." | "These results might perhaps indicate..." |
| Overclaims evidence | Matches claim to evidence | Undermines your own work |

### Claim Strength Ladder

From strongest to weakest:

| Level | Language | Use When |
|-------|----------|----------|
| **Certain** | "X is...", "This demonstrates..." | Established facts, direct observations |
| **Strong** | "X indicates...", "These results show..." | Strong statistical evidence, replicated findings |
| **Moderate** | "X suggests...", "This supports..." | Good evidence, reasonable inference |
| **Tentative** | "X may...", "This could indicate..." | Preliminary findings, indirect evidence |
| **Speculative** | "It is possible that...", "One might speculate..." | Limited evidence, theoretical extension |

See [HEDGING_AND_CLAIMS.md](HEDGING_AND_CLAIMS.md) for detailed guidance.

## Citation Integration

### Two Basic Patterns

**Integral citation** (author as subject):
- "Smith (2023) demonstrated that..."
- "According to Johnson et al. (2024),..."

**Non-integral citation** (information emphasized):
- "Gene expression varies with temperature (Smith 2023)."
- "Previous work supports this model (Johnson et al. 2024; Lee 2023)."

### When to Use Each

| Use Integral When | Use Non-Integral When |
|-------------------|----------------------|
| Author's contribution is noteworthy | Information is the focus |
| Discussing specific methodology | Supporting general claim |
| Comparing different authors' views | Citing multiple sources |
| Attributing a controversial claim | Stating widely accepted facts |

### Reporting Verbs

| Verb | Connotation | Example |
|------|-------------|---------|
| found | Neutral, empirical | "Smith (2023) found that X..." |
| showed | Strong evidence | "Johnson (2024) showed that Y..." |
| demonstrated | Strong, definitive | "Lee et al. demonstrated the effect..." |
| suggested | Tentative | "Prior work suggested a relationship..." |
| argued | Position/claim | "Wang (2023) argued that..." |
| reported | Neutral, descriptive | "Three studies reported increases..." |
| observed | Empirical, direct | "We observed a significant effect..." |
| noted | Passing mention | "As noted by Smith (2022),..." |
| claimed | Slight skepticism | "Authors claimed efficacy..." |
| proposed | Theoretical | "Chen (2024) proposed a model..." |

See [CITATION_PATTERNS.md](CITATION_PATTERNS.md) for more patterns.

## Tense Usage

### By Section

| Section | Primary Tense | Rationale |
|---------|---------------|-----------|
| Introduction | Present | General truths, current state of knowledge |
| Methods | Past | Describes completed actions |
| Results | Past | Reports what was found |
| Discussion | Present + Past | Interprets (present), refers to results (past) |

### By Content Type

| Content | Tense | Example |
|---------|-------|---------|
| General fact | Present | "Temperature affects enzyme activity." |
| Previous finding | Past | "Smith (2023) found that..." |
| Your methods | Past | "We collected samples from..." |
| Your results | Past | "Gene expression increased..." |
| Your interpretation | Present | "These findings suggest that..." |
| Future work | Future/Conditional | "Future studies should..." |

## Common Calibration Issues

### Overclaiming

**Problem:** Claims exceed what evidence supports.

| Overclaim | Calibrated |
|-----------|------------|
| "This proves X causes Y" | "These results suggest X is associated with Y" |
| "We discovered that..." | "We found that..." |
| "This novel finding..." | "We observed that..." (let novelty speak for itself) |
| "Clearly, X leads to Y" | "X appears to lead to Y" |

### Underclaiming

**Problem:** Excessive hedging weakens legitimate findings.

| Underclaim | Calibrated |
|------------|------------|
| "It may be possible that..." | "This suggests..." |
| "Perhaps X might..." | "X may..." |
| "We tentatively propose..." | "We propose..." |
| Stacking hedges: "might possibly suggest" | Choose one: "suggests" |

### Correlation vs. Causation

| Causal (use only with experimental evidence) | Associational (use with observational data) |
|---------------------------------------------|---------------------------------------------|
| causes, leads to, results in | is associated with, correlates with |
| produces, induces, triggers | is related to, is linked to |
| affects, influences | co-occurs with, predicts |

## Section-Specific Guidelines

### Introduction
- Present established facts confidently
- Use hedging when citing preliminary or contested findings
- State your objectives directly ("We tested..." not "We attempted to test...")

### Methods
- Be direct; minimal hedging needed
- State what you did, not what you tried to do

### Results
- Report findings directly
- Save interpretation (and hedging) for Discussion
- "Expression increased" not "Expression appeared to increase"

### Discussion
- Match hedging to evidence strength
- Distinguish your findings (past tense) from interpretation (present tense)
- Acknowledge limitations without undermining your conclusions

## Quality Checks

Before finalizing:

- [ ] Claims match evidence strength
- [ ] Causal language used only with causal evidence
- [ ] No hedge stacking ("might possibly suggest")
- [ ] Citations support the claims they follow
- [ ] Tense is consistent within sections
- [ ] Interpretation clearly distinguished from results
- [ ] Limitations acknowledged proportionally

## Related Files

- [CITATION_PATTERNS.md](CITATION_PATTERNS.md) - Citation integration patterns
- [HEDGING_AND_CLAIMS.md](HEDGING_AND_CLAIMS.md) - Detailed hedging guidance
