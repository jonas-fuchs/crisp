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

- Run the full planning workflow: clarify → decompose feature → build every related ticket → review feature.
- Write formal, related tickets in TODO.md under one unique `Feature: <name>` section.
- Enforce both gates: planning gate (user approves plan) and review gate (Reviewer approves the complete feature).

---

## TODO.md Structure

The planning file is the single source of truth for work status. It contains one section per feature; each feature carries exactly one status tag:

```markdown
# TODO

## 🟡 Feature: Example feature

- [ ] Ticket title — short description, affected modules
  - [ ] Acceptance: measurable condition
- [ ] Ticket title — short description, affected modules

## 🔍 Feature: Another feature

- [ ] Ticket title — implementation complete, awaiting Scientific Reviewer verdict

## ✅ Feature: Finished feature

- [x] Ticket title — completed (month/year)
```

### Status Tags

| Tag | Meaning |
|---|---|
| 🟡 active | Feature is being worked on right now |
| 🔍 review | Implementation complete, awaiting one Scientific Reviewer verdict |
| ✅ finished | Completed and reviewed |

### Archival

When the file grows beyond ~20 feature sections, move the oldest ✅ finished features to an archive file (`TODO-archive.md`). This keeps the active planning file scannable while preserving project history.

---

### Feature Lifecycle

```
🟡 active ──→ 🔍 review ──→ ✅ finished
    ▲              │
    └──────────────┘
     CHANGES REQUIRED

The Builder moves a feature to 🔍 review only after every ticket for it is implemented. The Reviewer approves or rejects the complete feature together.
```

### Ticket Writing

Each ticket is a single `- [ ]` line under its feature section. Format:

```
- [ ] Title — one-line description; affected modules in parentheses
```

Add acceptance criteria below the ticket line:

```
- [ ] Implement spectral normalization — add normalization step to `spectra.py` (core)
  - [ ] Acceptance: normalized output preserves area under curve
  - [ ] Acceptance: handles edge case of all-zero input
  - [ ] Acceptance: unit test with analytical case passes
```

### Ticket Rules

- One ticket = one self-contained change within exactly one feature.
- Each ticket has clear acceptance criteria, and every ticket for a feature lives under that feature's unique section.
- The Builder completes every related ticket using TDD before initiating review. On APPROVE, the Scientific Reviewer alone marks the reviewed feature ✅ finished.
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

### Step 4: Order Tickets

Write the feature as one section tagged 🟡 active, with tickets ordered so each builds on the last. Note any dependency that prevents starting the feature at the top of the section.

### Step 5: Present the Plan

Present the plan to the user. Wait for "go" before implementation begins (Delivery mode only).

---

## Ticket Status Updates

When work progresses, update the status tag on the feature heading:

| Action | Status change |
|---|---|
| Feature implementation complete | 🟡→🔍 (Builder marks the feature in-review) |
| Reviewer approves | 🔍→✅ (Scientific Reviewer marks the feature finished and checks its tickets) |
| Reviewer requests changes | 🔍→🟡 (back to active) |

Always update TODO.md in the same commit/PR as the related implementation work.
