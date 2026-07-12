---
name: reproducibility-audit
description: 'Audit stochastic reproducibility: random seeds pinned, environment provenance recorded, dataset identity and hashes documented, dependency versions pinned, notebook state clean, and Git commit recorded. Use when reviewing reproducibility of scientific results.'
argument-hint: 'Module, pipeline, or notebook to audit for reproducibility.'
user-invocable: true
disable-model-invocation: false
---

# Reproducibility Audit

## Overview

A reproducibility audit verifies that a computational result can be regenerated from the same inputs, the same code, and the same environment. It checks that stochasticity is controlled, provenance is recorded, and nothing critical is left to chance.

## When to Use

- After implementing a stochastic algorithm or simulation
- Before publishing results derived from computational methods
- When reviewing a pipeline that produces scientific outputs
- After environment or dependency changes
- When a result is difficult to reproduce on a different machine
- When reviewing notebooks for execution state hygiene

---

## Checklist

### 1. Random Seeds

- [ ] All RNG calls use an explicitly set seed — no reliance on global RNG state
- [ ] Seeds are documented at the point of use, not hidden in a distant config
- [ ] For `numpy`, `random.seed()` is avoided in favor of `np.random.default_rng(seed)` (Generator API)
- [ ] For `torch`, both `torch.manual_seed` and `torch.cuda.manual_seed_all` are set if applicable
- [ ] Stochastic tests verify reproducibility by running twice with the same seed and comparing

```
# Good
rng = np.random.default_rng(seed=42)
data = rng.standard_normal(1000)

# Bad — global state, easy to miss
np.random.seed(42)
data = np.random.randn(1000)
```

### 2. Environment Provenance

- [ ] Python version recorded
- [ ] All dependency versions recorded (requirements.txt, pyproject.toml lock, or environment.yml)
- [ ] Hardware/backend recorded if GPU or accelerator is used
- [ ] OS and platform recorded if platform-specific behaviour is possible

Record provenance using one of:
- `pip freeze > requirements_lock.txt`
- `conda env export > environment.yml`
- `python -c "import platform; print(platform.platform())"`

### 3. Dataset Identity

- [ ] Input datasets identified by name, version, and source
- [ ] File hashes (SHA-256 or MD5) recorded for datasets used in published results
- [ ] Download URLs or DOIs recorded
- [ ] Preprocessing steps documented and deterministic
- [ ] Train/test/validation splits are reproducible (fixed seed or explicit split file)

### 4. Dependency Versions

- [ ] Production dependencies pinned to specific versions (not `>=`)
- [ ] Development dependencies pinned to specific versions
- [ ] No implicit system-level dependencies without documentation
- [ ] Known version-sensitive libraries (numpy, scipy, torch, scipy.stats) are explicitly pinned

### 5. Notebook State

- [ ] Notebooks run top-to-bottom without errors after "Restart Kernel and Run All"
- [ ] No hidden state from interactive experimentation
- [ ] Cell execution order matches top-to-bottom layout
- [ ] Output cells reflect the code in the input cells (not stale output from a previous run)
- [ ] Random seeds set in the notebook, not inherited from a kernel that was previously used for exploration
- [ ] No hardcoded absolute paths — use relative paths or config

### 6. Git Commit Recording

- [ ] The Git commit hash at the time of result generation is recorded
- [ ] Uncommitted changes are either committed, stashed, or explicitly noted
- [ ] Branch name recorded if working outside the main branch
- [ ] Results include a provenance pointer to the exact code state

```python
import subprocess
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
print(f'Results generated at commit: {commit}')
```

### 7. Deterministic Output

- [ ] Report exports (HTML, JSON, TSV) are byte-stable across reruns with the same inputs
- [ ] Timestamps and machine names are excluded from deterministic outputs or placed in a separate metadata file
- [ ] Floating-point output is not sensitive to thread scheduling (single-threaded for reproducibility if needed)

### 8. Numerical Stability

- [ ] Results are not sensitive to platform-specific floating-point behaviour (or platform is pinned)
- [ ] Known sources of non-determinism (BLAS threading, GPU kernels) are documented and controlled
- [ ] `OMP_NUM_THREADS=1` or equivalent is set if BLAS non-determinism is a concern

---

## Output Format

```
## Reproducibility Audit: [module/pipeline/notebook]

### Summary
- Overall assessment: [Pass / Needs Improvement / At Risk]
- Key risks: [list]

### Findings

#### Random Seeds
- [finding or "No issues"]

#### Environment Provenance
- [finding or "No issues"]

#### Dataset Identity
- [finding or "No issues"]

#### Dependency Versions
- [finding or "No issues"]

#### Notebook State
- [finding or "No issues"]

#### Git Commit Recording
- [finding or "No issues"]

#### Deterministic Output
- [finding or "No issues"]

#### Numerical Stability
- [finding or "No issues"]

### Recommendations
1. [highest-priority fix]
2. [next fix]
3. [next fix]
```
