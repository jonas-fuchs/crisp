---
name: delivery-planning
description: 'Decompose a feature request into sprint tickets and manage the TODO.md ticket lifecycle. Use when planning a new feature, starting sprint work, or keeping the planning file accurate. For underspecified tasks, run grill-me first.'
argument-hint: 'Feature request, task description, or planning question. Include whether this is Discovery or Delivery mode.'
user-invocable: true
disable-model-invocation: false
---

# Delivery Planning

## Overview

This skill covers decomposition of one feature into related tickets and TODO.md lifecycle management. It is the backing procedure for the **Planner agent** and defines the mandatory lifecycle when the CRISP custom agents are used. For underspecified tasks, run `grill-me` first to resolve blocking ambiguity, then use this skill to decompose and plan.

## When to Use

- Planning a new feature or complex change
- Starting sprint work
- Decomposing a request into tickets
- Managing the TODO.md file

When NOT to use: the task is underspecified — run `grill-me` first to get alignment, then come here.

---

## Work Modes

### Discovery Mode

Use when the goal is exploration, prototyping, or trying algorithms where the outcome is unknown.

- Skip detailed planning and go directly to the Builder.
- Open a TODO.md entry but do not decompose into formal tickets.
- Review results before committing or scaling.

### Delivery Mode

Use when the goal is a production deliverable with clear requirements.

- Run the full planning workflow: clarify → decompose feature → prioritize → build every related ticket → review feature.
- Write formal, related tickets in TODO.md using the same unique `Feature: <name>` tag.
- Enforce both gates: planning gate (user approves plan) and review gate (Reviewer approves the complete feature).

---

## TODO.md Structure

The planning file is the single source of truth for work status. It has six sections:

```markdown
# TODO

## Active
- [ ] 🟡 Ticket title — short description, affected modules; Feature: Unique feature name

## Ready
- [ ] 🟠 Ticket title — short description, affected modules; Feature: Unique feature name

## Next
- [ ] 🔵 Ticket title — short description, affected modules

## Blocked
- [ ] ⛔ Ticket title — description and what it's blocked on

## Review
- [ ] 🔍 Ticket title — implementation complete, awaiting feature-level Scientific Reviewer verdict; Feature: Unique feature name

## Done
- [x] ✅ Ticket title — completed date (month/year)
```

### Section Semantics

| Section | Marker | Meaning |
|---|---|---|
| Active | 🟡 | Being worked on right now |
| Ready | 🟠 | Prioritized, ready to pick up |
| Next | 🔵 | Triaged, not yet prioritized |
| Blocked | ⛔ | Cannot proceed — waiting on a dependency |
| Done | ✅ | Completed and reviewed |

### Archival

When the Done section grows beyond ~20 items, move the oldest entries to an archive file (`TODO-archive.md`). This keeps the active planning file scannable while preserving project history.

---

## Ticket Lifecycle

```
Next ──→ Ready ──→ Active ──→ Review ──→ Done
 🔵       🟠       🟡         🔍        ✅
            │
            ▼
          CHANGES REQUIRED → Active

The Builder transitions every ticket sharing a feature tag together only after the complete feature is implemented. The Reviewer approves or rejects that complete feature ticket set together.
```

### Ticket Writing

Each ticket is a single `- [ ]` line in TODO.md. Format:

```
- [ ] [marker] Title — one-line description; affected modules in parentheses; Feature: Unique feature name
```

For the Ready section, add acceptance criteria below the ticket line:

```
- [ ] 🟠 Implement spectral normalization — add normalization step to `spectra.py` (core); Feature: Spectral processing
  - [ ] Acceptance: normalized output preserves area under curve
  - [ ] Acceptance: handles edge case of all-zero input
  - [ ] Acceptance: unit test with analytical case passes
```

### Ticket Rules

- One ticket = one self-contained change within exactly one feature.
- Each ticket has clear acceptance criteria, and every ticket for a feature uses an identical, unique `Feature: <name>` tag.
- The Builder completes every related ticket using TDD before initiating review. On APPROVE, the Scientific Reviewer alone moves the exact reviewed feature ticket set from Review to Done.
- If a feature is removed from the codebase, remove its tickets.
- Update TODO.md in the same PR or work item as the related implementation.

---

## Decomposition Procedure

### Step 1: Understand the Request

Read the request. If anything is blocking and cannot be answered by reading the codebase, run the `grill-me` skill first to resolve ambiguity.

### Step 2: Map Dependencies

Identify what the request depends on:

- Existing modules that need modification
- New modules that need creation
- External dependencies that need adding
- Data or schemas that need updating

### Step 3: Break Into Tickets

Order tickets so each builds on the last:

1. Foundation tickets (data structures, interfaces, schemas)
2. Core implementation tickets
3. Integration tickets
4. Test and validation tickets
5. Documentation tickets

Each ticket should be independently testable; all tickets for a feature are reviewed together as one completed feature.

### Step 4: Prioritize

Place tickets in the correct section:

- What must be done first → Ready
- What comes after → Next
- What can't start yet → Blocked (with reason)

### Step 5: Present the Plan

Present the plan to the user. Wait for "go" before implementation begins (Delivery mode only).

---

## Ticket Status Updates

When work progresses, update the marker on the ticket line:

| Action | Marker change |
|---|---|
| Prioritize | 🔵→🟠 (move to Ready section) |
| Start working | 🟠→🟡 (move to Active section) |
| Feature implementation complete | all related 🟡→🔍 (mark the feature set in-review) |
| Reviewer approves | Scientific Reviewer moves all related 🔍→✅ (move feature set to Done) |
| Reviewer requests changes | affected 🔍→🟡 (back to Active) |
| Blocked | any→⛔ (move to Blocked section, note the blocker) |

Always update TODO.md in the same commit/PR as the related implementation work.
