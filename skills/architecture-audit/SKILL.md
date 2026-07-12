---
name: architecture-audit
description: 'Audit a repository for architectural friction: shallow modules, weak seams, tightly coupled flows, overly complex functions, long scripts, deeply nested logic, and missing intent comments. Use when reviewing architecture, testability, and long-term maintainability.'
argument-hint: 'Scope to analyze, known pain points, and whether to deliver candidates only or a prioritized recommendation.'
user-invocable: true
disable-model-invocation: false
---

# Architecture Audit

## Overview

Use this skill to surface architectural friction and propose deepening opportunities. The target is not style cleanup. The target is higher leverage interfaces, better locality of change, and safer future edits. Also covers complexity and compartmentalization: overly complex functions, long scripts, deeply nested logic, weak module boundaries, and tiny single-use helpers that should be inlined or absorbed.

## Vocabulary

- Module: any unit with an interface and an implementation (function, class, package, feature slice)
- Interface: what callers must know to use a module (types, invariants, error modes, ordering, config)
- Implementation: what is hidden behind the interface
- Depth: how much useful behaviour is hidden behind a small interface
- Seam: a place where behaviour can change without editing callers in place
- Locality: related change concentrated in one place
- Leverage: value callers get from depth

## When to Use

- The codebase is becoming harder to change safely
- A feature requires touching too many modules
- Tests are hard to write because the current interface exposes too much wiring
- There is repeated logic across layers
- A review surfaces coupling, shallow pass-through modules, or unclear seams
- Find functions that are too long or too nested
- Identify scripts or modules that should be split into clearer units
- Flag missing intent comments around non-obvious logic
- Find tiny one-off helpers that add indirection without reuse

When NOT to use:

- Small local bug fixes that do not cross module boundaries
- Cosmetic refactors without structural payoff
- Code is already clear and consistent
- You do not yet understand the code path (understand first, then simplify)
- Suggested simplification would change behaviour or weaken error handling

## Core Principles

1. Preserve behaviour exactly.
2. Follow repository conventions and existing patterns.
3. Prefer clarity over cleverness.
4. Scope recommendations to changed or high-risk areas unless asked to broaden.

### Preserve Behavior Exactly

For each recommendation, verify that it preserves:

- Inputs and outputs
- Error behaviour and edge handling
- Side effects and execution ordering

### Understand Before Touching (Chesterton's Fence)

Before recommending removal or inlining:

- Identify what the code is responsible for.
- Identify callers and downstream dependencies.
- Check likely reasons the structure exists (testability, extensibility, performance, historical constraints).
- Avoid removing structure you cannot explain yet.

## Procedure

### Part A: Architectural Friction

1. Explore and map friction:
   - Follow a real user flow (CLI or web) and note where understanding requires excessive hopping.
   - Identify shallow modules by applying the deletion test: if deleting the module just spreads complexity to callers, it had value; if not, it may be pass-through noise.
2. Build architecture candidates:
   - Candidate title
   - Files involved
   - Problem (current friction)
   - Proposed seam/deepening move
   - Expected benefits in locality, leverage, and testability
   - Recommendation strength: `Strong`, `Worth exploring`, or `Speculative`
3. Prioritize:
   - Pick one top candidate with the best risk-to-value ratio.
   - State the minimum safe first step.

### Part B: Complexity and Compartmentalization

1. Identify simplification opportunities:
   - deep nesting (3+ levels)
   - long functions with mixed responsibilities
   - long procedural modules/scripts
   - repeated conditionals across call sites
   - boolean flag parameters that hide intent
   - nested ternaries or dense one-liners
   - helper functions used once with little naming value
   - unclear or misleading names
   - missing intent comments in non-obvious logic
2. Classify each issue as one of:
   - control-flow complexity
   - compartmentalization boundary issue
   - naming/readability issue
   - unnecessary indirection
   - documentation/intent gap
3. Recommend incremental refactors, not broad rewrites:
   - one focused change at a time
   - separate simplification from feature work
   - prefer local, reviewable changes
4. Verify suggested outcomes:
   - behaviour preserved
   - readability improved
   - boundaries clarified
   - no error handling removed

## Constraints

- Preserve behaviour unless behaviour change is explicitly requested.
- Prefer incremental deepening over broad rewrites.
- Do not introduce abstraction that exceeds real current need.
- Do not suggest refactors without naming the exact pain point.
- Do not recommend decomposition that adds more abstraction than it removes.
- Keep recommendations local and pragmatic.
- Do not optimize for line count alone.
- If architecture boundaries change, update the relevant development docs in the same change.

## Output Format

Return findings first, ordered by severity and impact.

For each finding include:

- What is too complex or architecturally weak.
- Why the current structure is costly or risky.
- Whether the issue is long-file, long-function, nesting, indirection, shallow-module, or missing-comment related.
- Recommended refactor boundary.
- Minimum safe simplification step.
- Expected benefit (locality, leverage, testability).

Then include:

- "Do first" list (highest ROI, lowest risk)
- Top recommendation and why
- Risks or unknowns to validate before implementation
- Optional follow-ups if scope expands
