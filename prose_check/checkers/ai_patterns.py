"""AI writing pattern checker -- flags LLM-characteristic words and phrases."""

from __future__ import annotations

import re
from functools import cached_property

from .._markers import load_markers
from .._models import DocumentContext, Finding, Severity
from .._text import find_context, word_count
from . import Checker

# -- Exclusion sets -----------------------------------------------------------

MARKDOWN_PATTERNS: set[str] = {
    "##", "###", "####", "#####",
    "```", "``", "`",
    "**", "__", "*", "_",
    "---", "***", "___",
    "- [", "- [ ]", "- [x]",
    "|", "|-", ">",
}

TRAINING_ARTIFACTS: set[str] = {
    "jenna", "marcus", "margaret", "chen", "sarah", "mike", "david",
    "alex", "tom", "lisa", "john", "james", "emma", "emily",
    "**marcus**", "**jenna**", "**margaret:**", "**the",
}

TECHNICAL_TERMS: set[str] = {
    # Languages & frameworks
    "python", "javascript", "typescript", "java", "rust", "go", "ruby",
    "react", "vue", "angular", "node", "django", "flask", "rails",
    "bash", "shell", "powershell", "perl", "php", "scala", "kotlin",
    # Infrastructure & tools
    "docker", "kubernetes", "aws", "azure", "gcp", "linux", "unix",
    "git", "github", "gitlab", "npm", "yarn", "pip", "cargo",
    "terraform", "ansible", "jenkins", "circleci", "travis",
    # Concepts
    "api", "apis", "rest", "graphql", "sql", "nosql", "json", "xml",
    "html", "css", "http", "https", "url", "uri", "oauth", "jwt",
    "microservices", "monolith", "serverless", "devops", "ci", "cd",
    "frontend", "backend", "fullstack", "database", "cache", "cdn",
    "tdd", "bdd", "agile", "scrum", "sprint", "kanban",
    # AI/ML
    "ai", "ml", "llm", "gpt", "nlp", "neural", "model", "training",
    "pytorch", "tensorflow", "keras", "sklearn", "pandas", "numpy",
    # Documentation
    "readme", "changelog", "documentation", "docs", "wiki",
    "technical", "specification", "requirements", "architecture",
}

PROGRAMMING_TERMS: set[str] = {
    "code", "function", "method", "class", "variable", "parameter",
    "argument", "return", "loop", "array", "object", "string",
    "integer", "boolean", "null", "undefined", "import", "export",
    "module", "package", "library", "framework", "dependency",
    "error", "errors", "exception", "bug", "bugs", "debug",
    "test", "tests", "testing", "unit", "integration",
    "deploy", "deployment", "build", "compile", "runtime",
    "server", "client", "request", "response", "endpoint",
    "query", "mutation", "schema", "type", "interface",
    "pattern", "patterns", "config", "configuration",
    "environment", "production", "staging",
    "log", "logs", "logging", "monitor", "monitoring",
    "async", "await", "promise", "callback", "event",
    "postgresql", "mysql", "mongodb", "redis", "sqlite",
    "table", "column", "row", "index", "migration",
    "authentication", "authorization", "token", "tokens", "session",
    "credentials", "password", "username", "login", "logout",
    "permission", "permissions", "role", "roles", "user", "users",
    "timestamp", "timeout", "expiration", "pagination", "validation",
    "serialization", "deserialization", "middleware", "handler",
    "controller", "service", "repository", "factory", "singleton",
    "requests", "responses", "headers", "payload", "body",
    "context", "contexts", "conventions", "convention", "document", "documents",
    "documentation", "limiting", "limits", "limit", "specified", "specify",
    "parameters", "values", "value", "options", "option", "settings",
    "format", "formats", "output", "input", "inputs", "outputs",
    "process", "processes", "processing", "handle", "handling",
}

TECHNICAL_PHRASES: set[str] = {
    "error handling", "rate limiting", "rest api", "api endpoint",
    "api endpoints", "user id", "access token", "http status",
    "status code", "query string", "request body", "response body",
    "json response", "best practices", "use case", "use cases",
    "data model", "file format", "return value", "input data",
    "output data", "default value",
}

# -- Pattern data -------------------------------------------------------------

# AI overuses these hedging words (ratios from corpus analysis)
HEDGING_WORDS: dict[str, float] = {
    "typically": 9.6,
    "often": 4.9,
    "sometimes": 4.2,
    "potentially": 3.4,
    "usually": 3.4,
    "rather": 3.3,
    "probably": 2.2,
}

FORMULAIC_STARTERS: list[str] = [
    "this document",
    "this guide",
    "this article",
    "this section",
    "comprehensive",
    "in this",
    "introduction",
    "let's",
]

# Alternatives: item.lower() -> human-friendly replacement (first element shown in output)
ALTERNATIVES: dict[str, list[str]] = {
    # LLM-favorite words
    "delve": ["explore", "examine", "look at"],
    "tapestry": ["mix", "combination", "range"],
    "multifaceted": ["complex", "varied"],
    "embark": ["start", "begin"],
    "plethora": ["many", "lots of"],
    "myriad": ["many", "numerous"],
    "aforementioned": ["this", "that", "the"],
    "seamlessly": ["smoothly", "easily"],
    "meticulous": ["careful", "thorough"],
    "intricate": ["complex", "detailed"],
    "comprehensive": ["complete", "full", "thorough"],
    "utilize": ["use"],
    "leverage": ["use", "apply"],
    "paramount": ["most important", "critical"],
    "groundbreaking": ["new", "novel"],
    "synergy": ["(delete or restate specifically)"],
    "holistic": ["broad", "complete", "overall"],
    "impactful": ["significant", "effective"],
    "pivotal": ["key", "central", "important"],
    "endeavor": ["effort", "attempt", "try"],
    "facilitate": ["help", "enable", "make easier"],
    "realm": ["area", "field"],
    "transformative": ["significant", "major"],
    "streamline": ["simplify", "improve"],
    "fostering": ["building", "encouraging"],
    "proactive": ["active", "preventive"],
    "nuanced": ["subtle", "detailed"],
    "underscore": ["show", "highlight", "emphasize"],
    "landscape": ["field", "area", "situation"],
    "paradigm": ["model", "approach"],
    "foster": ["encourage", "support", "build"],
    "navigate": ["handle", "manage", "work through"],
    "robust": ["strong", "solid"],
    "crucial": ["important", "key"],
    "vital": ["essential", "important"],
    "innovative": ["new", "original"],
    "noteworthy": ["notable", "worth mentioning"],
    # Hedging phrases
    "it's important to note": ["(delete)"],
    "it is important to note": ["(delete)"],
    "it's worth noting": ["(delete)"],
    "it is worth noting": ["(delete)"],
    "it should be noted": ["(delete)"],
    "it is worth mentioning": ["(delete)"],
    "needless to say": ["(delete)"],
    "it goes without saying": ["(delete)"],
    "that being said": ["but", "however"],
    "having said that": ["but", "however"],
    "with that in mind": ["so", "given this"],
    "generally speaking": ["usually", "(delete)"],
    "in many cases": ["often", "(delete)"],
    # Filler phrases
    "in order to": ["to"],
    "due to the fact that": ["because"],
    "at the end of the day": ["ultimately", "(delete)"],
    "in today's world": ["(delete)"],
    "in the realm of": ["in"],
    "when it comes to": ["for", "with"],
    "serves as a": ["is a"],
    "plays a crucial role": ["is important", "matters"],
    "plays a key role": ["is important", "matters"],
    "in terms of": ["for", "regarding", "(delete)"],
    "with respect to": ["for", "about"],
    "at this point in time": ["now"],
    "for all intents and purposes": ["effectively", "(delete)"],
    "the fact that": ["that", "(restructure)"],
    # Structure phrases
    "let's dive into": ["(delete, just start)"],
    "let's explore": ["(delete, just start)"],
    "let's delve into": ["(delete, just start)"],
    "let me explain": ["(delete)"],
    "let's break this down": ["(delete)"],
    "here's the thing": ["(delete)"],
    "first and foremost": ["first"],
    "last but not least": ["finally", "also"],
    "let's look at": ["(delete, just start)"],
    # Conclusion phrases
    "in essence": ["basically", "(delete)"],
    "fundamentally": ["basically", "(delete)"],
    "essentially": ["basically", "(delete)"],
    "at its core": ["basically", "(delete)"],
    "in summary": ["(delete or just summarize)"],
    "in conclusion": ["(delete)"],
    "to summarize": ["(delete)"],
    "all in all": ["overall", "(delete)"],
    "overall": ["(delete if implied)"],
    "ultimately": ["(delete if implied)"],
    # Emphasis
    "absolutely": ["(delete)"],
    "undoubtedly": ["(delete)"],
    "without a doubt": ["(delete)"],
    "certainly": ["(delete)"],
    "definitely": ["(delete)"],
    "obviously": ["(delete)"],
    "clearly": ["(delete or show, don't tell)"],
    "of course": ["(delete)"],
    "naturally": ["(delete)"],
    "indeed": ["(delete)"],
    # Transitions (use sparingly)
    "furthermore": ["also", "and"],
    "moreover": ["also", "and"],
    "additionally": ["also", "and"],
    "conversely": ["but", "on the other hand"],
    "nevertheless": ["still", "but"],
    "nonetheless": ["still", "but"],
    "consequently": ["so", "as a result"],
    "accordingly": ["so"],
    "subsequently": ["then", "after that"],
    "in addition": ["also", "and"],
}

# Severity thresholds
HIGH_SEVERITY_LOG_ODDS = 2.5
MEDIUM_SEVERITY_LOG_ODDS = 1.5


def _log_odds_to_severity(log_odds: float) -> Severity:
    if log_odds >= HIGH_SEVERITY_LOG_ODDS:
        return Severity.HIGH
    elif log_odds >= MEDIUM_SEVERITY_LOG_ODDS:
        return Severity.MEDIUM
    return Severity.LOW


class AIPatternChecker(Checker):
    """Detects LLM-characteristic words and phrases using the curated markers database."""

    name = "ai_patterns"

    @cached_property
    def _markers(self) -> list[dict]:
        return load_markers()

    def check(self, text: str, context: DocumentContext) -> list[Finding]:
        findings: list[Finding] = []

        # Build exclusion set
        excluded: set[str] = set(MARKDOWN_PATTERNS) | TRAINING_ARTIFACTS
        if context.technical:
            excluded |= TECHNICAL_TERMS | PROGRAMMING_TERMS | TECHNICAL_PHRASES

        # -- Marker loop with deduplication (keep highest log_odds per pattern) --
        # seen: pattern_lower -> (finding_index_in_list, log_odds, severity_bucket)
        seen: dict[str, tuple[int, float, str]] = {}

        def _severity_bucket(s: Severity) -> str:
            return s.value  # "high" | "medium" | "low"

        for marker in self._markers:
            item: str = marker["item"]
            mtype: str = marker["type"]
            log_odds: float = marker["log_odds"]
            item_lower = item.lower().strip()

            if item in excluded or item_lower in excluded:
                continue
            if log_odds < MEDIUM_SEVERITY_LOG_ODDS:
                continue

            if mtype == "sentence_starter":
                pattern = re.compile(
                    r"(?:^|[.!?]\s+)" + re.escape(item), re.IGNORECASE | re.MULTILINE
                )
                matches = list(pattern.finditer(text))
            else:
                pattern = re.compile(r"\b" + re.escape(item) + r"\b", re.IGNORECASE)
                matches = list(pattern.finditer(text))

            if not matches:
                continue

            severity = _log_odds_to_severity(log_odds)
            ratio = (
                marker["opus_rate"] / marker["human_rate"]
                if marker.get("human_rate", 0) > 0
                else 999.0
            )
            alts = ALTERNATIVES.get(item_lower)
            alt_str = ", ".join(alts) if alts else None

            ctx_snippet = find_context(text, matches[0].start(), matches[0].end())

            finding = Finding(
                checker=self.name,
                rule_id=f"marker_{item_lower.replace(' ', '_')}",
                text=item,
                message=f'"{item}" appears {len(matches)}x ({ratio:.0f}x more common in AI text)',
                severity=severity,
                alternative=alt_str,
                context=ctx_snippet,
            )

            # Deduplication: keep the finding with the highest log_odds for this pattern
            if item_lower in seen:
                prev_idx, prev_log_odds, _ = seen[item_lower]
                if log_odds > prev_log_odds:
                    findings[prev_idx] = finding  # replace
                    seen[item_lower] = (prev_idx, log_odds, _severity_bucket(severity))
                # else skip: previous finding had higher confidence
            else:
                seen[item_lower] = (len(findings), log_odds, _severity_bucket(severity))
                findings.append(finding)

        # -- Em-dash check ----------------------------------------------------
        em_dash_count = text.count("—") + text.count("--")
        if em_dash_count > 0 and len(text) > 0:
            per_1k = em_dash_count / len(text) * 1000
            if per_1k > 1.0:  # >3.5x human average of 0.28
                findings.append(Finding(
                    checker=self.name,
                    rule_id="em_dash_overuse",
                    text="em dash (—)",
                    message=f"Em dashes: {per_1k:.1f}/1k chars (human avg 0.28). Mainly an Opus 4.5 pattern.",
                    severity=Severity.HIGH,
                    alternative="Use commas, periods, or parentheses instead",
                    context=f"{em_dash_count} em dashes in {len(text)} chars",
                ))

        # -- Hedging language overuse -----------------------------------------
        total_words = word_count(text)
        hedging_hits: list[str] = []
        hedging_total = 0
        for word, _ in HEDGING_WORDS.items():
            pat = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
            cnt = len(pat.findall(text))
            if cnt:
                hedging_total += cnt
                hedging_hits.append(f"{word}({cnt})")
        if total_words > 0:
            per_1k = hedging_total / total_words * 1000
            if per_1k > 8.0:  # ~1.7x human average of 4.8
                findings.append(Finding(
                    checker=self.name,
                    rule_id="hedging_overuse",
                    text="hedging language",
                    message=f"Hedging rate {per_1k:.1f}/1k words (human avg 4.8). Be more direct.",
                    severity=Severity.MEDIUM,
                    alternative="Be direct; reduce typically/often/sometimes/potentially",
                    context=", ".join(hedging_hits[:5]),
                ))

        # -- Formulaic sentence starters --------------------------------------
        sentences = re.split(r"[.!?]+", text)
        formulaic_count = 0
        formulaic_examples: list[str] = []
        for sent in sentences:
            sc = sent.strip().lower()
            for starter in FORMULAIC_STARTERS:
                if sc.startswith(starter):
                    formulaic_count += 1
                    if len(formulaic_examples) < 2:
                        formulaic_examples.append(sent.strip()[:50])
                    break
        if formulaic_count >= 2:
            findings.append(Finding(
                checker=self.name,
                rule_id="formulaic_starters",
                text="formulaic sentence openers",
                message=f"{formulaic_count} sentences begin with formulaic AI openers.",
                severity=Severity.MEDIUM,
                alternative='Vary sentence openings; avoid "This document/guide/section"',
                context="; ".join(formulaic_examples),
            ))

        return findings
