# CRISP — Copilot Research Infrastructure for Scientific Python

**CRISP** is a personal AI workbench setup for VS Code and GitHub Copilot. It is built for developing scientific software in Python and follows a scrum-like workflow driven by `TODO.md` as a lightweight ticket system. It contains the custom instructions, agent definitions, and skills I use to tailor Copilot's behaviour to my workflow, including [graphify](https://github.com/Graphify-Labs/graphify) for codebase architecture analysis.

> [!CAUTION]
> This setup is primarily for personal use. Feel free to browse and borrow ideas, but it is not intended as a general-purpose distribution.

## What's Included

- **`copilot-instructions.md`** — Global coding instructions loaded into every Copilot session: scrum workflow, coding principles, security defaults, testing conventions, and project-specific notes.
- **`agents/`** — Custom agent definitions (Builder, Planner, Reviewer, Security, Web, CI/CD, Docs) that implement a lightweight scrum lifecycle.
- **`skills/`** — Domain-specific skill modules covering code review, testing, diagnosis, profiling, security hardening, sprint planning, architecture audits, and more. Includes the graphify skill for building and querying knowledge graphs of your codebase.

## Installation

1. **Copy the contents to your Copilot config directory.**

   The default location for Copilot customisations in VS Code is `~/.copilot/`. If this repository is cloned elsewhere, copy it over:

   ```bash
   cp -r /path/to/this-repo/* ~/.copilot/
   ```

   On most systems `~/.copilot/` maps to `/home/<username>/.copilot/`.

2. **Install graphify** (optional but recommended for architecture analysis):

   ```bash
   pip install graphifyy
   ```

3. **Restart VS Code** (or reload the window) so Copilot picks up the new instructions, agents, and skills.

4. **Verify** by opening a chat session in VS Code — the custom instructions and agents should be available automatically.

## Usage Protocol

The system follows a lightweight scrum lifecycle with two checkpoints — planning and review.

### 1. Planning (Planner agent)

Start a session with the **Planner** agent. Describe the feature, bug, or task you want to work on. The Planner:

- Asks clarifying questions if the request is underspecified.
- Decomposes the work into tickets and writes them to `TODO.md` with backlog (`🔵`) or sprint (`🟠`) markers.
- **Stops** and waits for you to review the plan.

**Checkpoint 1 — your "go":** Review the tickets in `TODO.md`. When you're happy with the plan, say "go" to start implementation.

### 2. Implementation (Builder agent)

The **Builder** agent picks up sprint tickets one at a time and implements them using TDD (test-driven development):

- Writes a failing test, then the minimal code to pass, then refactors.
- Debugs issues using the diagnose skill when needed.
- Profiles and optimises performance bottlenecks using the profiling skill when needed.
- Marks the ticket as in-progress (`🟡`) while working, then as review (`🔍`) when done.
- Hands off to the Reviewer.

### 3. Review (Reviewer agent)

The **Reviewer** agent performs a 5-axis review (correctness, readability, architecture, security, performance):

- **Approve** → ticket marked done (`[x]`).
- **Request changes** → ticket sent back to the Builder with specific findings.

**Checkpoint 2 — review gate:** No work is considered complete until the Reviewer approves it.

### Specialist Agents

The following agents are available by delegation (not directly selectable):

- **Security** — security audits and hardening.
- **Web** — coordinated frontend/backend web work.
- **CI/CD** — GitHub Actions workflow hardening.
- **Docs** — public documentation review and updates.
- **Researcher** — scientific literature research and bioinformatics pre-implementation reviews.

### Typical Session Flow

```
You: "I need to add a variant annotation module"
  → Planner: decomposes into tickets, writes TODO.md, waits for "go"
You: "go"
  → Builder: implements tickets with TDD, hands off to Reviewer
  → Reviewer: reviews, approves or requests changes
You: merge the approved work
```

## License

Personal use only.
