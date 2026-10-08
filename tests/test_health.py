# Mourad.Soltani — PlainRelease health tests

import json
import subprocess
import sys
from pathlib import Path

from plainrelease.cli import main
from plainrelease.lint import lint_notes

ROOT = Path(__file__).resolve().parents[1]


def test_health_cli_json(capsys):
    code = main(["--health"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert code == 0
    assert payload["status"] == "ok"
    assert payload["service"] == "plainrelease"
    assert payload["author"] == "Mourad.Soltani"


def test_health_module_invocation():
    proc = subprocess.run(
        [sys.executable, "-m", "plainrelease.cli", "--health"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "PYTHONPATH": str(ROOT / "src")},
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["status"] == "ok"


def test_good_note_is_structurally_ok():
    text = """## 1.2.0\n\n- You can now export invoices without the file cutting off.\n"""
    result = lint_notes(text)
    assert result.ok
    assert result.stats["errors"] == 0


def test_empty_note_fails():
    result = lint_notes("   ")
    assert not result.ok
    assert result.findings[0].rule == "empty"
