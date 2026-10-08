# PlainRelease

Local micro-tool that lints a public changelog before you paste it into a customer email, status page, or in-app widget.

Solo founders write release notes in engineer voice. Customers then see ticket ids, "refactor", and "idempotent" instead of what actually changed for them. PlainRelease is a deterministic checker: no model key, no account, notes stay on disk.

Signature: Mourad.Soltani

## What it flags

- Missing version heading (`## 1.4.0`)
- Empty notes or notes with no bullets
- Internal ticket ids (`PROJ-184`, `#1042`)
- Internal jargon with a plain-language swap
- Bullets that never say what the user can do now

Warnings do not fail the run. Missing structure does.

## Install

```bash
python -m pip install -e .
plainrelease --health
```

## Use

```bash
plainrelease examples/CHANGELOG.md --html report.html --json report.json
```

Exit `0` when structure is valid. Exit `1` when a version heading or bullets are missing. Exit `2` when the file is missing.

## Tests

```bash
python -m pytest -q
```

## Buyer notes

See `BUYER_NOTES.md` and `OUTREACH_TEMPLATES.md`. Templates are for one-to-one messages you send yourself. This repo does not send email.
