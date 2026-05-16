"""Text structure checker -- paragraph length, bullet overuse, sentence distribution."""

from __future__ import annotations

from .._models import DocumentContext, Finding, Severity
from .._text import count_list_items, split_paragraphs, word_count
from . import Checker

# AI avg: 16 words/para. Human avg: ~200 words/para.
MIN_HEALTHY_PARA_WORDS = 40       # non-technical prose threshold
MIN_HEALTHY_PARA_WORDS_TECH = 20  # lower threshold for technical/methods text
MAX_LIST_ITEMS_PER_100_WORDS = 1.0


class StructureChecker(Checker):
    """
    Flags AI-characteristic structural patterns:
    - Paragraph fragmentation (too many short paragraphs)
    - Bullet point overuse
    """

    name = "structure"

    def check(self, text: str, context: DocumentContext) -> list[Finding]:
        findings: list[Finding] = []

        paragraphs = split_paragraphs(text)
        if not paragraphs:
            return []

        para_word_counts = [word_count(p) for p in paragraphs if word_count(p) > 0]
        avg_para_words = sum(para_word_counts) / len(para_word_counts) if para_word_counts else 0
        total_words = word_count(text)
        list_items = count_list_items(text)

        threshold = MIN_HEALTHY_PARA_WORDS_TECH if context.technical else MIN_HEALTHY_PARA_WORDS

        if avg_para_words > 0 and avg_para_words < threshold:
            severity = Severity.MEDIUM
            findings.append(Finding(
                checker=self.name,
                rule_id="short_paragraphs",
                text="paragraph length",
                message=(
                    f"Average paragraph: {avg_para_words:.0f} words "
                    f"(aim for {threshold}+ words). "
                    "AI fragments text into many short paragraphs."
                ),
                severity=severity,
                alternative="Combine related ideas into longer, developed paragraphs",
                context=(
                    f"{len(para_word_counts)} paragraphs, "
                    f"avg {avg_para_words:.0f} words each"
                ),
            ))

        if total_words > 0:
            list_density = list_items / total_words * 100
            if list_density > MAX_LIST_ITEMS_PER_100_WORDS:
                findings.append(Finding(
                    checker=self.name,
                    rule_id="bullet_overuse",
                    text="bullet points",
                    message=(
                        f"{list_items} list items in {total_words} words "
                        f"({list_density:.1f}/100 words). "
                        "AI overuses bullet points; human writing uses prose."
                    ),
                    severity=Severity.MEDIUM,
                    alternative="Convert lists to prose paragraphs where possible",
                    context=f"{list_items} list items, {total_words} total words",
                ))

        return findings
