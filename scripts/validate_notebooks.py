"""Static validation for the lab notebooks.

Every notebook is checked to be valid nbformat JSON, every code cell must
compile, every top-level import must resolve to an installed package, and every
locally referenced dataset must exist on disk. This runs fast on every push;
executing a representative subset is handled by ``run_notebooks.py``.

Run from the repository root::

    python scripts/validate_notebooks.py
"""

from __future__ import annotations

import ast
import importlib.util
import re
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent

# Lines that begin with these markers are IPython magics/shell escapes and are
# not valid Python, so they are stripped before the syntax check.
MAGIC_PREFIXES = ("%", "!", "?")

# ``pd.read_csv('../data/foo.csv')`` style references to local files.
READ_CALL = re.compile(r"""read_(?:csv|table|json)\(\s*['"]([^'"]+)['"]""")


def code_cells(notebook: nbformat.NotebookNode) -> list[str]:
    return [c.source for c in notebook.cells if c.cell_type == "code"]


def strip_magics(source: str) -> str:
    return "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith(MAGIC_PREFIXES)
    )


def imported_modules(source: str) -> set[str]:
    """Top-level module names imported by a code cell, ignoring syntax noise."""
    modules: set[str] = set()
    try:
        tree = ast.parse(strip_magics(source))
    except SyntaxError:
        return modules
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def main() -> int:
    notebooks = sorted(ROOT.rglob("*.ipynb"))
    if not notebooks:
        print("No notebooks found.", file=sys.stderr)
        return 1

    errors: list[str] = []
    checked_imports: set[str] = set()

    for path in notebooks:
        rel = path.relative_to(ROOT).as_posix()
        try:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
        except Exception as exc:  # noqa: BLE001 - report any parse/validation failure
            errors.append(f"{rel}: invalid notebook ({exc})")
            continue

        for index, source in enumerate(code_cells(notebook)):
            stripped = strip_magics(source)
            try:
                compile(stripped, f"{rel}#cell{index}", "exec")
            except SyntaxError as exc:
                errors.append(f"{rel}: cell {index} does not compile ({exc.msg})")

            checked_imports |= imported_modules(source)

            for target in READ_CALL.findall(source):
                if "://" in target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    errors.append(f"{rel}: dataset not found -> {target}")

    for module in sorted(checked_imports):
        if importlib.util.find_spec(module) is None:
            errors.append(f"import not installed: {module}")

    print(f"Scanned {len(notebooks)} notebooks, {len(checked_imports)} unique imports.")
    if errors:
        print("\nFailures:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("All notebooks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
