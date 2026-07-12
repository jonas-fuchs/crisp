---
name: software-quality-audit
description: 'Conducts multi-axis code review covering correctness, readability, architecture, security, performance, dead code, complexity, and cleanup. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when assessing code quality before it enters the main branch.'
argument-hint: 'Scope (file, module, or full repo), review focus, and change description.'
user-invocable: true
disable-model-invocation: false
---

# Software Quality Audit

## Overview

Multi-dimensional code review with quality gates. Every change gets reviewed before merge. This skill consolidates correctness, readability, architecture, security, performance, dead code, complexity, and cleanup into a single review procedure.

Approval standard: approve a change when it definitely improves overall code health, even if it is not perfect. Do not block a change because it is not exactly how you would have written it. If it improves the codebase and follows project conventions, approve it.

Do not approve a change that has any Critical issue. If uncertain about a potential issue, say so and recommend the narrowest investigation that would resolve the uncertainty rather than guessing.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code that needs evaluation
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

---

## The Six-Axis Review

### 1. Correctness

Does the code do what it claims to do?

- Does it match the spec or task requirements?
- Are edge cases handled (empty, boundary, ambiguous states, None)?
- Are error paths handled, not just the happy path?
- Are exceptions handled explicitly (no silent `except` blocks that swallow failures)?
- Are there off-by-one errors in coordinate logic or index walks?
- Do tests actually test the right behaviour?
- Is data transformation, filtering, and rule matching consistent with the documented algorithm?

### 2. Readability and Simplicity

Can another engineer understand this code without the author explaining it?

- Are names descriptive and consistent with project conventions?
- Is control flow straightforward — no deeply nested branches, no clever one-liners?
- Could this be done more simply? More lines than needed is a problem, not a sign of thoroughness.
- Do abstractions earn their complexity? Do not generalize until the third use case.
- Are intent comments present where the logic is non-obvious?
- No dead code artifacts: unused variables, backwards-compat shims, stale imports, commented-out blocks.

### 3. Architecture

Does the change fit the system's design?

- Does it respect module boundaries from project instructions?
- Are new dependencies flowing in the right direction (no circular imports)?
- Is there code duplication that should be shared?
- Are functions too long or too nested? (flag deep nesting 3+ levels, long functions with mixed responsibilities)
- Are there tiny one-off helpers that add indirection without reuse?

For deeper architecture analysis, use the `architecture-audit` skill.

### 4. Security

Does the change introduce vulnerabilities?

- Is user input validated and sanitised at system boundaries?
- Are secrets kept out of code, logs, and version control?
- Are file path confinement rules respected?
- Are SQL queries parameterised — no string concatenation in DB calls?
- Is auth enforcement applied consistently on protected endpoints?
- Is data from external sources (user uploads, external APIs) treated as untrusted?

For detailed security review, use the `security-review` skill.

### 5. Performance

Does the change introduce performance problems?

- Any N+1 query patterns against the database?
- Any unbounded loops over data without early exit?
- Any large objects created in hot paths?
- Any Python-level loops that should be vectorised with NumPy?
- Any large intermediate arrays or unnecessary copies in memory-sensitive paths?
- If the change affects a hot path, were profiling results provided (before/after)?

For measured optimisation, use the `profiling` skill.

### 6. Cleanup

Is the code harder to maintain than necessary?

Check for cleanup opportunities in changed lines and immediately adjacent code:

- **Dead code**: unused helpers, stale branches, commented-out code, compatibility shims, unused imports, write-only variables.
- **Comment problems**: stale comments, comments that restate the code, missing intent comments around non-obvious logic.
- **Function shape**: functions doing more than one job, long selector chains, flag arguments, too many parameters.
- **Naming**: vague names, misleading names, names that hide side effects.
- **DRY**: duplicated conditionals, repeated parsing or normalization logic, repeated non-obvious literals.
- **Obscured intent**: dense branching, magic values, hidden coupling, train-wreck access chains.

Use rule tags when reporting cleanup findings:

- `C1-C5`: comments hygiene
- `F1-F4`: function hygiene
- `G5`: DRY; `G9`: remove dead code; `G16`: avoid obscured intent; `G25`: replace magic numbers; `G30`: functions do one thing; `G36`: avoid train-wreck chains
- `N1-N7`: naming clarity and side-effect honesty
- `P3`: type hints on public interfaces

---

## Review Process

### Step 1: Understand the Context

Before looking at code, understand the intent:

- What is this change trying to accomplish?
- Which module(s) are affected?
- What is the expected observable behaviour change?

### Step 2: Review the Tests First

Tests reveal intent and coverage:

- Do tests exist for the change?
- Do they test behaviour, not implementation details?
- Are edge cases covered?
- Would the tests catch a regression if the code changed?

### Step 3: Review the Implementation

Walk through the code with the six axes in mind. For each file changed, check correctness, readability, architecture, security, performance, and cleanup.

### Step 4: Dead Code Hygiene

After any refactoring or implementation change, check for orphaned code:

1. Search for candidate symbols, helpers, and modules that look unused or stale.
2. Verify usages across production code and tests separately.
3. Distinguish: truly unused code, code used only by tests, code used indirectly through CLI/framework/reflection/serialization.
4. Flag only findings that have evidence. Do not call code dead without checking runtime entry points.

### Step 5: Categorize Findings

| Label | Meaning |
|---|---|
| **Critical:** | Blocks merge — security vulnerability, data loss, broken functionality |
| *(no prefix)* | Required change — must address before merge |
| **Nit:** | Minor, optional — author may ignore |
| **Optional:** / **Consider:** | Suggestion — worth considering but not required |
| **FYI** | Informational only — no action needed |

Every Critical and Required finding should include a specific fix recommendation.

### Step 6: Verify the Verification

- Are tests run and passing?
- Is expected behaviour verified?
- For report changes: is output deterministic?
- For scientific code: is validation independent?

---

## Change Sizing

| Lines Changed | Assessment |
|---|---|
| ~100 | Good — reviewable in one pass |
| ~300 | Acceptable for a single logical change |
| ~1000 | Too large — split into smaller changes |

One change = one self-contained modification that addresses one thing, includes related tests, and leaves the system functional. Separate refactoring from feature work.

---

## Review Output Template

```
## Review Summary

**Verdict:** APPROVE | REQUEST CHANGES

**Overview:** [1-2 sentences summarizing the change and overall assessment]

### Critical Issues
- [file reference] [description and recommended fix]

### Required Changes
- [file reference] [description and recommended fix]

### Cleanup Findings
- [rule tag] [file reference] [description and minimal fix]

### Suggestions
- [file reference] [optional improvement]

### What's Done Well
- [specific positive observation]

### Verification Story
- Tests reviewed: [yes/no, observations]
- Build or focused validation checked: [yes/no, observations]
- Security checked: [yes/no, observations]
```

---

## Reviewer Rules

1. Review the tests first — they reveal intent and coverage.
2. Read the task, spec, or user request before reviewing implementation details.
3. Every Critical and Required finding must include a concrete fix recommendation.
4. Include at least one specific positive observation when the change does something well.
5. Do not guess. If evidence is incomplete, say what remains uncertain and what should be checked next.
6. Prefer fewer, high-signal findings over long low-value lists.
