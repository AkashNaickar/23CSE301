# Contributing

Thanks for taking the time to improve these labs. This repository holds the
Jupyter notebooks for the 23CSE301 Machine Learning course; changes are expected
to be small, focused, and easy to review.

## Before you start

- Open an issue describing the bug or the lab you want to change, unless the
  change is trivial (a typo or a broken link).
- One pull request should address one thing. Do not mix a notebook rewrite with
  a dependency bump.

## Development setup

Requires Python 3.12. Everything runs offline against the committed CSVs and the
datasets bundled with scikit-learn, except PCA 02, which downloads data on first
run.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Branch naming

Branch from `main`:

| Prefix | Use |
|--------|-----|
| `feat/` | New lab content or tooling |
| `fix/` | Correct a notebook, script, or dataset path |
| `docs/` | README and documentation changes |
| `chore/` | Dependency updates, CI, config |
| `refactor/` | Restructuring without changing results |

## Notebook conventions

- One lab per notebook, named `23cse301-<topic>-<number>.ipynb`, and listed in
  the README labs table.
- Keep notebooks runnable from the repository root. Use relative paths and the
  bundled data under `data/`; no absolute or machine-specific paths.
- Prefer the dependencies already pinned in `requirements.txt`. If a lab needs a
  new package, add the exact version there and explain why in the PR.
- Avoid network access unless the notebook is documented as network-backed in
  the README and excluded from the offline execution subset.
- Do not commit `.ipynb_checkpoints/`, a virtualenv, or large binary outputs.
- If you change a dataset, update the README data table and make sure every
  notebook that references it still points at the right file.

## Testing

Both checks run in CI and should pass locally before you open a pull request:

```bash
# Static checks: JSON validity, all code cells compile, imports resolve,
# and every referenced dataset exists.
python scripts/validate_notebooks.py

# Execute the offline notebook subset end to end.
MPLBACKEND=Agg python scripts/run_notebooks.py
```

On Windows PowerShell, set the backend first:
`$env:MPLBACKEND = "Agg"; python scripts/run_notebooks.py`.

## Commit messages

Small, logical, and imperative. Describe the change, not the file:

- `fix broken path in decision tree 02`
- `add elbow-plot explanation to k-means 01`
- `pin scikit-learn version`

Avoid generic messages such as "update files" and do not use emoji.

## Pull requests

Fill in the pull request template. Every PR should:

- Explain what changed and why.
- Keep CI green (notebook validation and the offline execution subset).
- Update the README if usage, data, or setup changed.
- Contain no secrets.

## Reporting bugs and security issues

Open an issue for lab bugs. For security issues, follow
[SECURITY.md](SECURITY.md) and report privately. All contributors are expected
to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
