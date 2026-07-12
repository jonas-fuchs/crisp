---
name: grill-me
description: 'Use when a task is underspecified, risky, or needs alignment before code changes. Ask a short set of targeted questions to resolve blocking ambiguity. Lightweight and fast — no planning ceremony.'
argument-hint: 'The task, request, or change that needs clarification before proceeding.'
user-invocable: true
disable-model-invocation: false
---

# Grill Me

## Overview

A lightweight clarification gate. Before planning or building, if a task is underspecified or risky, ask a short set of sharply targeted questions to resolve blocking ambiguity. This is not a planning workflow — it produces questions, not tickets.

## When to Use

- A request is underspecified — key decisions are ambiguous and would change the implementation.
- A task carries risk (data loss, security, breaking changes) and needs alignment first.
- You are about to plan but cannot without the answer to a few blocking questions.
- The user's intent could mean two materially different things.

When NOT to use:

- The codebase already answers the question — read it and decide yourself.
- The answer would not change the plan or implementation.
- The task is clear and ready to decompose (skip to `delivery-planning`).
- Discovery/exploration where ambiguity is the point.

## Rules

1. **Answer what you can yourself.** Read the codebase, check conventions, look at existing patterns. Do not ask what you can discover.
2. **Ask only blocking questions.** Every question must be one where the answer changes the plan, the implementation approach, or the acceptance criteria. If the answer would not change what you do, do not ask it.
3. **Maximum 5 questions.** Fewer is better. 2-3 sharp questions are better than 5 broad ones.
4. **Be specific, not open-ended.** "Should X be stored in the database or computed on-the-fly?" beats "How should we handle X?"
5. **Provide options when useful.** If there are 2-3 realistic choices, list them. The user can pick or give a different answer.
6. **One round, then proceed.** Ask once, incorporate the answers, and move to planning or implementation. Do not loop.

## Procedure

1. **Read the request carefully.** What is the user asking for?

2. **Read the codebase.** What does the current state tell you? What conventions exist? What are the constraints?

3. **Identify ambiguities.** What is left unspecified that would change what you build? Filter ruthlessly — keep only the questions where different answers lead to materially different implementations.

4. **Formulate questions.** For each blocking ambiguity, write a specific question. If there are realistic options, present them.

5. **Ask.** Present the questions and stop. Wait for the user's answers before proceeding.

6. **Incorporate and proceed.** Once answered, move to `delivery-planning` (if the task needs decomposition) or directly to the Builder (if the task is now clear enough to implement).

## Output Format

```
## Quick questions before I start

1. [specific question]
   - Option A: ...
   - Option B: ...

2. [specific question]

...

These answers will change [what specifically].
```

Then stop. Do not plan or build until the user answers.
