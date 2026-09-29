---
name: project-planning
description: 'Procedure for writing a researched implementation plan for a NEW project: research-first rules, spike discipline, and the feature format for ProjectPlan.md. Use when shaping a greenfield project idea into a plan with distinct, independently testable features.'
argument-hint: 'The project idea and what has already been settled in discussion with the user.'
user-invocable: true
disable-model-invocation: false
---

# Project Planning

## Overview

The Stage 2 procedure for the **Project Planner agent**: turn a discussed and settled project idea into `project-planning/ProjectPlan.md`. This skill covers research-first rules, spike discipline, and the feature format. It does not cover feature discussion (Stage 1) or repository initialization (Stage 3) — those live in the agent.

For existing projects, this skill does not apply: use the `grill-me` and `delivery-planning` skills with the Planner agent instead.

## When to Use

- A greenfield project idea has been discussed and the user said "go for the implementation plan".
- A `ProjectPlan.md` needs to be written or revised from research findings.

When NOT to use: the project already exists; the task is a feature inside an existing codebase (`delivery-planning`); the user has not approved moving to the plan yet (keep discussing).

## Rules

### Research first, always

- Every non-obvious claim in the plan must rest on research, not recall. Delegate to the **Researcher** subagent for anything outside standard software engineering knowledge.
- Minimum research set before writing the plan:
  1. **Similar repositories** — what exists, what is solved, what to reuse, what to avoid. Note license, maintenance status, and scope for each.
  2. **Dependency and library candidates** — for each candidate: maintenance, license, dependency weight, scope fit, and why it benefits this repo.
  3. **Technology decisions with real uncertainty** — APIs, data formats, protocols, algorithms.
- Record longer research notes in `project-planning/research/*.md` (one file per topic). The plan references them; the notes survive Stage 3 cleanup.
- If research does not support a clear decision, do not pick silently. State the options in *Considerations before starting to work on the MVP* and move on.

### Spike discipline

Throwaway test code is allowed only under these rules:

- All spike code lives in `spikes/` at the project root. Nothing outside it.
- Every spike maps to a named open question or risk in the plan. If it answers nothing, do not write it.
- Spikes are never committed, never copied into the final structure, never kept as starting points.
- Record the conclusion (works / does not work, with evidence) in the plan before cleanup. Stage 3 deletes `spikes/` wholesale.

### Feature format

The plan decomposes the project into features — the high-level units the Planner agent later digests into tickets. Each feature must have:

- A short title and a description of what it delivers.
- **Builds on:** which features must exist first (state explicitly, even if none).
- **Acceptance:** one measurable criterion ("returns X for input Y", not "works correctly").
- **Risks:** feature-specific open risks or unknowns; `none` is acceptable.

Features are independently testable implementation steps. If a feature cannot be tested on its own, split it or fold it into the feature it belongs to.

## Procedure

1. **Create the planning folder** `project-planning/` at the project root with `ProjectPlan.md`, `TODO.md` (empty skeleton), and — for scientific projects — `SCIENTIFIC_CONTRACT.md`.
2. **Run the research set** (above) via the Researcher subagent; write notes to `project-planning/research/`.
3. **Write `ProjectPlan.md`** from `templates/PROJECT_PLAN.md`. Sections may be `none` if not applicable — say `none`, do not delete the section.
4. **Run spikes** only for questions that block a plan decision; record conclusions in the plan.
5. **Present the plan and stop.** Iterate on user feedback within Stage 2. Do not advance to repository initialization.

## Output Format

`ProjectPlan.md` follows `templates/PROJECT_PLAN.md` exactly:

- `## Similar repositories` — one `###` subsection per repo, short description plus license and what to take from it.
- `## Useful technologies to consider while implementing` — bullets for libraries, languages, APIs; each with *why this benefits the repo*.
- `## Minimal viable product` — the minimal feature set that reaches the goal.
- `## Additional consideration` — useful but non-MVP ideas and add-ons.
- `## Considerations before starting to work on the MVP` — everything unclear between planning and implementation: API key checks, pending research, unresolved decisions.
- `## Implementation plan` — `### Feature N` subsections in the feature format above.
- `## Open risks and validation needed` — risks and validation to run after the MVP exists.
