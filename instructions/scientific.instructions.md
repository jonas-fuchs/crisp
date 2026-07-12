---
name: Scientific software invariants
description: Numerical correctness, reproducibility, and scientific validation rules.
applyTo: "**/*.py,**/*.ipynb"
---

# Scientific Software Invariants

These rules apply to all scientific Python code and notebooks. They are distinct from ordinary software tests — a passing test suite does not prove scientific validity.

---

## Numerical Correctness

- Treat units, coordinate systems, sign conventions, array shapes, dtypes, valid input domains, and random-state behaviour as part of the API. Document them in docstrings or a scientific contract.
- Check convergence, residuals, conservation laws, or metamorphic properties where applicable.
- Do not widen a tolerance solely to make a failing test pass.
- Explain nontrivial numerical tolerances from scale, conditioning, discretization error, stochastic variation, or measurement uncertainty.
- Distinguish scientific uncertainty from software defects.

---

## Validation Independence

- Do not derive expected test values from the implementation under test.
- Validate scientific behaviour with at least one of:
  - An analytical case with a known closed-form solution
  - An independent reference implementation
  - A trusted dataset with known ground truth
  - A high-precision implementation (e.g. `mpmath` at extended precision)
  - A stated invariant or conservation law
  - A metamorphic property (the output changes predictably under a defined input transformation)

---

## Reproducibility and Provenance

- Record random seeds, dataset identity, dependency versions, and relevant hardware or numerical backend details.
- Pin random seeds explicitly. Do not rely on global RNG state.
- For stochastic simulations, verify reproducibility by running twice with the same seed and comparing outputs.
- Record the Git commit used to produce any published result.

---

## Notebook Hygiene

- Reset and re-run all cells from top to bottom before trusting notebook output.
- Do not leave hidden state that makes the notebook non-reproducible from a fresh kernel.
- Record environment and dependency versions in the notebook or an accompanying file.

---

## Scientific Contract

Each scientific repository should maintain a `docs/SCIENTIFIC_CONTRACT.md` (see `templates/SCIENTIFIC_CONTRACT.md`). At minimum, document:

- Scientific objective
- Definitions and equations
- Units and coordinate conventions
- Array shapes and dtypes
- Supported input domain
- Approximations and assumptions
- Error metrics
- Tolerance rationale
- Reference cases
- Stochastic policy
- Data provenance
- Performance constraints
- Known limitations
