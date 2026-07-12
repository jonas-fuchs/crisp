---
name: scientific-validation
description: 'Validate scientific computations against independent references. Use when implementing numerical algorithms, checking convergence, verifying conservation laws, or establishing that a computational result is scientifically correct. Distinct from ordinary software testing.'
argument-hint: 'What to validate: algorithm, computation, or model. Include the reference source if known.'
user-invocable: true
disable-model-invocation: false
---

# Scientific Validation

## Overview

Scientific validation is distinct from ordinary software testing. A passing test suite proves the code runs; scientific validation proves the result is correct. This skill provides the procedure for validating numerical computations against independent references.

## When to Use

- Implementing or modifying a numerical algorithm
- Verifying that a computational result matches a known analytical solution
- Checking convergence, stability, or conservation properties
- Establishing tolerance rationale for numerical comparisons
- Validating against a trusted dataset or independent implementation
- Reviewing a scientific computation before publication or deployment

When NOT to use: ordinary software testing without numerical content (use `scientific-testing` skill instead).

---

## Validation Sources

Each scientific computation needs at least one independent validation source. Listed in order of strength:

### 1. Analytical Case

A closed-form solution exists for a simple input.

```python
# Example: validate a numerical integrator against the exact integral
# ∫₀¹ x² dx = 1/3
numerical = integrate(f=lambda x: x**2, a=0, b=1, n=1000)
assert abs(numerical - 1/3) < 1e-6
```

### 2. Independent Reference Implementation

A trusted implementation using a different library or different approach produces the same result.

```python
# Validate custom FFT against numpy
custom_result = my_fft(signal)
numpy_result = np.fft.fft(signal)
np.testing.assert_allclose(custom_result, numpy_result, rtol=1e-10)
```

### 3. Trusted Dataset

Ground-truth data with known expected outputs.

```python
# Validate against a published benchmark dataset
expected = load_reference_results('benchmark_v2.json')
actual = run_pipeline(benchmark_input)
assert_results_match(actual, expected, tolerance=1e-8)
```

### 4. High-Precision Implementation

`mpmath` or similar at extended precision confirms the result.

```python
import mpmath
mpmath.mp.dps = 50  # 50 decimal digits
high_precision = mpmath.quad(lambda x: x**2, [0, 1])
assert abs(float(high_precision) - numerical) < 1e-12
```

### 5. Stated Invariant or Conservation Law

A property that must hold for the computation to be correct.

```python
# Validate that a particle simulation conserves total energy
initial_energy = total_energy(system)
simulate(system, dt=0.01, steps=1000)
final_energy = total_energy(system)
assert abs(final_energy - initial_energy) / initial_energy < 1e-6
```

### 6. Metamorphic Property

The output changes predictably under a defined input transformation.

```python
# Metamorphic property: scaling the input by k should scale the output by k
result_original = compute_norm(vector)
result_scaled = compute_norm(vector * 3.0)
assert abs(result_scaled - 3.0 * result_original) < 1e-10
```

---

## Tolerance Justification

Numerical comparisons require explained tolerances. Never set a tolerance by convenience.

| Source | Tolerance basis |
|---|---|
| Scale | `rtol` proportional to the magnitude of the expected value |
| Conditioning | Wider tolerance for ill-conditioned problems (condition number × machine epsilon) |
| Discretization error | Tolerance matching the expected truncation error (e.g. O(h²) for a second-order method) |
| Stochastic variation | Tolerance covering the expected variance (with fixed seed and documented sample size) |
| Measurement uncertainty | Tolerance matching instrument or data precision |

### Anti-pattern

```python
# BAD: tolerance chosen to make the test pass
np.testing.assert_allclose(result, expected, rtol=1e-2)  # why 1e-2?

# GOOD: tolerance justified from the method's known error
# Second-order finite difference: error ~ O(h²) where h=0.01 → error ~ 1e-4
np.testing.assert_allclose(result, expected, rtol=1e-3)  # 10× the expected error
```

---

## Validation Procedure

### Step 1: Identify the Scientific Claim

What equation, algorithm, or model does this code implement? What is the expected behaviour?

### Step 2: Select the Validation Source

Which independent reference is available and appropriate?

- Is there an analytical solution for a simple case?
- Is there a trusted implementation in a different library?
- Is there a dataset with known ground truth?
- Is there a conservation law or invariant?
- Is there a metamorphic property?

### Step 3: Prepare the Test Case

- Choose inputs that exercise the computation meaningfully (not trivially easy).
- For analytical cases, use inputs where the closed-form solution is known.
- For convergence checks, run at multiple resolutions and verify the error decreases at the expected rate.

### Step 4: Run and Compare

- Run the implementation and the reference.
- Compare using a justified tolerance.
- If the comparison fails, investigate before widening the tolerance.

### Step 5: Document

Record:

- The validation source used.
- The tolerance and its justification.
- The input case.
- The result (pass/fail).
- The Git commit of the implementation.

---

## Convergence Checking

For numerical methods that approximate a continuous solution:

```python
# Verify convergence rate matches the method's theoretical order
errors = []
hs = [0.1, 0.05, 0.025, 0.0125]
for h in hs:
    error = abs(numerical_solution(h) - analytical_solution)
    errors.append(error)

# Check that error ~ h^p where p is the expected order
rates = [np.log(errors[i]/errors[i+1]) / np.log(hs[i]/hs[i+1]) for i in range(len(errors)-1)]
assert all(abs(rate - expected_order) < 0.1 for rate in rates)
```

---

## Output Format

```
## Scientific Validation: [algorithm/computation name]

### Scientific Claim
[What equation or algorithm is being validated]

### Validation Source
[Analytical case / independent reference / trusted dataset / high-precision / invariant / metamorphic]

### Test Case
[Input, parameters, and why they were chosen]

### Result
- Implementation output: [value]
- Reference output: [value]
- Difference: [value]
- Tolerance: [value] — justification: [explanation]
- Verdict: PASS / FAIL

### Provenance
- Git commit: [hash]
- Dependencies: [versions]
- Random seed: [value, if applicable]
```
