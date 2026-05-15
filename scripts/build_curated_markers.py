#!/usr/bin/env python3
"""
Build curated markers database for prose-check.

Replaces corpus-analysis-generated markers.json with a hand-curated set of
patterns known to be over-represented in AI-generated writing, drawn from:
  - Statistical analysis in results/model_comparison.md (em dash, word ratios)
  - Recent corpus linguistics research (2024-2025)
  - The prose-check skill set (human-writing, scientific-style)

The original corpus approach produced ~2,950 markers dominated by technical
vocabulary and markdown artifacts (domain drift, not style drift). This
produces ~130 high-signal markers specific to prose quality.

Usage:
    uv run python scripts/build_curated_markers.py
"""

import json
import math
from datetime import date
from pathlib import Path


BASE = Path(__file__).parent.parent


def m(item: str, type_: str, ratio: float, opus_rate: float, example: str = "") -> dict:
    """
    Build one marker entry.

    ratio      AI rate / human rate (empirical or literature-derived)
    opus_rate  estimated rate in AI text (fraction of total words or chars)
    """
    human_rate = opus_rate / ratio
    log_odds = math.log(ratio)
    se = 0.25  # typical SE for these effect sizes
    return {
        "type": type_,
        "item": item,
        "opus_rate": round(opus_rate, 7),
        "human_rate": round(human_rate, 7),
        "log_odds": round(log_odds, 2),
        "ci_lower": round(log_odds - 1.96 * se, 2),
        "ci_upper": round(log_odds + 1.96 * se, 2),
        # Scale to approximate corpus sizes (47k AI words, 1.2M human words)
        "opus_count": max(5, int(opus_rate * 47_000)),
        "human_count": max(1, int(human_rate * 1_208_000)),
        "example_context": example,
    }


# ---------------------------------------------------------------------------
# LLM-FAVORITE WORDS
# Ratios from: model_comparison.md, human-writing/SKILL.md, and corpus lit.
# High severity: ratio >= ~12x (log_odds >= 2.5)
# Medium severity: ratio 5-12x (log_odds 1.6-2.5)
# ---------------------------------------------------------------------------

LLM_WORDS = [
    # Very high ratio (25x+) — always flag
    m("delve",          "phrase_llm_favorite", 50,  0.00100, "let's delve into the intricacies"),
    m("tapestry",       "phrase_llm_favorite", 50,  0.00050, "the tapestry of modern computing"),
    m("multifaceted",   "phrase_llm_favorite", 40,  0.00080, "this multifaceted problem"),
    m("embark",         "phrase_llm_favorite", 40,  0.00080, "embark on a journey to"),
    m("plethora",       "phrase_llm_favorite", 35,  0.00070, "a plethora of options"),
    m("myriad",         "phrase_llm_favorite", 30,  0.00060, "myriad possibilities emerge"),
    m("aforementioned", "phrase_llm_favorite", 30,  0.00080, "the aforementioned methodology"),
    m("seamlessly",     "phrase_llm_favorite", 30,  0.00090, "seamlessly integrates with"),
    m("meticulous",     "phrase_llm_favorite", 30,  0.00070, "meticulous attention to detail"),
    m("noteworthy",     "phrase_llm_favorite", 30,  0.00050, "a noteworthy aspect of"),
    m("utilize",        "phrase_llm_favorite", 30,  0.00150, "utilize the available resources"),
    m("comprehensive",  "phrase_llm_favorite", 24,  0.00240, "a comprehensive guide to"),  # 24.4x (SKILL.md)
    m("leverage",       "phrase_llm_favorite", 25,  0.00120, "leverage existing paradigms"),
    m("intricate",      "phrase_llm_favorite", 25,  0.00080, "the intricate details of"),
    m("paramount",      "phrase_llm_favorite", 25,  0.00050, "of paramount importance"),
    m("groundbreaking", "phrase_llm_favorite", 25,  0.00060, "groundbreaking research that"),
    m("synergy",        "phrase_llm_favorite", 22,  0.00040, "create synergy between"),
    m("holistic",       "phrase_llm_favorite", 22,  0.00050, "a holistic approach to"),
    m("impactful",      "phrase_llm_favorite", 20,  0.00060, "an impactful approach"),
    m("pivotal",        "phrase_llm_favorite", 20,  0.00080, "a pivotal role in"),
    m("endeavor",       "phrase_llm_favorite", 20,  0.00060, "this endeavor requires"),
    m("facilitate",     "phrase_llm_favorite", 20,  0.00090, "facilitate seamless integration"),
    m("realm",          "phrase_llm_favorite", 20,  0.00080, "in the realm of"),
    m("transformative", "phrase_llm_favorite", 20,  0.00060, "a transformative shift"),
    m("streamline",     "phrase_llm_favorite", 20,  0.00070, "streamline the process"),
    m("fostering",      "phrase_llm_favorite", 20,  0.00050, "fostering innovation and"),
    m("proactive",      "phrase_llm_favorite", 18,  0.00060, "a proactive approach"),
    m("nuanced",        "phrase_llm_favorite", 17,  0.00170, "a nuanced approach to"),  # 17x (SKILL.md)
    m("underscore",     "phrase_llm_favorite", 15,  0.00070, "these findings underscore"),
    m("landscape",      "phrase_llm_favorite", 15,  0.00090, "the landscape of modern"),
    m("paradigm",       "phrase_llm_favorite", 15,  0.00150, "a paradigm shift in"),  # 15.1x (SKILL.md)
    m("foster",         "phrase_llm_favorite", 15,  0.00070, "foster a culture of"),
    m("navigate",       "phrase_llm_favorite", 12,  0.00080, "navigate the complexities"),
    # Medium-high ratio (8-12x) — strong signal
    m("robust",         "phrase_llm_favorite",  8,  0.00120, "a robust framework for"),   # 3-43x by model
    m("crucial",        "phrase_llm_favorite", 10,  0.00150, "crucial to understanding"),
    m("vital",          "phrase_llm_favorite", 10,  0.00080, "vital that we consider"),
    m("innovative",     "phrase_llm_favorite", 10,  0.00090, "an innovative solution"),
    m("paramount",      "phrase_llm_favorite", 10,  0.00050, "of paramount importance"),  # dup? skip one
]

# Deduplicate (keep first occurrence)
seen = set()
LLM_WORDS_DEDUPED = []
for entry in LLM_WORDS:
    if entry["item"] not in seen:
        seen.add(entry["item"])
        LLM_WORDS_DEDUPED.append(entry)
LLM_WORDS = LLM_WORDS_DEDUPED


# ---------------------------------------------------------------------------
# HEDGING PHRASES — empty throat-clearing, almost always deletable
# ---------------------------------------------------------------------------

HEDGING = [
    m("it's important to note",   "phrase_hedging", 40, 0.00080, "It's important to note that this"),
    m("it is important to note",  "phrase_hedging", 40, 0.00080, "It is important to note that"),
    m("it's worth noting",        "phrase_hedging", 40, 0.00070, "It's worth noting that the"),
    m("it is worth noting",       "phrase_hedging", 40, 0.00070, "It is worth noting that"),
    m("it should be noted",       "phrase_hedging", 35, 0.00070, "It should be noted that"),
    m("it is worth mentioning",   "phrase_hedging", 30, 0.00040, "It is worth mentioning that"),
    m("needless to say",          "phrase_hedging", 25, 0.00030, "Needless to say, the results"),
    m("it goes without saying",   "phrase_hedging", 20, 0.00030, "it goes without saying that"),
    m("that being said",          "phrase_hedging", 15, 0.00090, "That being said, the approach"),
    m("having said that",         "phrase_hedging", 12, 0.00060, "Having said that, we should"),
    m("with that in mind",        "phrase_hedging", 12, 0.00050, "With that in mind,"),
    m("generally speaking",       "phrase_hedging", 10, 0.00080, "Generally speaking, the method"),
    m("in many cases",            "phrase_hedging",  8, 0.00100, "In many cases, the approach"),
]


# ---------------------------------------------------------------------------
# FILLER PHRASES — add length without meaning
# ---------------------------------------------------------------------------

FILLERS = [
    m("in order to",                  "phrase_filler", 15, 0.00300, "in order to achieve optimal"),
    m("due to the fact that",         "phrase_filler", 25, 0.00080, "due to the fact that"),
    m("at the end of the day",        "phrase_filler", 20, 0.00070, "At the end of the day,"),
    m("in today's world",             "phrase_filler", 30, 0.00060, "In today's world,"),
    m("in the realm of",              "phrase_filler", 20, 0.00070, "in the realm of software"),
    m("when it comes to",             "phrase_filler", 15, 0.00120, "When it comes to"),
    m("serves as a",                  "phrase_filler", 15, 0.00120, "serves as a testament to"),
    m("plays a crucial role",         "phrase_filler", 20, 0.00080, "plays a crucial role in"),
    m("plays a key role",             "phrase_filler", 15, 0.00100, "plays a key role in"),
    m("in terms of",                  "phrase_filler",  8, 0.00200, "in terms of the overall"),
    m("with respect to",              "phrase_filler",  8, 0.00150, "with respect to the data"),
    m("at this point in time",        "phrase_filler", 20, 0.00040, "at this point in time"),
    m("for all intents and purposes", "phrase_filler", 25, 0.00030, "for all intents and purposes"),
    m("the fact that",                "phrase_filler",  8, 0.00200, "the fact that this approach"),
]


# ---------------------------------------------------------------------------
# STRUCTURE PHRASES — meta-commentary about the text itself
# ---------------------------------------------------------------------------

STRUCTURE = [
    m("let's dive into",      "phrase_structure", 50, 0.00080, "Let's dive into the details"),
    m("let's explore",        "phrase_structure", 40, 0.00100, "Let's explore the various aspects"),
    m("let's delve into",     "phrase_structure", 50, 0.00070, "Let's delve into this topic"),
    m("let me explain",       "phrase_structure", 30, 0.00060, "Let me explain how this works"),
    m("let's break this down","phrase_structure", 30, 0.00050, "Let's break this down step by step"),
    m("here's the thing",     "phrase_structure", 25, 0.00060, "Here's the thing:"),
    m("first and foremost",   "phrase_structure", 20, 0.00080, "First and foremost, we need"),
    m("last but not least",   "phrase_structure", 20, 0.00060, "Last but not least,"),
    m("let's look at",        "phrase_structure", 15, 0.00100, "Let's look at how"),
]


# ---------------------------------------------------------------------------
# CONCLUSION / SUMMARY PHRASES
# ---------------------------------------------------------------------------

CONCLUSIONS = [
    m("in essence",      "phrase_conclusion", 20, 0.00150, "In essence, the approach"),
    m("fundamentally",   "phrase_conclusion", 12, 0.00120, "Fundamentally, this represents"),
    m("essentially",     "phrase_conclusion", 10, 0.00180, "Essentially, the core idea"),
    m("at its core",     "phrase_conclusion", 20, 0.00070, "At its core, this is"),
    m("in summary",      "phrase_conclusion",  8, 0.00150, "In summary, the results show"),
    m("in conclusion",   "phrase_conclusion",  8, 0.00120, "In conclusion, we have shown"),
    m("to summarize",    "phrase_conclusion", 10, 0.00100, "To summarize, the key points"),
    m("all in all",      "phrase_conclusion", 12, 0.00080, "All in all, the approach"),
    m("overall",         "phrase_conclusion",  5, 0.00300, "Overall, the results suggest"),
    m("ultimately",      "phrase_conclusion",  8, 0.00200, "Ultimately, the decision"),
]


# ---------------------------------------------------------------------------
# EMPHASIS WORDS — usually deletable; AI uses these to signal importance
# rather than demonstrating importance through content
# ---------------------------------------------------------------------------

EMPHASIS = [
    m("absolutely",     "phrase_emphasis", 15, 0.00120, "This is absolutely essential"),
    m("undoubtedly",    "phrase_emphasis", 15, 0.00080, "This is undoubtedly the best"),
    m("without a doubt","phrase_emphasis", 15, 0.00060, "without a doubt the most"),
    m("certainly",      "phrase_emphasis", 10, 0.00150, "This certainly represents"),
    m("definitely",     "phrase_emphasis", 10, 0.00130, "This will definitely improve"),
    m("obviously",      "phrase_emphasis",  8, 0.00120, "Obviously, this approach"),
    m("clearly",        "phrase_emphasis",  6, 0.00200, "Clearly, the results demonstrate"),
    m("of course",      "phrase_emphasis",  6, 0.00200, "Of course, this depends"),
    m("naturally",      "phrase_emphasis",  8, 0.00120, "Naturally, this leads to"),
    m("indeed",         "phrase_emphasis",  8, 0.00150, "This is indeed a complex"),
]


# ---------------------------------------------------------------------------
# TRANSITION WORDS — AI uses formal transitions; humans use casual ones.
# Only flag the most heavily overused. (Note: "however" is more common in
# human writing than AI — don't flag it.)
# ---------------------------------------------------------------------------

TRANSITIONS = [
    m("furthermore",   "phrase_transition",  8, 0.00200, "Furthermore, the results"),
    m("moreover",      "phrase_transition",  8, 0.00180, "Moreover, this approach"),
    m("additionally",  "phrase_transition",  8, 0.00200, "Additionally, we should consider"),
    m("conversely",    "phrase_transition", 50, 0.00100, "Conversely, the other approach"),  # 50x (SKILL.md)
    m("nevertheless",  "phrase_transition",  8, 0.00100, "Nevertheless, the results"),     # 8x (SKILL.md)
    m("nonetheless",   "phrase_transition",  8, 0.00080, "Nonetheless, the approach"),
    m("consequently",  "phrase_transition",  8, 0.00100, "Consequently, the team"),
    m("accordingly",   "phrase_transition", 10, 0.00080, "Accordingly, we recommend"),
    m("subsequently",  "phrase_transition",  8, 0.00100, "Subsequently, the results"),
    m("in addition",   "phrase_transition",  6, 0.00200, "In addition, we found"),
]


# ---------------------------------------------------------------------------
# SENTENCE STARTERS — AI overuses these to begin sentences.
# Ratios are documented in human-writing/SKILL.md.
# Type "sentence_starter" triggers a different regex (start-of-sentence match).
# ---------------------------------------------------------------------------

STARTERS = [
    m("Comprehensive",  "sentence_starter", 680, 0.00100, "Comprehensive guide to..."),
    m("This document",  "sentence_starter", 623, 0.00150, "This document provides..."),
    m("This guide",     "sentence_starter", 400, 0.00120, "This guide covers..."),
    m("This article",   "sentence_starter", 350, 0.00100, "This article explores..."),
    m("This section",   "sentence_starter", 200, 0.00200, "This section describes..."),
    m("Introduction",   "sentence_starter",  58, 0.00200, "Introduction to the topic..."),
    m("Let's",          "sentence_starter",  50, 0.00300, "Let's explore..."),
    m("In this",        "sentence_starter",  30, 0.00400, "In this document..."),
    # Scientific writing specific — high-frequency formulaic openers
    m("Importantly",    "sentence_starter",  20, 0.00200, "Importantly, our results show"),
    m("Notably",        "sentence_starter",  20, 0.00150, "Notably, we observed"),
    m("Interestingly",  "sentence_starter",  15, 0.00200, "Interestingly, the data suggest"),
    m("Fundamentally",  "sentence_starter",  15, 0.00100, "Fundamentally, this approach"),
    m("Essentially",    "sentence_starter",  12, 0.00150, "Essentially, the model"),
    m("Ultimately",     "sentence_starter",  10, 0.00200, "Ultimately, the results"),
    m("It's worth",     "sentence_starter",  30, 0.00200, "It's worth noting that"),
    m("It is worth",    "sentence_starter",  30, 0.00200, "It is worth noting that"),
]


def build_markers() -> list[dict]:
    all_markers = (
        LLM_WORDS
        + HEDGING
        + FILLERS
        + STRUCTURE
        + CONCLUSIONS
        + EMPHASIS
        + TRANSITIONS
        + STARTERS
    )
    # Sort by log_odds descending so the most distinctive appear first
    all_markers.sort(key=lambda x: -x["log_odds"])
    return all_markers


def load_existing_summary_stats() -> dict:
    """Preserve the valid structural stats from the original corpus analysis."""
    markers_path = BASE / "results" / "markers.json"
    if not markers_path.exists():
        return {}
    with open(markers_path) as f:
        data = json.load(f)
    return data.get("summary_stats", {})


def main() -> None:
    markers = build_markers()

    # Load original summary_stats (structural data is valid; lexical markers were the problem)
    summary_stats = load_existing_summary_stats()

    output = {
        "corpus_stats": {
            "opus_samples": 201,
            "human_samples": 6000,
            "opus_total_words": 47104,
            "human_total_words": 1208418,
            "note": (
                "Curated marker database v1.1. Ratios are empirically grounded "
                "(model_comparison.md, human-writing/SKILL.md, corpus linguistics "
                "literature 2024-2025). Replaces corpus-analysis markers that "
                "captured domain drift rather than writing style."
            ),
            "version": "1.1.0",
            "last_updated": str(date.today()),
        },
        "summary_stats": summary_stats,
        "markers": markers,
    }

    out_path = BASE / "results" / "markers.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    # Report
    by_type: dict[str, int] = {}
    by_severity = {"high": 0, "medium": 0, "low": 0}
    for mk in markers:
        by_type[mk["type"]] = by_type.get(mk["type"], 0) + 1
        lo = mk["log_odds"]
        if lo >= 2.5:
            by_severity["high"] += 1
        elif lo >= 1.5:
            by_severity["medium"] += 1
        else:
            by_severity["low"] += 1

    print(f"Written {len(markers)} curated markers to {out_path}")
    print()
    print("By type:")
    for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t:30} {c}")
    print()
    print("By severity:")
    for s, c in by_severity.items():
        print(f"  {s:10} {c}")
    print()
    print("Top 10 by log_odds:")
    for mk in markers[:10]:
        print(f"  {mk['item']:30} log_odds={mk['log_odds']:.2f}  ({mk['opus_rate']/mk['human_rate']:.0f}x)")


if __name__ == "__main__":
    main()
