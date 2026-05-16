"""Output formatters for CheckResult."""

from __future__ import annotations

import json as _json
from collections import defaultdict

from ._models import CheckResult, Finding
from .scoring import get_grade

try:
    from jinja2 import Template as _Template
except ImportError:
    _Template = None  # type: ignore[assignment, misc]


def format_text(result: CheckResult, filename: str, verbose: bool = False) -> str:
    """Format a CheckResult as plain text."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"Writing Analysis: {filename}")
    lines.append("=" * 60)
    lines.append(f"Words: {result.word_count:,}")
    lines.append(f"Section: {result.section_type.value}")
    lines.append(f"Patterns found: {len(result.findings)}")
    lines.append(f"  High severity: {len(result.high)}")
    lines.append(f"  Medium severity: {len(result.medium)}")
    lines.append("")
    lines.append(f"Score: {result.score}/100 ({get_grade(result.score)})")
    lines.append("")

    if result.high:
        lines.append("-" * 60)
        lines.append("HIGH SEVERITY")
        lines.append("-" * 60)
        for f in sorted(result.high, key=lambda x: x.rule_id)[:15]:
            alt = f" -> {f.alternative}" if f.alternative else ""
            lines.append(f'  [{f.checker}] "{f.text}"{alt}')
            if verbose and f.context:
                lines.append(f"       {f.context}")
            if verbose and f.message:
                lines.append(f"       {f.message}")
        lines.append("")

    if result.medium and verbose:
        lines.append("-" * 60)
        lines.append("MEDIUM SEVERITY")
        lines.append("-" * 60)
        for f in sorted(result.medium, key=lambda x: x.rule_id)[:10]:
            alt = f" -> {f.alternative}" if f.alternative else ""
            lines.append(f'  [{f.checker}] "{f.text}"{alt}')
            if f.context:
                lines.append(f"       {f.context}")
        lines.append("")

    if verbose and result.findings:
        lines.append("-" * 60)
        lines.append("BY CHECKER")
        lines.append("-" * 60)
        by_checker: dict[str, int] = defaultdict(int)
        for f in result.findings:
            by_checker[f.checker] += 1
        for checker, count in sorted(by_checker.items()):
            lines.append(f"  {checker}: {count} finding(s)")
        lines.append("")

    if result.high:
        lines.append("-" * 60)
        lines.append("SUGGESTIONS")
        lines.append("-" * 60)
        suggestions = {
            f'Replace "{f.text}" with: {f.alternative}'
            for f in result.high[:5]
            if f.alternative and not f.alternative.startswith("(")
        }
        for s in list(suggestions)[:5]:
            lines.append(f"  - {s}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def format_json(result: CheckResult, filename: str) -> str:
    """Format a CheckResult as JSON."""
    def _finding_dict(f: Finding) -> dict:
        return {
            "checker": f.checker,
            "rule_id": f.rule_id,
            "text": f.text,
            "message": f.message,
            "severity": f.severity.value,
            "alternative": f.alternative,
            "context": f.context,
        }

    output = {
        "filename": filename,
        "score": result.score,
        "grade": get_grade(result.score),
        "word_count": result.word_count,
        "section_type": result.section_type.value,
        "stats": {
            "total_findings": len(result.findings),
            "high_severity": len(result.high),
            "medium_severity": len(result.medium),
        },
        "high_severity": [_finding_dict(f) for f in result.high],
        "medium_severity": [_finding_dict(f) for f in result.medium],
    }
    return _json.dumps(output, indent=2)


def format_json_batch(results: list[tuple[str, CheckResult]]) -> str:
    """Format multiple file results as JSON."""
    files = []
    for filename, result in results:
        files.append({
            "filename": filename,
            "score": result.score,
            "grade": get_grade(result.score),
            "stats": {
                "total_findings": len(result.findings),
                "high_severity": len(result.high),
                "medium_severity": len(result.medium),
            },
        })
    total = len(files)
    passing = sum(1 for _, r in results if r.score >= 60)
    avg = sum(r.score for _, r in results) / total if total else 0
    return _json.dumps({
        "files": files,
        "summary": {
            "total_files": total,
            "passing": passing,
            "failing": total - passing,
            "average_score": round(avg, 1),
        },
    }, indent=2)


# HTML output

_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Writing Analysis Report</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.6;color:#333;max-width:900px;margin:0 auto;padding:20px;background:#f5f5f5}
.report{background:#fff;border-radius:8px;padding:30px;box-shadow:0 2px 10px rgba(0,0,0,.1)}
h1{color:#2c3e50;margin-bottom:20px;font-size:1.8em}
h2{color:#34495e;margin:25px 0 15px;font-size:1.3em;border-bottom:2px solid #eee;padding-bottom:8px}
.score-gauge{display:flex;align-items:center;gap:20px;margin:20px 0;padding:20px;background:#f8f9fa;border-radius:8px}
.score-number{font-size:3em;font-weight:bold}
.score-excellent{color:#27ae60}.score-good{color:#2ecc71}.score-fair{color:#f39c12}.score-poor{color:#e67e22}.score-bad{color:#e74c3c}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin:20px 0}
.stat-box{background:#f8f9fa;padding:15px;border-radius:6px;text-align:center}
.stat-value{font-size:1.8em;font-weight:bold;color:#2c3e50}
.stat-label{color:#7f8c8d;font-size:.9em}
.finding{display:flex;align-items:flex-start;gap:15px;padding:12px;margin:8px 0;border-radius:6px;border-left:4px solid}
.finding-high{background:#fdf2f2;border-color:#e74c3c}
.finding-medium{background:#fef6e7;border-color:#f39c12}
.finding-badge{background:#fff;padding:4px 8px;border-radius:4px;font-size:.8em;font-weight:bold;white-space:nowrap}
.finding-high .finding-badge{color:#e74c3c}
.finding-medium .finding-badge{color:#f39c12}
.finding-content{flex:1}
.finding-pattern{font-weight:600}
.finding-alt{color:#27ae60;font-size:.9em}
.finding-ctx{color:#7f8c8d;font-size:.85em;margin-top:4px;font-style:italic}
footer{margin-top:30px;padding-top:20px;border-top:1px solid #eee;color:#7f8c8d;font-size:.85em;text-align:center}
</style>
</head>
<body>
<div class="report">
<h1>Writing Analysis Report</h1>
<p><strong>File:</strong> {{ filename }}</p>
<p><strong>Section:</strong> {{ section_type }}</p>
<div class="score-gauge">
  <div class="score-number {{ score_class }}">{{ score }}</div>
  <div><div style="margin-bottom:8px;font-weight:600">{{ grade }}</div></div>
</div>
<div class="stats">
  <div class="stat-box"><div class="stat-value">{{ word_count }}</div><div class="stat-label">Words</div></div>
  <div class="stat-box"><div class="stat-value">{{ total_findings }}</div><div class="stat-label">Findings</div></div>
  <div class="stat-box"><div class="stat-value" style="color:#e74c3c">{{ high_count }}</div><div class="stat-label">High</div></div>
  <div class="stat-box"><div class="stat-value" style="color:#f39c12">{{ medium_count }}</div><div class="stat-label">Medium</div></div>
</div>
{% if high_findings %}
<h2>High Severity ({{ high_findings|length }})</h2>
{% for f in high_findings %}
<div class="finding finding-high">
  <div class="finding-badge">{{ f.checker }}</div>
  <div class="finding-content">
    <div class="finding-pattern">"{{ f.text }}"</div>
    {% if f.alternative %}<div class="finding-alt">-> {{ f.alternative }}</div>{% endif %}
    {% if f.context %}<div class="finding-ctx">{{ f.context }}</div>{% endif %}
  </div>
</div>
{% endfor %}
{% endif %}
{% if medium_findings %}
<h2>Medium Severity ({{ medium_findings|length }})</h2>
{% for f in medium_findings %}
<div class="finding finding-medium">
  <div class="finding-badge">{{ f.checker }}</div>
  <div class="finding-content">
    <div class="finding-pattern">"{{ f.text }}"</div>
    {% if f.alternative %}<div class="finding-alt">-> {{ f.alternative }}</div>{% endif %}
    {% if f.context %}<div class="finding-ctx">{{ f.context }}</div>{% endif %}
  </div>
</div>
{% endfor %}
{% endif %}
<footer>Generated by prose-check | Score: {{ score }}/100</footer>
</div>
<script>
function toggleSection(el){el.classList.toggle('collapsed');el.nextElementSibling.classList.toggle('hidden');}
</script>
</body>
</html>"""


def _score_class(score: int) -> str:
    if score >= 90:
        return "score-excellent"
    if score >= 75:
        return "score-good"
    if score >= 60:
        return "score-fair"
    if score >= 40:
        return "score-poor"
    return "score-bad"


def format_html(result: CheckResult, filename: str) -> str:
    """Format a CheckResult as HTML."""
    ctx = {
        "filename": filename,
        "section_type": result.section_type.value,
        "score": result.score,
        "score_class": _score_class(result.score),
        "grade": get_grade(result.score),
        "word_count": result.word_count,
        "total_findings": len(result.findings),
        "high_count": len(result.high),
        "medium_count": len(result.medium),
        "high_findings": result.high[:15],
        "medium_findings": result.medium[:10],
    }
    if _Template is not None:
        return _Template(_HTML_TEMPLATE).render(**ctx)
    # Minimal fallback
    return (
        f"<!DOCTYPE html><html><head><title>Writing Analysis</title></head><body>"
        f"<h1>{filename}</h1><p>Score: {result.score}/100 ({get_grade(result.score)})</p>"
        f"<p>High: {len(result.high)} | Medium: {len(result.medium)}</p></body></html>"
    )
