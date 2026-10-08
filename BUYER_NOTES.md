# Buyer notes — PlainRelease

Signature: Mourad.Soltani

## Product

PlainRelease is a local CLI that lints a public changelog before it is pasted into a customer email, status page, or in-app widget. It flags leaked ticket ids, internal jargon, and bullets with no user impact. It does not call a model and it does not upload the note.

## Who pays

Solo SaaS founders and support leads who write their own release notes and have already been asked "what does this mean for me?" Price band to test: $9–$19/month for a hosted paste box, or a one-time $49 local license. Do not discount below the cost of one avoided support thread.

## What is shipped

- CLI with `--health`
- JSON and HTML reports
- Pytest health and lint coverage
- Sample changelog

## What a buyer still has to do

- Hosted paste UI and Stripe, if they want recurring revenue
- Custom jargon dictionary per product
- Widget embed, if they sell this next to a changelog page

## Proof to show a buyer

Run `python -m pytest -q` and `plainrelease examples/CHANGELOG.md --html report.html`. The sample file is intentionally messy.

## Non-goals

No cold email is sent from this repo. Outreach templates are drafts only.
