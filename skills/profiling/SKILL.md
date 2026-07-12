---
name: profiling
description: 'Use when code is slow, memory-heavy, or needs optimisation. Profile with cProfile, line_profiler, or memory_profiler, identify hot paths, and apply targeted optimisations. Measure before and after — never optimise blind.'
argument-hint: 'What is slow or memory-heavy: function, module, or workflow step.'
user-invocable: true
disable-model-invocation: false
---

# Profiling

## Overview

Use this skill when performance is a problem — code is too slow, uses too much memory, or needs to scale to larger inputs. The discipline is simple: **measure first, optimise second, measure again**. Never guess where the bottleneck is; always profile before changing code.

Scientific Python code has a common optimisation ladder:

```
Correct code ──→ Profiled code ──→ Vectorised code ──→ Parallelised code
```

Each step should only be taken when the previous one is measured and proven insufficient.

## When to Use

- A function, module, or workflow step is too slow for its intended use.
- Memory usage is unexpectedly high (OOM errors, excessive swapping).
- A user or reviewer asks for performance improvements.
- Scaling to larger datasets.
- Before and after a planned optimisation to prove it worked.

When NOT to use: premature optimisation of code that is already fast enough.

---

## Workflow

### 1. Define the Baseline

Before profiling, establish a measurable baseline:

- What is the current wall-clock time for a representative input?
- What is the current peak memory usage?
- What is the target performance (if known)?

Use a realistic input — the largest dataset the code is expected to handle in production, or a representative sample of it.

### 2. Profile CPU

Start with `cProfile` to get a function-level overview. For line-level detail on the hottest function, use `line_profiler`.

Key things to look at:

- `cumtime` — cumulative time spent in a function and all its callees.
- `tottime` — time spent in the function itself, excluding callees.
- `ncalls` — number of calls; unexpectedly high counts may indicate a hidden loop or N+1 pattern.

### 3. Profile Memory

For memory issues, use `memory_profiler` or `tracemalloc` for a quick peak-memory check.

### 4. Identify the Bottleneck

From the profile output, identify the single biggest contributor:

- Is one function dominating `tottime`? → Optimise that function's inner logic.
- Is one function dominating `cumtime` but not `tottime`? → The bottleneck is in a callee — profile deeper.
- Are there many calls to a cheap function? → Look for unnecessary repeated work.
- Is memory growing linearly with input? → Look for accumulating lists, copies, or unclosed resources.

Form one concrete hypothesis about the bottleneck before optimising.

### 5. Apply Targeted Optimisation

Choose the smallest change that addresses the identified bottleneck. Common patterns in scientific Python:

| Bottleneck | Optimisation |
|---|---|
| Python-level loop over array | Vectorise with NumPy |
| Repeated DataFrame `.apply()` | Use vectorised pandas operations or `itertuples` |
| Repeated file parsing | Parse once, cache the result |
| Repeated regex compilation | Compile at module level |
| Large intermediate arrays | Use in-place operations (`out=`, `+=`) or generators |
| Quadratic lookup (`x in list`) | Convert to set or dict for O(1) lookup |
| DataFrame growing in a loop | Pre-allocate or collect then `pd.concat` once |
| Pure CPU-bound loop | Consider `multiprocessing` or `joblib.Parallel` |
| I/O-bound processing | Use async or thread pool for concurrent I/O |

Do not apply multiple optimisations at once — change one thing, measure, then decide.

### 6. Verify the Improvement

Re-run the same measurement from step 1. Compare:

- Did wall-clock time improve?
- Did peak memory decrease?
- Are the results identical (or within acceptable numerical tolerance)?

If the optimisation did not help, revert it.

### 7. Regression-Test

Add or update a test that locks in the optimised behaviour:

- A correctness test confirming the output is unchanged.
- A performance smoke test if the improvement is critical.

---

## Rules

- **Never optimise without measuring first.** "Feels slow" is not a profile.
- **One optimisation at a time.** Measure between each change.
- **Revert optimisations that don't help.** Speculative changes add complexity for no benefit.
- **Correctness before speed.** A fast wrong answer is still wrong.
- **Vectorise before parallelising.** NumPy vectorisation is simpler and often faster than multiprocessing for moderate data sizes.
- **Profile the realistic input.** Profiling on tiny inputs hides bottlenecks that emerge at scale.
- **Keep optimisations readable.** If the optimised code is hard to understand, add an intent comment explaining the trade-off.

## Output Style

- State the baseline measurement (time and/or memory).
- State the profile result and the identified bottleneck.
- State the hypothesis and the optimisation applied.
- State the post-optimisation measurement and the improvement factor.
- State whether tests still pass.
