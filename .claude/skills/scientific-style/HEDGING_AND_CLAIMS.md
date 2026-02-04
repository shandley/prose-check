# Hedging and Claims

Detailed guidance on calibrating claim strength in scientific writing.

## The Claim Strength Spectrum

### Level 1: Certain (Unhedged)

**Language markers:**
- "X is..."
- "This demonstrates..."
- "The results prove..."
- No modal verbs or qualifiers

**Appropriate when:**
- Stating established scientific facts
- Reporting direct observations
- Mathematical or logical necessities
- Definitional statements

**Examples:**
```
Water freezes at 0°C at standard pressure.
The experiment included 50 participants.
DNA consists of four nucleotide bases.
```

### Level 2: Strong

**Language markers:**
- "This shows that..."
- "These results indicate..."
- "The evidence demonstrates..."
- "X leads to Y" (with causal evidence)

**Appropriate when:**
- Strong statistical evidence (p << 0.05)
- Large effect sizes
- Replicated findings
- Direct experimental manipulation with controls

**Examples:**
```
Treatment significantly reduced inflammation (p < 0.001, d = 1.2).
These results show that temperature affects reaction rate.
Knockout of gene X leads to developmental defects.
```

### Level 3: Moderate

**Language markers:**
- "X suggests that..."
- "This supports the hypothesis..."
- "The data are consistent with..."
- "X appears to..."

**Appropriate when:**
- Good statistical evidence
- Reasonable inference from data
- Alignment with existing theory
- Single study findings

**Examples:**
```
These findings suggest a role for X in Y.
The correlation supports the proposed mechanism.
Results are consistent with the competitive binding model.
```

### Level 4: Tentative

**Language markers:**
- "X may..."
- "This could indicate..."
- "It is possible that..."
- "X might play a role in..."

**Appropriate when:**
- Preliminary findings
- Small sample sizes
- Indirect evidence
- Extending beyond direct data

**Examples:**
```
This polymorphism may contribute to disease risk.
The observed pattern could reflect selection pressure.
It is possible that additional factors influence the relationship.
```

### Level 5: Speculative

**Language markers:**
- "One might speculate..."
- "It is tempting to hypothesize..."
- "Speculatively,..."
- "While data are limited..."

**Appropriate when:**
- Extrapolating well beyond data
- Generating future hypotheses
- Theoretical implications
- Very preliminary evidence

**Examples:**
```
One might speculate that this mechanism operates across taxa.
It is tempting to hypothesize a broader regulatory role.
While data are limited, X could potentially influence Y.
```

## Hedging Devices

### Modal Verbs

| Verb | Strength | Example |
|------|----------|---------|
| will | Certain | "This will affect..." |
| would | Moderate | "This would suggest..." |
| should | Moderate | "This should indicate..." |
| may | Tentative | "This may reflect..." |
| might | Tentative | "This might be due to..." |
| could | Tentative | "This could indicate..." |
| can | Possibility | "This can occur when..." |

### Adverbs of Frequency/Probability

| Adverb | Use | Note |
|--------|-----|------|
| always, never | Strong claims | Use cautiously |
| usually, typically | General pattern | Some variation expected |
| often, frequently | Common | Not universal |
| sometimes | Variable | Context-dependent |
| occasionally, rarely | Uncommon | Exception rather than rule |
| possibly, perhaps | Uncertain | Limited evidence |

### Qualifying Phrases

**Appropriate hedges:**
- "Under these conditions,..."
- "In this system,..."
- "To our knowledge,..."
- "Based on these data,..."
- "With the caveat that,..."

**Overused (avoid stacking):**
- "It may be possible that..." → "This may..."
- "It would seem to suggest..." → "This suggests..."
- "Perhaps it might be..." → "This could..."

## Section-Specific Hedging

### Introduction

**Cite established facts confidently:**
```
✓ "Climate change affects species distributions (IPCC 2023)."
✗ "Climate change may potentially affect species distributions."
```

**Hedge uncertain claims:**
```
✓ "Recent evidence suggests that X may also influence Y (Smith 2023)."
✓ "The mechanism remains unclear."
```

**State objectives directly:**
```
✓ "We tested whether X affects Y."
✗ "We attempted to investigate whether X might possibly affect Y."
```

### Methods

**Generally unhedged:**
```
✓ "We collected samples from 10 sites."
✓ "Statistical analysis was performed using R."
✗ "We attempted to collect samples..."
```

**Exception - methodological limitations:**
```
✓ "Due to sample availability, we were limited to..."
```

### Results

**Report findings directly:**
```
✓ "Expression increased 2.5-fold (p < 0.01)."
✗ "Expression appeared to possibly increase."
```

**Statistical hedging is built-in:**
```
✓ "There was no significant difference (p = 0.12)."
The statistics do the hedging; don't add more.
```

### Discussion

**Match hedging to evidence:**
```
Strong evidence:
✓ "Our results demonstrate that X affects Y."

Moderate evidence:
✓ "These findings suggest that X may affect Y."

Weak evidence:
✓ "One possibility is that X influences Y, though further work is needed."
```

**Interpretation vs. observation:**
```
Observation (less hedged): "We observed a 3-fold increase."
Interpretation (more hedged): "This increase may reflect..."
```

## Common Problems

### Hedge Stacking

**Problem:** Multiple hedges weakening the claim unnecessarily.

| Overhedged | Calibrated |
|------------|------------|
| "It may possibly suggest that perhaps..." | "This suggests that..." |
| "It would seem to potentially indicate..." | "This may indicate..." |
| "One could tentatively speculate..." | "One might speculate..." |

### Underhedging

**Problem:** Claims exceed evidence.

| Overconfident | Calibrated |
|---------------|------------|
| "This proves that X causes Y." | "These results suggest X is associated with Y." |
| "We discovered that..." | "We found that..." |
| "This confirms the mechanism." | "This is consistent with the proposed mechanism." |

### Inconsistent Hedging

**Problem:** Same finding hedged differently in different places.

**Solution:** Establish appropriate hedge level and use consistently.

### Misplaced Hedging

**Problem:** Hedging facts instead of interpretations.

```
✗ "We collected possibly 50 samples."
✓ "We collected 50 samples."

✗ "The mean may have been 3.5."
✓ "The mean was 3.5."
```

## Calibration Exercises

### Exercise 1: Match Claim to Evidence

**Evidence:** Correlation (r = 0.3, p = 0.04) in n = 50 sample

**Appropriate:**
- "X was associated with Y (r = 0.3, p = 0.04)."
- "We found a modest positive correlation between X and Y."
- "These results suggest a relationship between X and Y."

**Too strong:**
- "X causes Y."
- "This demonstrates that X determines Y."

**Too weak:**
- "X might possibly be somewhat related to Y."

### Exercise 2: Section-Appropriate Hedging

**Finding:** Knockout mice show 80% survival vs. 95% in controls (p < 0.001)

**Results section:**
"Knockout mice showed significantly reduced survival compared to controls (80% vs. 95%, p < 0.001)."

**Discussion section:**
"The reduced survival in knockout mice suggests that Gene X plays an important role in [function]. This finding indicates that..."

### Exercise 3: Hedge Reduction

**Original (overhedged):**
"It may be possible that these results could potentially suggest that X might perhaps play a role in Y."

**Calibrated:**
"These results suggest that X may play a role in Y."

## Quick Reference

### Strengthen Claims
- Remove unnecessary hedges
- Use stronger verbs (show → demonstrate)
- Remove qualifiers (may → [delete])
- Combine stacked hedges

### Weaken Claims
- Add appropriate modal (is → may be)
- Use tentative verbs (demonstrate → suggest)
- Add qualifiers (This → Under these conditions, this)
- Acknowledge limitations explicitly
