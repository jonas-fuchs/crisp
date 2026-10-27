---
name: CRISP general engineering
description: "Cross-project engineering guardrails; excludes the CRISP specialist workflow."
applyTo: "**"
---

# General Engineering Instructions

These are baseline engineering guardrails for normal Copilot agent mode. Language- and task-specific rules live in scoped instruction files (`python.instructions.md`, `scientific.instructions.md`, `tests.instructions.md`).

---

## Workflow Scope

This file does not activate or impose the CRISP Planner → Builder → Reviewer workflow. Do not create `TODO.md` feature tickets, require a planning approval gate or formal TDD cycle, or perform a specialist review handoff based on this file alone. Those requirements apply only when the corresponding CRISP custom agent is invoked, or when the user explicitly requests that workflow.

In normal agent mode, choose planning, tests, and validation proportionately to the change. Use TDD when the user requests it or when the change is substantive enough to benefit from it; trivial, low-risk edits may use a lighter validation check.

---

## Change Discipline

- Make the smallest coherent change.
- Separate behaviour changes from unrelated refactoring — one change does one thing.
- Keep changes small, local, and reviewable.
- Avoid unrelated refactors in the same change.

| Lines Changed | Assessment |
|---|---|
| ~100 | Good — reviewable in one pass |
| ~300 | Acceptable for a single logical change |
| ~1000 | Too large — split into smaller changes |

---

## Error Handling

- Do not silently swallow failures. Every `except` block must either re-raise, raise a domain-specific error, or log explicitly.
- Do not add silent or unverified fallbacks. Explicit, tested CPU/GPU, solver, backend, or precision fallbacks are valid.
- Prefer clean fail-fast behaviour over hidden compatibility logic.
- Do not add backward-compatibility layers unless explicitly requested.

---

## Command Discovery

Do not invent build, test, lint, or validation commands. Discover the canonical interface in this order:

1. `justfile` or `Makefile`
2. `pyproject.toml` task configuration
3. CI workflows (`.github/workflows/`)
4. Developer documentation
5. Package-manager metadata

When no canonical command exists, propose one before relying on ad hoc commands.

---

## Security Defaults

- Validate all external input at system boundaries.
- Keep secrets in environment variables — never in code or git.
- Treat data from external sources (uploads, APIs) as untrusted.
- Never expose stack traces or internal paths in error responses.

---

## Reporting

- Report commands run, evidence, assumptions, and unresolved risk.
- Make deterministic behaviour the default, especially in reporting and exports.

---

## Scientific Evidence

- Treat scientific validation separately from ordinary software tests.
- Do not derive expected test values from the implementation under test.
- See `scientific.instructions.md` for full numerical and reproducibility rules.
