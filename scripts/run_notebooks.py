"""Execute a representative subset of the lab notebooks headlessly.

Notebooks load their CSVs with paths relative to their own folder
(``../data/...``), so each notebook is executed with its directory as the
working directory. Every notebook is statically validated by
``validate_notebooks.py``; this script runs a subset that only uses local or
bundled datasets, keeping CI fast and offline. Notebooks that download data
(``fetch_california_housing``) are intentionally excluded.

Run from the repository root::

    python scripts/run_notebooks.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

os.environ.setdefault("MPLBACKEND", "Agg")  # no display in CI

ROOT = Path(__file__).resolve().parent.parent

SUBSET = [
    "Linear Regression/23cse301-linearregression-01.ipynb",
    "Linear Regression/23cse301-linearregression-03.ipynb",
    "Logistic Regression/23cse301-logisticregression-01.ipynb",
    "Logistic Regression/23cse301-logisticregression-02.ipynb",
    "Decison Tree Classifier/23cse301-decisiontree-01.ipynb",
    "K Nearest Neighbors/23cse301-knn-01.ipynb",
    "K Nearest Neighbors/23cse301-knn-02.ipynb",
    "K Means Clustering/23cse301-kmeans-01.ipynb",
    "K Means Clustering/23cse301-kmeans-02.ipynb",
    "Principal Component Analysis/23cse301-pca-01.ipynb",
    "Random Forests/23cse301-randomforest-01.ipynb",
    "Support Vector Machine/23cse301-svm-01.ipynb",
    "Support Vector Machine/23cse301-svm-03.ipynb",
]

TIMEOUT = 600  # seconds per cell


def run(relative: str) -> str | None:
    """Execute one notebook; return an error message, or None on success."""
    path = ROOT / relative
    if not path.exists():
        return "notebook is missing"

    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=TIMEOUT,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    try:
        client.execute()
    except CellExecutionError as exc:
        return str(exc)
    except Exception as exc:  # noqa: BLE001 - kernel/timeout failures
        return f"{type(exc).__name__}: {exc}"
    return None


def main() -> int:
    failures = 0
    for relative in SUBSET:
        error = run(relative)
        if error is None:
            print(f"ok   {relative}")
        else:
            failures += 1
            print(f"FAIL {relative}\n{error}\n")

    print(f"\nExecuted {len(SUBSET)} notebooks, {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
