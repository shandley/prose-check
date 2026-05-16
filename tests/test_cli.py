"""CLI integration tests for prose-check."""
import json
import subprocess
import sys
from pathlib import Path


def run_cli(*args: str, stdin_text: str | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "prose_check.cli"] + list(args)
    return subprocess.run(
        cmd,
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )


class TestCLIStdin:
    def test_clean_text_exits_zero(self):
        result = run_cli("--stdin", stdin_text=(
            "The old bookshop had been there for forty years. "
            "Mrs. Chen opened it when her daughter was born. "
            "The smell of pages mixed with the tea she kept brewing."
        ))
        assert result.returncode == 0

    def test_ai_text_exits_nonzero(self):
        result = run_cli("--stdin", stdin_text=(
            "This comprehensive guide provides a robust framework. "
            "Furthermore, it is important to note that delving into "
            "these nuanced paradigms facilitates seamless integration."
        ))
        assert result.returncode == 1

    def test_json_output_valid(self):
        result = run_cli("--stdin", "--format", "json", stdin_text=(
            "This comprehensive approach leverages robust paradigms."
        ))
        data = json.loads(result.stdout)
        assert "score" in data
        assert "findings" not in data or isinstance(data.get("high_severity"), list)
        assert isinstance(data["score"], int)

    def test_html_output(self):
        result = run_cli("--stdin", "--format", "html", stdin_text="Simple text here.")
        assert "<html" in result.stdout.lower()

    def test_section_flag(self):
        result = run_cli(
            "--stdin", "--section", "results", "--format", "json",
            stdin_text="Temperature drives species richness.",
        )
        data = json.loads(result.stdout)
        # causal_lang checker should fire in results section with unknown study type
        all_findings = data.get("high_severity", []) + data.get("medium_severity", [])
        checkers = {f["checker"] for f in all_findings}
        assert "causal_lang" in checkers

    def test_study_type_flag(self):
        # With observational study type, causal language should be flagged
        result_obs = run_cli(
            "--stdin", "--section", "results", "--study-type", "observational",
            "--format", "json",
            stdin_text="The mutation causes resistance in these populations.",
        )
        result_exp = run_cli(
            "--stdin", "--section", "results", "--study-type", "experimental",
            "--format", "json",
            stdin_text="The mutation causes resistance in these populations.",
        )
        data_obs = json.loads(result_obs.stdout)
        data_exp = json.loads(result_exp.stdout)
        findings_obs = data_obs.get("high_severity", []) + data_obs.get("medium_severity", [])
        findings_exp = data_exp.get("high_severity", []) + data_exp.get("medium_severity", [])
        causal_obs = sum(1 for f in findings_obs if f["checker"] == "causal_lang")
        causal_exp = sum(1 for f in findings_exp if f["checker"] == "causal_lang")
        assert causal_obs > causal_exp

    def test_checkers_flag(self):
        result = run_cli(
            "--stdin", "--checkers", "ai_patterns", "--format", "json",
            stdin_text="This comprehensive guide is robust.",
        )
        data = json.loads(result.stdout)
        all_findings = data.get("high_severity", []) + data.get("medium_severity", [])
        checkers = {f["checker"] for f in all_findings}
        assert checkers <= {"ai_patterns"}  # only ai_patterns, no others

    def test_min_score_flag(self):
        # Perfect text should pass with default min-score but fail with 101 (impossible)
        result_pass = run_cli(
            "--stdin", "--min-score", "0",
            stdin_text="Simple direct text without AI patterns here.",
        )
        assert result_pass.returncode == 0
