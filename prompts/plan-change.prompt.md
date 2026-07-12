---
name: plan-change
description: 'Plan a change or feature before implementation. Runs clarification, decomposition, and produces a TODO.md-ready plan. Delivery mode by default; Discovery mode if specified.'
---

# Plan a Change

Use the `delivery-planning` skill to run this workflow.

## Steps

1. **Understand the request.** Read the user's description. Identify the affected modules, the expected behaviour change, and any constraints.

2. **Clarify.** If anything is blocking and cannot be answered by reading the codebase, use the `grill-me` skill to ask a short set of targeted questions. Do not ask what you can discover yourself.

3. **Determine mode.**
   - If the user said "explore," "prototype," "try," or the outcome is unknown → Discovery mode. Open a single TODO.md entry; skip formal decomposition.
   - Otherwise → Delivery mode. Proceed to full decomposition.

4. **Map dependencies.** Identify existing modules that need modification, new modules that need creation, external dependencies, and data/schema changes.

5. **Decompose into tickets.** Order tickets so each builds on the last:
   - Foundation (data structures, interfaces, schemas)
   - Core implementation
   - Integration
   - Tests and validation
   - Documentation

6. **Prioritize.** Place tickets in the correct TODO.md section (Ready, Next, Blocked).

7. **Present the plan.** Show the ticket list to the user. Wait for "go" before implementation begins (Delivery mode only).

## Output

Present:
- The mode (Discovery or Delivery)
- The tickets with acceptance criteria
- The dependency order
- Any blockers or risks

Then stop. Do not start implementation until the user says "go."
