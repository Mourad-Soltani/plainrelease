# Mourad.Soltani — PlainRelease
"""HTML and JSON report writers."""

from __future__ import annotations

import html
import json
from pathlib import Path

from plainrelease.lint import LintResult


def write_json(result: LintResult, path: Path) -> None:
    path.write_text(json.dumps(result.to_dict(), indent=2) + "\n", encoding="utf-8")


def write_html(result: LintResult, path: Path, title: str = "PlainRelease report") -> None:
    rows = []
    for item in result.findings:
        rows.append(
            "<tr>"
            f"<td>{item.line}</td>"
            f"<td>{html.escape(item.severity)}</td>"
            f"<td>{html.escape(item.rule)}</td>"
            f"<td>{html.escape(item.message)}</td>"
            f"<td>{html.escape(item.suggestion)}</td>"
            "</tr>"
        )
    body = "\n".join(rows) or "<tr><td colspan='5'>No findings.</td></tr>"
    status = "ready to publish" if result.ok else "needs a version heading or bullets"
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Georgia, serif; margin: 2rem; color: #1c1917; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border-bottom: 1px solid #d6d3d1; text-align: left; padding: 0.4rem; vertical-align: top; }}
    .meta {{ color: #57534e; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p class="meta">Signed Mourad.Soltani · status: {html.escape(status)} · findings: {result.stats.get("findings", 0)}</p>
  <table>
    <thead><tr><th>Line</th><th>Severity</th><th>Rule</th><th>Message</th><th>Suggestion</th></tr></thead>
    <tbody>
      {body}
    </tbody>
  </table>
</body>
</html>
"""
    path.write_text(document, encoding="utf-8")
