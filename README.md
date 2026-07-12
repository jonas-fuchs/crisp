# CRISP — Copilot Research Infrastructure for Scientific Python

VS Code Copilot customizations for scientific Python: instructions, agents, skills, prompts, and templates.

## Quick Start

```bash
./scripts/install.sh             # copy to ~/.copilot/
./scripts/install.sh --link      # symlink (for active development)
./scripts/install.sh --dry-run   # preview
./scripts/install.sh --uninstall # remove
python3 scripts/validate_customizations.py  # validate
```

## Workflow

```
User request
     │
     ▼
Grill (grill-me skill)          ← if ambiguous: ask 2-5 blocking questions, stop
     │
     ▼
Plan (delivery-planning skill)  ← decompose into tickets with acceptance criteria
     │
     ▼  [Planning Gate: user says "go"]
     │
Build (Builder agent)           ← TDD, discovers canonical commands, hands off
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

## Prompts

| Command | Purpose |
|---|---|
| `/plan-change` | Plan a change: clarify, decompose, present tickets, wait for "go" |
| `/review-change` | Review completed work: 6-axis audit, return verdict |
| `/prepare-pr` | Summarize changes, run final validation, generate PR description |
| `/reproduce-result` | Reproduce a computational result from recorded provenance |

## Templates

- **`SCIENTIFIC_CONTRACT.md`** — pre-implementation contract for numerical work: equations, units, shapes, tolerances, validation sources, stochastic policy, data provenance.
- **`TODO.md`** — sprint planning file (Active / Ready / Next / Blocked / Done).

## Validation

`scripts/validate_customizations.py` checks 10 invariants: frontmatter parsing, skill-directory name match, agent handoff references, tool name validity, web access for research agents, markdown link resolution, skill description distinctness, instruction file conventions, install manifest integrity, and naming conventions.

CI runs on every push and PR via `.github/workflows/validate.yml`.
