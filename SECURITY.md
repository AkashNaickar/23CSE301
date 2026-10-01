# Security Policy

This repository contains teaching notebooks for the 23CSE301 Machine Learning
course. It ships no server, no deployed service, and no credentials, so its
attack surface is limited to the code you run locally and the committed data
files.

## Supported versions

Only the current `main` branch is maintained. There are no tagged releases.

| Version | Supported |
|---------|-----------|
| `main` | Yes |
| Older commits | No |

## Reporting a vulnerability

Please report security issues **privately** using GitHub's
[private vulnerability reporting](https://github.com/AkashNaickar/23CSE301/security/advisories/new)
instead of opening a public issue. Include:

- A description of the issue and its impact.
- Steps to reproduce, or a minimal notebook/script that triggers it.
- The OS and Python version you used.

Do not include real secrets, access tokens, or personal data in the report.

This is a single-maintainer coursework repository, so responses are best effort.
If a report is valid you will be credited in the fix unless you prefer otherwise.

## Scope

In scope:

- Code execution that escapes the notebook sandbox while running a lab.
- A committed file that contains a real credential or personal data.
- A dependency with a known vulnerability that affects these labs.

Out of scope:

- Findings that require an already-compromised local machine.
- Scanner hits inside vendored third-party code in git history. A full
  virtualenv was committed in the root commit and removed later; its blobs
  remain in the pack, and `.gitleaks.toml` allowlists that historical `.venv/`
  path as false positives. See `NEEDS_ME.md` in the portfolio repo for the
  pending (optional, approval-gated) history rewrite.

## Secrets

CI runs gitleaks on every push and pull request. Never commit tokens, API keys,
or `.env` files; `.gitignore` excludes them. If you believe a real secret has
been committed, report it privately as above and treat it as compromised.
