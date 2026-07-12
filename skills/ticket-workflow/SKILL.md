---
name: ticket-workflow
description: 'Manage TODO.md tickets. Use when adding new tasks, marking work done, checking whether a feature is already implemented, drafting new todo items from a plan, selecting next priorities, or keeping the planning file accurate after a change.'
argument-hint: 'What to add, update, check, or verify in TODO.md.'
user-invocable: true
disable-model-invocation: false
---

# Ticket Workflow

## Planning Source of Truth

`TODO.md` is the single planning source of truth and the **ticket system** for the scrum workflow. Always read it before any substantial change.

## Structure

The file has three sections:

- **Done** — completed work, grouped by theme, marked `[x]`. Never remove entries; they serve as project history.
- **Next / Backlog** — open work, grouped by theme. Each item carries a **lifecycle marker** and a **priority emoji**:
- **Deferred** (subsection of Next) — explicitly postponed items; keep them visible but do not pick them up unless requested.

### Ticket Lifecycle Stages

| Marker | Stage | Meaning |
|---|---|---|
| `- [ ] 🔵` | Backlog | Triaged but not yet prioritized for a sprint |
| `- [ ] 🟠` | Sprint | Prioritized for the current sprint; ready to pick up |
| `- [ ] 🟡` | In-Progress | Being implemented right now by the Builder |
| `- [ ] 🔍` | Review | Implementation complete, awaiting Reviewer verdict |
| `- [x]` | Done | Reviewed and approved; moved to Done section |

### Priority Emojis

Combined with the lifecycle marker:

- 🔴 high — tackle first; blockers or foundational work
- 🟡 medium — important but not urgent
- 🟢 low — nice-to-have or dependent on higher-priority work

Example: `- [ ] 🟠 🔴 Add foo to bar.py so that X is possible.`

## How to Select Work

1. Prefer `🟠` (sprint) items with 🔴 priority unless the user specifies otherwise.
2. When a group of items is marked "introduce together", implement them in one change.
3. If user instructions conflict with to-do priorities, follow the user and update the to-do afterwards.
4. If only 🟡 items are present, reevaluate the priorities for all tasks.

## How to Advance Tickets Through the Lifecycle

### Backlog → Sprint
The Planner promotes backlog items to sprint when prioritizing:
- Change `- [ ] 🔵` to `- [ ] 🟠`.
- Assign or confirm the priority emoji.

### Sprint → In-Progress
When the Builder starts work:
- Change `- [ ] 🟠` to `- [ ] 🟡`.
- The Planner should delegate the ticket to the Builder.

### In-Progress → Review
When the Builder completes work:
- Change `- [ ] 🟡` to `- [ ] 🔍`.
- The Planner should delegate to the Reviewer.

### Review → Done
When the Reviewer approves:
- Move the entry from **Next** to the matching theme group in **Done**.
- Change to `- [x]` and drop the lifecycle marker and priority emoji.
- Keep the description concise — one line that summarises what was built.

### Review → In-Progress (Changes Requested)
When the Reviewer requests changes:
- Change `- [ ] 🔍` back to `- [ ] 🟡`.
- The Planner should re-delegate to the Builder with specific findings.

## How to Mark Work Done

When a feature is fully implemented and reviewed:

1. Move its entry from **Next** to the matching theme group in **Done**, or create a new group if none fits.
2. Change the marker to `- [x]` and drop the lifecycle + priority emojis.
3. Keep the description concise — one line that summarises what was built.
4. Update the to-do in the same change as the implementation.

## How to Add New Items

1. Choose the correct theme group in **Next / Backlog**, or add a new group if none fits.
2. Assign a lifecycle marker: `🔵` (backlog) for triaged-but-unprioritized, `🟠` (sprint) for prioritized-this-sprint.
3. Assign a priority emoji based on urgency and dependency order: 🔴, 🟡, or 🟢.
4. Write a single-sentence description that includes the affected module(s) and the observable behaviour change.
5. If the item is intentionally deferred, place it in the **Deferred** subsection with a brief rationale.

## How to Check if a Task is Already Done

1. Read the **Done** section and search for matching keywords, module names, or feature descriptions.
2. If a close match is found in **Done**, verify by reading the relevant source files or tests.
3. If verification confirms the feature exists, report it as already done and do not re-add it.
4. If the **Done** entry exists but source code evidence is missing, flag the discrepancy.

## How to Draft New Todo Items from a Plan

1. Read the plan or user request and decompose it into observable behaviour changes.
2. Check **Done** for each proposed item — skip anything already completed.
3. Check **Next** for exact or near-duplicate items — propose an update rather than a duplicate.
4. Assign priority based on dependencies, blocking risk, and user priority signals.
5. Write each item as a single sentence: affected module(s) + observable behaviour change.
6. Group related items under one theme heading rather than creating isolated entries.
7. Propose the additions for confirmation before editing `TODO.md` unless explicitly told to write immediately.

## What Not to Do

- Do not remove **Done** entries — they are project history.
- Do not invent a "Now" section; the lifecycle marker (`🟡` in-progress) replaces it.
- Do not leave the to-do stale after a change.
- Do not add duplicate items — check both **Done** and **Next / Backlog** first.
- Do not write multi-sentence todo items; each item must be implementable from one sentence.
- Do not skip lifecycle markers — every open item must have one of `🔵` `🟠` `🟡` `🔍`.
- Do not implement anything — only manage the to-do.

## Output Format

When proposing new todo items, output a preview block showing exactly how the entries will appear in `TODO.md` before writing the file. For example:

```
### My Theme

- [ ] 🟠 🔴 Add `foo` parameter to `src/core/bar.py` so that X is possible.
- [ ] 🟠 🟡 Extend `db/results.py` to persist Y when Z occurs.
- [ ] 🔵 🟢 Add test coverage for edge case E in `src/core/bar.py`.
```

When marking items done, show the moved entry with its `[x]` prefix and the target **Done** group.
