---
name: sprint-planning
description: 'Use when decomposing a feature request or complex task into sprint tickets for TODO.md. Covers clarification, decomposition, dependency mapping, prioritization, and sprint plan presentation.'
argument-hint: 'Feature request or task to decompose into tickets.'
user-invocable: true
disable-model-invocation: false
---

# Sprint Planning

## Overview

This skill guides the Planner through the planning ceremony: turning a user request into well-structured tickets in TODO.md, mapping dependencies, and presenting a sprint plan for user approval.

## When to Use

- A new feature request needs decomposition into implementable tickets.
- A complex task has multiple steps that should be tracked separately.
- The user wants to see a plan before authorizing implementation.

## When NOT to Use

- Trivial single-file changes that don't need a ticket.
- Read-only exploration or questions.
- The user explicitly says "just do it" with no planning.

## Planning Workflow

### Step 1: Clarify

If the request is underspecified, use the `grill-me` skill to ask the minimum questions needed to avoid rework:

- User goal and definition of done
- Scope boundaries and out-of-scope items
- Required inputs, outputs, and runtime constraints
- Validation expectations and acceptable trade-offs

Stop asking as soon as the blocking uncertainty is resolved. Do not ask about details already clear from the repo context.

### Step 2: Read Current State

- Read `TODO.md` if it exists — check Done and Next/backlog sections.
- Read `copilot-instructions.md` for project conventions and module boundaries.
- Identify affected modules and key dependencies.
- Check whether any related work is already in Done or in-progress.

### Step 3: Decompose into Tickets

Break the request into the smallest set of independently verifiable behaviour changes:

**Rules for good tickets:**
1. Each ticket is one observable behaviour change.
2. Each ticket is implementable from a single sentence.
3. Each ticket has a clear acceptance signal (test passes, command works, output correct).
4. Each ticket touches a coherent set of files — not scattered across unrelated modules.
5. A ticket should be completable in one implementation pass.

**Decomposition approach:**
- Start with the user's goal and work backwards to the smallest first step.
- Identify dependencies — what must exist before what.
- Separate cross-cutting concerns (tests, docs, config) into their own tickets only if they are substantial enough to warrant separate review.
- If a ticket is larger than ~300 lines of change, split it further.

### Step 4: Check for Duplicates

Before writing any tickets:
1. Search **Done** section for matching keywords or module names. Skip anything already completed.
2. Search **Next/backlog** section for exact or near-duplicate items. Propose an update rather than a duplicate.
3. If a close match is found in Done, verify by reading the relevant source files.
4. If the Done entry exists but source code evidence is missing, flag the discrepancy.

### Step 5: Assign Priority and Sprint Status

Map each ticket to a lifecycle stage and priority:

| Marker | Stage | Meaning |
|---|---|---|
| `- [ ] 🔵` | Backlog | Triaged but not prioritized for this sprint |
| `- [ ] 🟠` | Sprint | Prioritized for the current sprint; ready to pick up |
| `- [ ] 🟡` | In-Progress | Being implemented right now |
| `- [ ] 🔍` | Review | Implementation complete, awaiting review |
| `- [x]` | Done | Reviewed and approved |

Priority within sprint:
- **🔴 high** — blockers or foundational work; tackle first
- **🟡 medium** — important but not urgent
- **🟢 low** — nice-to-have or dependent on higher-priority work

New tickets from this planning session are typically `🟠` (sprint) or `🔵` (backlog).

### Step 6: Map Dependencies

Identify the execution order:
- Which tickets block others?
- Which tickets are independent?
- Which tickets can run in parallel?

Present as a simple ordered list or a Mermaid diagram for complex dependency graphs.

### Step 7: Write Tickets to TODO.md

Use the `ticket-workflow` skill to write tickets. Present a **preview block** showing exactly how entries will appear before writing:

```
### [Theme Name]

- 🟠 🔴 [ticket 1: affected module + observable behaviour change]
- 🟠 🟡 [ticket 2: affected module + observable behaviour change]
- 🔵 🟢 [ticket 3: affected module + observable behaviour change]
```

### Step 8: Present Sprint Plan

Present the plan to the user in this format:

```
## Sprint Plan: [feature/task name]

### Context
[1-2 sentences on what we're building and why]

### Tickets Created
- 🟠 [ticket 1]
- 🟠 [ticket 2]
- 🔵 [ticket 3]

### Execution Order
1. [ticket 1] — foundational, blocks [ticket 2]
2. [ticket 2] — depends on [ticket 1]
3. [ticket 3] — independent, can be done anytime

### Risks & Assumptions
- [risk 1 and mitigation]
- [assumption 1]
- [open question for user, if any]

---
Say "go" to start execution. The Builder will pick up the first ticket.
```

### Step 9: STOP

Do not delegate. Do not implement. Wait for the user's "go".

This is the **planning gate**. It is never skipped.

## Ticket Writing Rules

### Single Sentence

Each ticket is a single sentence: `affected module(s) + observable behaviour change`.

Good:
- `Add input validation for edge-case values in src/core/processor.py so empty inputs are rejected with a clear error.`
- `Add POST /api/jobs endpoint to the web backend so the frontend can submit background jobs.`
- `Add migration to db/schema.py to add status column to the results table.`

Bad (multi-sentence):
- `Add input validation. This should check the ref value and validate the alt. Also update the tests.`

### Theme Grouping

Group related tickets under a theme heading:

```
### Processing Improvements

- 🟠 🔴 Add boundary-value handling to src/core/processor.py for edge-case inputs.
- 🟠 🟡 Add structured error output to src/core/processor.py for invalid records.
- 🔵 🟢 Add test coverage for edge-case input handling in src/core/processor.py.
```

### Acceptance Criteria

For each ticket, include a brief acceptance signal — what proves the ticket is done:

- `Acceptance: test_edge_case_input passes and python -m pytest tests clean.`
- `Acceptance: curl POST /api/jobs returns 201 with job_id.`
- `Acceptance: migration applies cleanly on existing database and new column has correct defaults.`

Keep acceptance criteria inline with the ticket where space allows, or in a follow-up line.

## Anti-Patterns

- **Planning and implementing in one step** — always stop at the gate.
- **Tickets that are too large** — if it needs more than ~300 lines, split it.
- **Tickets that mix concerns** — refactoring + feature + tests in one ticket is three tickets.
- **Vague tickets** — "improve the processing" is not a ticket. "Add boundary-value handling for edge-case inputs in processor.py" is.
- **No dependency mapping** — if ticket 2 depends on ticket 1, say so explicitly.
- **Skipping duplicate check** — always check Done and Next before creating new tickets.
