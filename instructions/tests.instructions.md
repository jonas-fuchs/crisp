---
name: CRISP test conventions
description: Testing conventions for Python test suites — TDD cycle, test structure, and anti-patterns.
applyTo: "**/tests/**/*.py"
---

# Test Conventions

## TDD Cycle

For Builder-led Delivery work, use the full red-green-refactor cycle:

```
RED: Write a failing test that describes the desired behaviour
 │
 ▼
GREEN: Write the minimum code to make the test pass
 │
 ▼
REFACTOR: Clean up the implementation — tests must still pass
```

Discovery work may begin with characterization, experiments, or reference construction — it is not forced through the TDD cycle until the expected behaviour is understood.

In normal Copilot agent mode, use a test strategy proportionate to the risk. Apply this full cycle when the user requests TDD or the behaviour change warrants it; trivial, low-risk edits are not required to begin with a failing test, but must still receive an appropriate focused check.

### Bug Fixes (Prove-It Pattern)

```
Write a test that reproduces the bug → test FAILS → apply smallest fix → test PASSES → run full suite
```

---

## Test Structure

- Organize related scenarios in test classes with descriptive names that read like a specification.
- Use fixtures for reusable setup: temporary files, in-memory DBs, minimal project DB setup, mock external calls.
- Structure every test in Arrange-Act-Assert phases.
- One concept per test. Do not test multiple behaviours in a single test.
- Test behaviour, not implementation details. Assert on outcomes, not internal call sequences.

---

## Mocking

Prefer real implementations over mocks. Mock only at external service boundaries.

```
Preference order:
1. Real implementation  → highest confidence
2. Fake                 → in-memory version (e.g. tmp SQLite, fakeredis)
3. Stub                 → canned data, no behaviour
4. Mock (interaction)   → use only at external service boundaries
```

---

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Testing implementation details | Breaks on refactor even if behaviour is unchanged | Test inputs and outputs |
| Flaky tests (timing, order-dependent) | Erodes trust | Use deterministic assertions; isolate test state |
| No test isolation | Tests pass alone, fail together | Each test sets up and tears down its own state |
| Mocking everything | Tests pass, production breaks | Prefer real or fake over mock |
| Tests that always pass | Proves nothing | Verify the test fails before the fix |
| Skipping tests to make suite pass | Hides regressions | Fix the test or remove the feature |

---

## Verification Checklist

```
- [ ] Every new behaviour has a corresponding test
- [ ] Bug fixes include a reproduction test that failed before the fix
- [ ] Test names describe the behaviour being verified
- [ ] No tests were skipped or disabled
- [ ] Exception paths are explicit (no silent `except` blocks in touched code)
- [ ] Deterministic outputs remain stable (report/export tests)
- [ ] If a feature was removed, its tests were also removed
```
