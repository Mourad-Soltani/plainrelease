# Mourad.Soltani — PlainRelease
"""Command line for PlainRelease."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from plainrelease import __version__
from plainrelease.lint import lint_notes
from plainrelease.report import write_html, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="plainrelease",
        description="Lint public release notes for internal jargon. Mourad.Soltani.",
    )
    parser.add_argument("path", nargs="?", help="Markdown file to lint")
    parser.add_argument("--health", action="store_true", help="Print health JSON and exit")
    parser.add_argument("--json", dest="json_out", help="Write JSON report to this path")
    parser.add_argument("--html", dest="html_out", help="Write HTML report to this path")
    parser.add_argument("--version", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    if args.health:
        payload = {
            "status": "ok",
            "service": "plainrelease",
            "version": __version__,
            "author": "Mourad.Soltani",
        }
        print(json.dumps(payload))
        return 0
    if not args.path:
        parser.error("path is required unless --health or --version is set")
    source = Path(args.path)
    if not source.is_file():
        print(f"file not found: {source}", file=sys.stderr)
        return 2
    result = lint_notes(source.read_text(encoding="utf-8"))
    if args.json_out:
        write_json(result, Path(args.json_out))
    if args.html_out:
        write_html(result, Path(args.html_out), title=source.name)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
