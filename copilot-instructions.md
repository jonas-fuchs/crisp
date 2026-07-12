# General Coding Instructions

These guidelines apply to all work in every project. They are always loaded.
Skills and agents reference this file instead of restating these rules.

---

## Scrum Workflow

Work follows a lightweight scrum lifecycle driven by `TODO.md` as the ticket system.

```
User request ──→ Planner ──→ Tickets in TODO.md (backlog)
                                     │
                          User "go"  │
                                     ▼
                             Builder ──→ Reviewer
                            (TDD, validates)  (5-axis gate)
                                     │                     │
                                     │              APPROVE │ REQUEST CHANGES
                                     │                     │
                                     ▼                     ▼
                              ticket: review ──→ ticket: done | back to in-progress
```

### Ticket Lifecycle Stages

| Stage | Marker in TODO.md | Meaning |
|---|---|---|
| Backlog | `- [ ] 🔵` | Triaged but not yet prioritized for a sprint |
| Sprint | `- [ ] 🟠` | Prioritized for the current sprint; ready to pick up |
| In-Progress | `- [ ] 🟡` | Being implemented right now by the Builder |
| Review | `- [ ] 🔍` | Implementation complete, awaiting Reviewer verdict |
| Done | `- [x]` | Reviewed and approved; moved to Done section |

### The Two Checkpoints

1. **Planning gate**: Planner creates tickets and stops. The user reviews and says "go" before any implementation starts.
2. **Review gate**: Reviewer verifies implementation. APPROVE → done. REQUEST CHANGES → back to Builder with specific findings.

### Fast Path

The planning gate can be bypassed in two cases:

- The user explicitly says "just do it" or invokes the **Builder** directly for a well-scoped task.
- The work is exploratory — trying algorithms, tuning parameters, or prototyping where the outcome is unknown. Use Builder directly, then review the result before committing.

The review gate is never bypassed. All changes that will be merged must pass Reviewer.

### Agent Roles

- **Planner**: Clarifies the request, decomposes into tickets, writes TODO.md, waits for user "go", then delegates to Builder. Does not write code.
- **Builder**: Takes one ticket, implements using TDD (`testing` skill), debugs with `diagnose` skill, escalates to specialist subagents when needed. Hands off to Reviewer when done.
- **Reviewer**: 5-axis review (`code-review-and-quality` skill). Read-only. Gate for merge. Can delegate to audit skills and Security.
- **Researcher**: scientific literature research and bioinformatics pre-implementation reviews. User-invocable (shown in agent picker) and delegatable by Planner or Builder.

Specialist subagents (Security, Web, CI/CD, Docs) are accessible by delegation only — not shown in the agent picker.

---

## Project Guardrails

- No functions in `__init__.py`: package init files must only contain a module docstring.
  Place functions in named submodules (e.g. `pkg/utils/files.py`) and import from there.
- If any feature is removed from the codebase, remove all related tests.
- If a feature is only loaded by tests remove it from the codebase.
- Never write imports into functions or classes. Always import from the top level.
- Prefer top-down module function layout (excluding the main entrypoint), ordered by call flow:
  1. Top function (orchestrates A, B, C)
  2. Subfunctions near their caller (A before B when called in that order)
  3. Helpers immediately below their owning subfunction (A.1, A.2, then B.1, B.2)
  4. Shared helpers at the bottom of the module
- Keep this layout logical and readable rather than strictly mechanical; proximity should make call flow easy to follow.
- Very small one-purpose helpers may be nested inside a larger function when they are local to that function.
- Nested tiny helpers should stay simple, contain no complex logic, and are tested through the parent function rather than separately.

---

## Code Conventions

| Element | Convention |
|---|---|
| Functions/variables | `snake_case` |
| Classes | `PascalCase` |
| Constants | `UPPER_SNAKE_CASE` (only when reused, versioned, or holds large text/regex/lookup tables) |
| Internal helpers | prefix with `_` |
| Strings | single quotes (`'...'`) |
| Docstrings | triple double quotes (`"""..."""`) |
| Line length | 100 |

### Imports

Group by: built-in, installed/third-party, local package — separated by blank lines. Always top-level, never inside functions or classes.

```python
import os
from pathlib import Path

import numpy as np

from mypackage import config
from mypackage.core.processor import process_data
```

### Docstrings

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

### Type Hints

Required on public functions and cross-module interfaces. Use `from __future__ import annotations` for forward refs. Prefer built-in generics (`list`, `dict`, `tuple`) and `X | None` over `Optional`.

### Dataclasses

Use `@dataclass(frozen=True)` for immutable result containers. Add dunder methods (`__len__`, `__iter__`, `__contains__`) when the class represents a collection.

---

## General Coding Principles

### Correctness First

- Understand the requirement before writing code.
- Handle edge cases: empty inputs, boundary values, null/None, ambiguous states.
- Handle error paths explicitly — no silent `except` blocks that swallow failures.
- Every bug fix starts with a failing test that reproduces the bug.

### Simplicity and Readability

- Names are descriptive and consistent with existing conventions.
- Control flow is straightforward — no deeply nested branches, no clever one-liners.
- More lines than needed is a problem, not thoroughness.
- Do not generalize until the third use case.
- Intent comments only for non-obvious logic — do not comment obvious code.
- No dead code: unused variables, backward-compat shims, stale imports, commented-out blocks.

### Coding Standards

- Prefer explicit code over clever abstraction.
- Prefer simpler, linear implementations over complex branching or indirection when behavior is the same.
- Do not add fallback code paths for missing data — require the data to be present and fail fast if it is not. Compatibility shims and graceful degradation add hidden complexity and mask bugs during build-out.
- Do not use silent exception handlers. Every `except` block must either re-raise, raise a domain-specific error, or log the failure explicitly.
- Keep changes small, local, and reviewable.
- Avoid unrelated refactors in the same change.
- Preserve existing public APIs unless the task clearly requires a change.
- Prefer library-native functionality over custom helpers: before adding a new helper/utility function, check whether an equivalent function already exists in dependencies we already rely on.
- During active build-out, do not enforce backward compatibility unless explicitly requested by the user.
- Keep helpers close to their domain module unless reuse is clear and immediate.
- Make deterministic behavior the default, especially in reporting and exports.

### Backward Compatibility

- Do not add backward-compatibility layers unless explicitly requested by the user.
- Avoid proactive migration helpers, legacy fallbacks, alias parsers, or dual-schema code paths when the project is still in active build-out.
- Prefer a clean fail-fast behavior over hidden compatibility logic.
- If backward compatibility is requested later, implement it as a clearly scoped, isolated change.

### Comments

- Use comments sparingly and only where they improve readability.
- Prefer short logic-focused comments (why/intent), not line-by-line restatements (what).
- Add brief comments before non-obvious assumptions, coordinate conversions, and validation branches that could be misread.
- Keep comments concise (one to two lines when possible) and colocated with the code block.
- Remove or update outdated comments in the same change; comments must stay accurate.

---

## Module Boundaries

Keep module responsibilities clean and one-directional:

- **Input/parsing layer**: parse external formats, validate structure. No domain logic.
- **Core/domain layer**: business logic, algorithms, interpretation. No I/O concerns.
- **Persistence layer**: database queries, storage. No domain logic.
- **Reporting layer**: rendering, export, formatting. No domain logic.
- **CLI layer**: thin handlers that wire user input to core. No domain logic.
- **Web layer**: transport, validation at boundaries. Reuse core logic, do not reimplement.

No functions in `__init__.py` — only module docstrings.
No imports inside functions or classes — always top-level.
No circular imports between layers.

### Architecture

- New dependencies flow in the right direction: outer layers depend on inner, never reverse.
- If code is duplicated across layers, extract shared logic into the appropriate module.
- Separate refactoring from feature work — one change does one thing.

### Change Sizing

| Lines Changed | Assessment |
|---|---|
| ~100 | Good — reviewable in one pass |
| ~300 | Acceptable for a single logical change |
| ~1000 | Too large — split into smaller changes |

---

## Editing Guidance

- Align implementation with `TODO.md` priorities unless direct user instructions say otherwise.
- When changing repository layout or module responsibilities, update the contributing/architecture docs in the same change.
- For architecture-relevant changes, use `graphify` selectively for drift checks; do not run it on routine local edits.
- When behavior changes can make documentation inaccurate, update affected docs in the same change.
- In Markdown docs, do not introduce artificial manual line breaks in normal paragraphs. Keep prose as natural paragraphs and only break lines where structure requires it.
- Put format-specific parsing in the input layer, domain interpretation in the core layer, persistence concerns in the persistence layer, and rendering/export concerns in the reporting layer.
- Keep CLI handlers thin: orchestration belongs in the CLI layer, while reusable logic belongs in package modules.

---

## Testing

- Run the test suite with: `python -m pytest`
- TDD cycle: RED (write failing test) → GREEN (minimal code to pass) → REFACTOR (clean up, tests still pass)
- Bug fixes: write a test that reproduces the bug before attempting a fix.
- Test behaviour, not implementation details.
- One concept per test.
- Prefer real implementations over mocks. Mock only at external service boundaries.
- No tests skipped or disabled to make the suite pass.
- For full testing rules, TDD cycle, fixtures, focus areas, and anti-patterns, use the `testing` skill.
- For unclear failures and regressions, use the `diagnose` skill before implementing a fix.

---

## Security Defaults

- Validate all external input at system boundaries.
- Parameterise all SQL queries — never concatenate user input.
- Keep secrets in environment variables — never in code or git.
- Treat data from external sources (uploads, APIs) as untrusted.
- Never expose stack traces or internal paths in error responses.
- Enforce auth consistently on protected endpoints.
- For detailed security guidance, use the `security-and-hardening` skill.

---

## Build and Test Commands

```bash
# Install dependencies (adapt to project)
pip install -e .

# Run full test suite
python -m pytest

# Run tests for a specific module
python -m pytest tests/test_<module>.py -q

# Type checking (if configured)
python -m mypy src/

# Linting (if configured)
python -m ruff check src/

# CPU profiling
python -m cProfile -s cumulative -o profile.out myscript.py

# Memory profiling
python -m memory_profiler myscript.py
```

---

## Planning Source of Truth

`TODO.md` is the planning source of truth. Always read it before any substantial change.

- **Done** section: completed work, marked `[x]`. Never remove — serves as project history.
- **Next / Backlog** section: open work with priority markers.
- Update TODO.md in the same change as the implementation.
- For detailed workflow, see the `ticket-workflow` skill.

---

## Agents & Skills

### Core Agents (user-invocable)

| Agent | Use for | Key skills |
|---|---|---|
| **Planner** | Planning and delegation for multi-step work | `grill-me`, `sprint-planning`, `ticket-workflow` |
| **Builder** | Default executor for coding changes | `testing`, `diagnose` |
| **Reviewer** | Quality review — read-only merge gate | `code-review-and-quality`, `review-cleanup-playbook` |
| **Researcher** | Scientific literature and bioinformatics pre-implementation reviews | — |

### Specialist Agents (delegation only)

| Agent | Delegate for | Key skill |
|---|---|---|
| **Security** | Audits and hardening (uploads, auth, SQL, CORS, rate limits) | `security-and-hardening` |
| **Web** | Coordinated backend/frontend work | `security-and-hardening`, `testing` |
| **Docs** | Public docs quality and drift correction | `public-documentation` |
| **CI/CD** | Workflow and CI/CD hardening | — |

### Built-in Subagents

| Subagent | Use for |
|---|---|
| **Explore** | Fast read-only codebase navigation and Q&A |

### Workflow Skills

- `grill-me` — targeted clarification before code changes.
- `sprint-planning` — decomposing requests into sprint tickets.
- `ticket-workflow` — TODO.md ticket lifecycle.
- `testing` — red-green-refactor loop for implementation or bug fixes.
- `diagnose` — disciplined bug reproduction and narrowing.
- `graphify` — subsystem boundaries or architecture decisions.
- `improve-codebase-architecture` — shallow modules or cross-layer coupling.

---

## Code Review Guidelines

Full code review is handled by the **Reviewer** agent and its skills (`code-review-and-quality`, `dead-code-and-test-only-audit`, `complexity-and-compartmentalization-audit`, `improve-codebase-architecture`, `review-cleanup-playbook`).

When reviewing code, always check for:

- Coding conventions from this file (Code Conventions section)
- Logical consistency and correctness, especially in edge cases
- Proper error handling and informative error messages
- Proper use of type hints and docstrings
- Proper test coverage and quality of test cases
- Backward-compatibility code that was not explicitly requested — remove it
- Follow SOLID, KISS and DRY principles

---

## graphify

For any question about a codebase's architecture, structure, components, or how to add/modify/find code, your first action should be `graphify query "<question>"` when `graphify-out/graph.json` exists. Use `graphify path "<A>" "<B>"` for relationship questions and `graphify explain "<concept>"` for focused-concept questions. These return a scoped subgraph, usually much smaller than the full report or raw grep output.

Triggers: "how do I…", "where is…", "what does … do", "add/modify a <component>", "explain the architecture", or anything that depends on how files or classes relate.

If `graphify-out/wiki/index.md` exists, use it for broad navigation. Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context. Only read source files when (a) modifying/debugging specific code, (b) the graph lacks the needed detail, or (c) the graph is missing or stale.

Type `/graphify` in Copilot Chat to build or update the graph.
