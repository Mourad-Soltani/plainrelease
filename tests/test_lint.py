# Mourad.Soltani — PlainRelease lint tests

from plainrelease.lint import lint_notes
from plainrelease.report import write_html, write_json


def test_flags_jargon_and_ticket():
    text = """## 1.4.0

- Refactor billing payload handler (PROJ-184) to be idempotent.
- You can now download invoices again when the file is large.
"""
    result = lint_notes(text)
    rules = {item.rule for item in result.findings}
    assert "internal-jargon" in rules
    assert "leaked-ticket" in rules
    assert result.ok


def test_missing_version_is_error():
    text = "- You can now export invoices.\n"
    result = lint_notes(text)
    assert not result.ok
    assert any(item.rule == "missing-version" for item in result.findings)


def test_reports_roundtrip(tmp_path):
    text = """## 2.0.0

- Fixed search so your filters stay applied after reload.
"""
    result = lint_notes(text)
    json_path = tmp_path / "report.json"
    html_path = tmp_path / "report.html"
    write_json(result, json_path)
    write_html(result, html_path)
    assert "findings" in json_path.read_text(encoding="utf-8")
    assert "Mourad.Soltani" in html_path.read_text(encoding="utf-8")
