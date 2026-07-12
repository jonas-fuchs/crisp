# Scientific Contract

> Fill in this template before implementing a numerical algorithm or scientific computation. It forces explicit agreement on equations, units, shapes, tolerances, and validation sources. Place the completed contract alongside the implementation (e.g. `docs/contracts/spectral_normalization.md`).

---

## Scientific Objective

**What does this computation do?** One-paragraph description of the scientific or numerical problem being solved.

## Definitions and Equations

**Mathematical specification.** Write the key equations in LaTeX. Define every symbol.

$$
\text{result} = f(x, \theta)
$$

| Symbol | Definition | Units |
|---|---|---|
| $x$ | Input signal | [units] |
| $\theta$ | Parameters | [units] |
| $\text{result}$ | Output | [units] |

## Units and Coordinate Conventions

- Input units: [e.g. nm, counts, dimensionless]
- Output units: [e.g. normalized intensity, dimensionless]
- Coordinate system: [e.g. wavelength in vacuum, wavenumber]
- Reference frame: [e.g. lab frame, comoving]

## Array Shapes and dtypes

| Array | Shape | dtype | Description |
|---|---|---|---|
| input | `(N,)` or `(N, M)` | `float64` | Raw input data |
| output | `(N,)` or `(N, M)` | `float64` | Computed result |

- Dimension labels: [e.g. axis 0 = wavelength, axis 1 = time]
- Memory layout: [e.g. C-contiguous]

## Supported Input Domain

- Valid range for each input parameter
- What happens outside the valid range (error, clamp, extrapolate?)
- Special values (NaN, Inf, zero, negative)

## Approximations and Assumptions

- Mathematical approximations used (e.g. small-angle, first-order Taylor)
- Physical assumptions (e.g. isotropic medium, non-relativistic)
- Regime of validity (e.g. valid for $\lambda > 400\,\text{nm}$)

## Error Metrics

How is correctness measured?

| Metric | Formula | Target |
|---|---|---|
| Relative error | $\|r - r_{\text{ref}}\| / \|r_{\text{ref}}\|$ | $< 10^{-6}$ |
| Absolute error | $\|r - r_{\text{ref}}\|$ | $< 10^{-8}$ |
| RMS error | $\sqrt{\frac{1}{N}\sum_i (r_i - r_{\text{ref},i})^2}$ | $< 10^{-4}$ |

## Tolerance Rationale

Justify each tolerance from its numerical source:

- [ ] Scale: tolerance proportional to expected value magnitude
- [ ] Conditioning: tolerance accounts for condition number
- [ ] Discretization: tolerance matches truncation error of the method
- [ ] Stochastic: tolerance covers expected variance (with fixed seed)
- [ ] Measurement: tolerance matches instrument/data precision

## Reference Cases

List the independent validation sources:

| Case | Type | Description | Expected result |
|---|---|---|---|
| 1 | Analytical | [e.g. $\int_0^1 x^2\,dx = 1/3$] | $1/3$ |
| 2 | Independent reference | [e.g. `scipy.integrate.quad`] | [value] |
| 3 | Trusted dataset | [e.g. NIST StRD] | [expected] |
| 4 | Invariant | [e.g. conservation of total energy] | [property] |

## Stochastic Policy

- Is this computation stochastic? [Yes / No]
- If yes:
  - Random seed: [value or "from config"]
  - RNG library and function: [e.g. `numpy.random.default_rng(42)`]
  - Expected variance across runs: [estimate]
  - Reproducibility test: [e.g. "run twice, compare outputs"]

## Data Provenance

- Source dataset: [name, version, URL or DOI]
- SHA-256 hash: [hash of the input file]
- Preprocessing applied: [steps, in order]
- Split/selection: [how the subset was chosen]

## Performance Constraints

- Target throughput: [e.g. 1000 spectra/second]
- Target latency: [e.g. < 100ms per call]
- Memory limit: [e.g. < 2GB peak]
- Parallelism: [single-threaded / multi-core / GPU]

## Known Limitations

- What this computation does NOT handle
- Edge cases that are explicitly unsupported
- Planned but unimplemented features
