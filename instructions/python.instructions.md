---
name: CRISP Python conventions
description: Python-specific coding conventions not enforced by formatters or linters.
applyTo: "**/*.py"
---

# Python Conventions

Formatting rules (single quotes, line length 100, import grouping, unused imports) are enforced by Ruff, Black, or project-configured formatters. This file covers conventions that tools cannot enforce.

---

## Imports

Prefer top-level imports. Permit local imports for:
- Optional dependencies (avoid `ImportError` at module load)
- Import-cycle avoidance
- Startup cost reduction
- Backend or runtime selection

Group by: built-in, installed/third-party, local package — separated by blank lines.

```python
import os
from pathlib import Path

import numpy as np

from mypackage import config
from mypackage.core.processor import process_data
```

---

## Module Layout

Prefer top-down module function layout (excluding the main entrypoint), ordered by call flow:

1. Top function (orchestrates A, B, C)
2. Subfunctions near their caller (A before B when called in that order)
3. Helpers immediately below their owning subfunction (A.1, A.2, then B.1, B.2)
4. Shared helpers at the bottom of the module

Keep this layout logical and readable rather than strictly mechanical; proximity should make call flow easy to follow. Very small one-purpose helpers may be nested inside a larger function when they are local to that function.

---

## Package Initializers

Keep package `__init__.py` files declarative. Re-exports, `__all__`, version metadata, and minimal package initialization are acceptable. Do not place domain logic in `__init__.py`.

---

## Dead Code

Before classifying code as dead, verify entry points, plugins, reflection, serialization, external API use, and test instrumentation. Remove genuinely dead code: unused variables, backward-compat shims, stale imports, commented-out blocks.

If any feature is removed from the codebase, remove all related tests. Verify that code appearing only in tests is not used through indirect mechanisms before removing it.

---

## Type Hints

Required on public functions and cross-module interfaces. Use `from __future__ import annotations` for forward refs. Prefer built-in generics (`list`, `dict`, `tuple`) and `X | None` over `Optional`.

---

## Docstrings

Concise reST-style for functions; short description for modules:

```python
def resolve_record(key: str, db_path: Path) -> Record:
    """
    Match a key to an internal record.

    :param key: lookup key from input file
    :param db_path: path to the project database
    :return: matched Record object
    """
```

---

## Dataclasses

Use `@dataclass(frozen=True)` for immutable result containers. Add dunder methods (`__len__`, `__iter__`, `__contains__`) when the class represents a collection.

---

## Comments

- Use comments sparingly and only where they improve readability.
- Prefer short logic-focused comments (why/intent), not line-by-line restatements (what).
- Add brief comments before non-obvious assumptions, coordinate conversions, and validation branches that could be misread.
- Remove or update outdated comments in the same change.

---

## Coding Standards

- Prefer explicit code over clever abstraction.
- Prefer simpler, linear implementations over complex branching or indirection when behaviour is the same.
- Do not generalize until the third use case.
- Prefer library-native functionality over custom helpers: check whether an equivalent function already exists in dependencies.
- Keep helpers close to their domain module unless reuse is clear and immediate.
