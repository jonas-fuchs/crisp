---
name: reproduce-result
description: 'Reproduce a computational result from a published or stored run. Verifies reproducibility by regenerating outputs from recorded provenance: code commit, dataset, environment, and seed.'
---

# Reproduce a Result

Use the `reproducibility-audit` skill checklist to verify each step.

## Steps

1. **Locate provenance.** Find the record of the original run:
   - Git commit hash
   - Dataset identifier or hash
   - Environment / dependency versions
   - Random seed (if applicable)
   - Hardware / backend (if applicable)

2. **Check out the code.** Verify the working tree is at the recorded commit, or check it out:
   ```
   git rev-parse HEAD  → compare to recorded hash
   ```
   Note any uncommitted changes. If the original run had uncommitted changes, this must be documented — otherwise reproduction may fail.

3. **Verify the environment.**
   - Compare installed dependency versions against the recorded provenance.
   - If versions differ, flag the mismatch. Some differences are benign; others (numpy, scipy, torch) may change numerical results.

4. **Verify dataset identity.**
   - Compare file hashes (SHA-256) of input datasets against recorded hashes.
   - If hashes differ, the input data has changed — reproduction will fail.

5. **Run the computation.**
   - Set the recorded random seed explicitly.
   - Use the same backend (CPU/GPU) if specified.
   - Discover and use the canonical run command for the repository.

6. **Compare outputs.**
   - Compare the regenerated output against the stored output.
   - For numerical results: use a justified tolerance. If results differ beyond tolerance, investigate:
     - Dependency version mismatch?
     - Different BLAS/threading?
     - Different hardware?
     - Floating-point non-determinism?

7. **Report.**

```
## Reproduction Report

### Original Run
- Git commit: [hash]
- Dataset: [name, version, SHA-256]
- Environment: [key dependency versions]
- Seed: [value]
- Backend: [CPU/GPU]

### Reproduction Run
- Git commit: [hash — same/different]
- Dataset: [hash — same/different]
- Environment: [versions — same/different]
- Seed: [value — same/different]
- Backend: [CPU/GPU — same/different]

### Result
- Output match: [exact / within tolerance / mismatch]
- Tolerance: [value and justification]
- Verdict: REPRODUCIBLE / NOT REPRODUCIBLE

### Notes
[Any mismatches and their likely impact]
```
