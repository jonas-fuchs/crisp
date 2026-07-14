# CRISP — Copilot Research Infrastructure for Scientific Python

> **Personal use only.** This repository contains my personal Copilot configuration — instructions, agents, skills, and prompts tuned for my scientific Python workflow. It is not a general-purpose framework and is not intended for external use or distribution.

VS Code Copilot customizations for scientific Python: instructions, agents, skills, prompts, and templates.

## Quick Start

```bash
./scripts/install.sh             # copy to ~/.copilot/
./scripts/install.sh --link      # symlink (for active development)
./scripts/install.sh --dry-run   # preview
./scripts/install.sh --uninstall # remove
```

## Workflow

```
User request
     │
     ▼
Planner agent                   ← clarify, grill-me if needed, decompose, write TODO.md
     │
     ▼  [Planning Gate: user says "go"]
     │
Builder agent                   ← TDD, discovers canonical commands, hands off
     │
     ▼  [Review Gate: Scientific Reviewer approves]
     │
Done (TODO.md ticket → Done)
```

### Work Modes

- **Discovery** — explore, prototype, tune. Skip planning ceremony. Open one TODO.md entry, go straight to Builder.
- **Delivery** — production change with both gates enforced.

## Instructions

Always-on context, scoped by file type:

| File | Applies to | Covers |
|---|---|---|
| `general.instructions.md` | all files | Workflow, change discipline, command discovery, security defaults |
| `python.instructions.md` | `*.py` | Imports, module layout, type hints, dead code rules |
| `tests.instructions.md` | `tests/**/*.py` | TDD cycle, test structure, mocking, anti-patterns |
| `scientific.instructions.md` | `*.py`, `*.ipynb` | Units, shapes, dtypes, tolerances, validation independence, reproducibility |

## Agents

| Agent | Role |
|---|---|
| **Planner** | Clarifies requests, runs grill-me when needed, decomposes into tickets, writes TODO.md, enforces the planning gate. Hands off to Builder on "go". Does not implement. |
| **Builder** | Implements tickets using TDD. Discovers test/build commands from project config. Hands off to Scientific Reviewer. Does not mark tickets done. |
| **Scientific Reviewer** | Read-only review on six axes: scientific definition, units, numerical behaviour, validation independence, reproducibility, software quality. Returns APPROVE or CHANGES REQUIRED. |
| **Researcher** | Literature research (with `web` tool) and bioinformatics pre-implementation review. |

## Skills

| Skill | Use when |
|---|---|
| `grill-me` | Task is underspecified — ask targeted questions before planning |
| `delivery-planning` | Decompose a feature into tickets, manage TODO.md lifecycle |
| `scientific-testing` | Write tests with TDD and independent scientific validation |
| `scientific-validation` | Validate numerical computations against independent references |
| `software-quality-audit` | 6-axis code review before merge |
| `architecture-audit` | Review module boundaries, complexity, and coupling |
| `security-review` | Static security checklist (read-only) |
| `reproducibility-audit` | Audit stochastic reproducibility, seeds, provenance |
| `diagnose` | Debug with reproduce → minimize → hypothesize → fix loop |
| `profiling` | Measure performance, identify hot paths, optimise, re-measure |
| `graphify` | Cross-module architecture analysis (manual only, forked context) |

## Templates

- **`SCIENTIFIC_CONTRACT.md`** — pre-implementation contract for numerical work: equations, units, shapes, tolerances, validation sources, stochastic policy, data provenance.
- **`TODO.md`** — sprint planning file (Active / Ready / Next / Blocked / Review / Done).
