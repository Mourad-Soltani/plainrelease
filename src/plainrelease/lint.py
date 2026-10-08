# Mourad.Soltani — PlainRelease
"""Rule tables and deterministic checks for public release notes."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field


JARGON = {
    "refactor": "reorganized the code behind this so it is easier to change later",
    "idempotent": "safe to run more than once with the same result",
    "race condition": "two actions could finish in the wrong order",
    "regression": "a problem that came back after a previous fix",
    "hotfix": "an urgent fix shipped outside the normal release",
    "debounce": "waits briefly so repeated clicks count as one action",
    "throttle": "limits how often an action can run",
    "payload": "the data sent with the request",
    "endpoint": "the address the app calls",
    "schema": "the shape of the saved data",
    "migration": "a one-time update to stored data",
    "null pointer": "a missing value the app did not expect",
    "n+1": "the app was asking for related data one row at a time",
    "cache invalidation": "clearing saved answers so the next view is fresh",
    "deadlock": "two tasks waiting on each other and never finishing",
    "sharding": "splitting stored data so each piece stays smaller",
    "webhook": "a message the app sends to another system when something happens",
    "cron": "a scheduled job that runs on a timer",
    "rollback": "returning to the previous version",
    "feature flag": "a switch that turns a change on for some people only",
}

TICKET_RE = re.compile(
    r"\b(?:[A-Z]{2,10}-\d+|GH-\d+|#\d{3,})\b"
)
VERSION_RE = re.compile(
    r"^#{1,3}\s+\[?v?\d+\.\d+\.\d+\]?",
    re.IGNORECASE | re.MULTILINE,
)
BULLET_RE = re.compile(r"^\s*[-*]\s+(.+)$")


@dataclass
class Finding:
    rule: str
    severity: str
    line: int
    message: str
    excerpt: str
    suggestion: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LintResult:
    ok: bool
    findings: list[Finding] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "stats": self.stats,
            "findings": [item.to_dict() for item in self.findings],
        }


def _suggestion_for(text: str) -> str:
    lowered = text.lower()
    hits = [plain for term, plain in JARGON.items() if term in lowered]
    if not hits:
        return "Say what the person using the product can now do, or what stopped breaking."
    return "Try: " + "; ".join(hits[:2]) + "."


def lint_notes(text: str) -> LintResult:
    """Lint a markdown changelog or release note."""
    findings: list[Finding] = []
    lines = text.splitlines()
    bullets = 0
    jargon_hits = 0

    if not text.strip():
        findings.append(
            Finding(
                rule="empty",
                severity="error",
                line=1,
                message="Release note is empty.",
                excerpt="",
                suggestion="Add a version heading and at least one user-facing bullet.",
            )
        )
        return LintResult(ok=False, findings=findings, stats={"bullets": 0, "lines": 0})

    if not VERSION_RE.search(text):
        findings.append(
            Finding(
                rule="missing-version",
                severity="error",
                line=1,
                message="No version heading like ## 1.2.0 or ## [1.2.0].",
                excerpt=lines[0][:120] if lines else "",
                suggestion="Start with a version heading so readers know which release this is.",
            )
        )

    for index, line in enumerate(lines, start=1):
        bullet = BULLET_RE.match(line)
        if not bullet:
            continue
        bullets += 1
        body = bullet.group(1).strip()
        lowered = body.lower()

        for match in TICKET_RE.findall(body):
            findings.append(
                Finding(
                    rule="leaked-ticket",
                    severity="warning",
                    line=index,
                    message=f"Internal ticket id {match} is visible to customers.",
                    excerpt=body[:160],
                    suggestion="Drop the ticket id or move it to an internal appendix.",
                )
            )

        for term, plain in JARGON.items():
            if re.search(rf"\b{re.escape(term)}\b", lowered):
                jargon_hits += 1
                findings.append(
                    Finding(
                        rule="internal-jargon",
                        severity="warning",
                        line=index,
                        message=f"Internal term '{term}' is hard for customers to parse.",
                        excerpt=body[:160],
                        suggestion=plain,
                    )
                )

        has_user_word = any(
            token in lowered
            for token in (
                "you",
                "your",
                "users",
                "customers",
                "can now",
                "no longer",
                "fixed",
                "faster",
                "when you",
            )
        )
        if len(body) < 24 or not has_user_word:
            findings.append(
                Finding(
                    rule="missing-user-impact",
                    severity="warning",
                    line=index,
                    message="Bullet does not say what changed for the person using the product.",
                    excerpt=body[:160],
                    suggestion=_suggestion_for(body),
                )
            )

    if bullets == 0:
        findings.append(
            Finding(
                rule="no-bullets",
                severity="error",
                line=1,
                message="No markdown bullets found.",
                excerpt="",
                suggestion="Write one bullet per change, starting with what the user can do now.",
            )
        )

    errors = [item for item in findings if item.severity == "error"]
    stats = {
        "lines": len(lines),
        "bullets": bullets,
        "jargon_hits": jargon_hits,
        "findings": len(findings),
        "errors": len(errors),
    }
    return LintResult(ok=len(errors) == 0, findings=findings, stats=stats)
