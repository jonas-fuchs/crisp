---
name: CRISP general engineering
description: Cross-project engineering invariants for scientific Python work.
applyTo: "**"
---

# General Engineering Instructions

These invariants apply to all work in every project. Language- and task-specific rules live in scoped instruction files (`python.instructions.md`, `scientific.instructions.md`, `tests.instructions.md`).

---

## Workflow

CRISP follows a two-gate workflow: Plan → Build → Review.

```
Plan ──→ user "go" ──→ Build ──→ Scientific Review ──→ done | changes required
```

### Gates

1. **Planning gate**: The plan is presented and stops. The user reviews and says "go" before implementation starts. Bypass only when the user explicitly says "just do it" or the work is exploratory (algorithm tuning, prototyping).
2. **Review gate**: Never bypassed. All changes that will be merged must pass Scientific Review.

### Work Modes

- **Discovery**: question → hypothesis → experiment → evidence → decision. May begin with characterization, experiments, or reference construction. Not forced through TDD or ticket ceremony.
- **Delivery**: plan → build → scientific review → done. Requires a measurable acceptance condition and an independent validation approach before starting.

### TODO.md

`TODO.md` is the planning source of truth. Structure:

```
## Active
## Ready
## Next
## Blocked
```

Archive completed work into `docs/plans/`, GitHub issues, `CHANGELOG.md`, or `docs/archive/`. Git history preserves previous versions — do not accumulate completed items indefinitely.

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
