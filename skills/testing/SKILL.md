---
name: testing
description: 'Use when implementing logic, fixing bugs, or changing behavior. Drive the work with a red-green-refactor loop and prove the result with pytest.'
argument-hint: 'What to test: new feature, bug fix, edge case, or module name.'
user-invocable: true
disable-model-invocation: false
---

# Testing

## Overview

This is the repository's TDD skill. Write a failing test before writing the code that makes it pass. For bug fixes, reproduce the bug with a test before attempting a fix. Tests are proof — "seems right" is not done. A codebase with good tests is the fastest path to confident refactoring; a codebase without tests is a liability.

Run the full test suite with:

```bash
python -m pytest
```

Web-layer tests only:

```bash
python -m pytest tests/test_web_app.py -q
```

## When to Use

- Implementing any new logic or behaviour
- Fixing any bug (the Prove-It Pattern)
- Modifying existing functionality
- Adding edge-case coverage (boundary values, ambiguous inputs, empty states)
- Any change that could break existing behaviour

When NOT to use: pure configuration changes, documentation updates, or static content additions that have no behavioural impact.

---

## The TDD Cycle

```
    RED                GREEN              REFACTOR
 Write a test    Write minimal code    Clean up the
 that fails  ──→  to make it pass  ──→  implementation  ──→  (repeat)
      │                  │                    │
      ▼                  ▼                    ▼
   Test FAILS        Test PASSES         Tests still PASS
```

### Step 1: RED — Write a Failing Test

Write the test first. It must fail. A test that passes immediately proves nothing.

```python
class TestDataProcessing:
    def test_boundary_input_produces_expected_result(self) -> None:
        # RED: fails because the handler is not yet implemented
        result = process_record(key='edge_case', value=42)
        assert result.status == 'valid'
```

### Step 2: GREEN — Make It Pass

Write the minimum code to make the test pass. Do not over-engineer.

### Step 3: REFACTOR — Clean Up

With tests green, improve the code without changing behaviour:

- Extract shared logic
- Improve naming
- Remove duplication
- Optimize if necessary

Run tests after every refactor step to confirm nothing broke.

---

## The Prove-It Pattern (Bug Fixes)

When a bug is reported, do not start by trying to fix it. Start by writing a test that reproduces it.

```
Bug report arrives
       │
       ▼
  Write a test that demonstrates the bug
       │
       ▼
  Test FAILS (confirming the bug exists)
       │
       ▼
  Implement the fix
       │
       ▼
  Test PASSES (proving the fix works)
       │
       ▼
  Run full test suite (no regressions)
```

When fixing ambiguous interpretation (e.g. a boundary-value edge case), add a test that would fail without the fix.

---

## Test Structure

### Organize in Classes for Related Scenarios

Group related scenarios under a test class. Use descriptive names that read like a specification.

```python
import pytest
from mypackage.core.processor import process_record


class TestRecordProcessing:
    def test_single_record_changes_status(self) -> None:
        result = process_record(...)
        assert result.status == 'valid'

    def test_no_change_detected(self) -> None:
        result = process_record(...)
        assert result.consequence == 'noop'

    def test_boundary_value_handled_correctly(self) -> None:
        ...
```

### Use Fixtures for Reusable Setup

```python
@pytest.fixture
def sample_input(tmp_path):
    infile = tmp_path / 'sample.txt'
    infile.write_text('header\n...')
    return infile
```

Use fixtures for: temporary files, in-memory DBs, minimal project DB setup, and mock external calls.

### Arrange-Act-Assert

Structure every test in three clear phases:

```python
def test_boundary_input_produces_error_sentinel(self) -> None:
    # Arrange
    record = make_record(value='', position=10)

    # Act
    result = process_record(record)

    # Assert
    assert result.status == 'error'
```

---

## Focus Areas

Priority test scenarios, ordered by risk:

### 1. Edge Cases and Boundary Values

- Boundary values — minimum, maximum, off-by-one positions
- Empty inputs and None — graceful handling, not crashes
- Ambiguous states — deterministic resolution or explicit rejection
- Missing fields — fail fast with a clear error
- Concurrent modifications — consistency preserved

### 2. Data Transformation and Validation

- Input validation — malformed data rejected with clear errors
- Coordinate/index conversions — off-by-one and boundary checks
- Format parsing — structural validation before processing
- Normalization — consistent output for equivalent inputs

### 3. Rule Matching and Business Logic

- Single-condition rule: exact match on expected values
- Multi-condition rule: all members must co-occur to fire
- Compound expressions: AND/OR/NOT/XOR evaluated correctly
- Fuzzy matching: similarity scoring for non-exact matches
- Unknown references — skipped with warning, not abort
- Conflicting references — flagged, not silently resolved

### 4. Deterministic Report Exports

- HTML, JSON, and TSV (or other format) outputs are byte-stable across reruns
- Regeneration from stored results produces identical output to original run
- Column hiding and formatting logic is deterministic

### 5. Schema Migrations

- Opening an older database migrates automatically without data loss
- New columns added with correct defaults
- Existing data semantics preserved after migration

---

## Test Sizing

| Size | Resources | Target | Examples |
|---|---|---|---|
| Small | Single process, no I/O | Vast majority | Pure processing logic, rule matching, data walks |
| Medium | Localhost, tmp files, in-memory DB | Integration paths | CLI commands, DB persistence, report export |
| Large | External services | Avoid in CI | Manual only: external API calls |

Mock external services in all automated tests. Use fakes and isolated queues for web-layer test isolation.

---

## Writing Good Tests

### Test Behaviour, Not Implementation

Assert on outcomes. Do not assert on which internal methods were called — that makes tests break during refactoring even when behaviour is unchanged.

```python
# Good: tests what the function produces
assert result.status == 'valid'

# Bad: tests internal call sequence
mock_process.assert_called_once_with(record)
```

### DAMP Over DRY

Each test should tell a complete story. Duplication in tests is acceptable when it makes each test independently readable without tracing shared helpers.

### One Concept Per Test

```python
# Good
def test_rejects_empty_record_name(self): ...
def test_trims_whitespace_from_record_name(self): ...

# Bad
def test_record_name_validation(self):
    # tests both in one — harder to diagnose on failure
```

### Prefer Real Implementations Over Mocks

```
Preference order:
1. Real implementation  → highest confidence
2. Fake                 → in-memory version (e.g. tmp SQLite, fakeredis)
3. Stub                 → canned data, no behaviour
4. Mock (interaction)   → use only at external service boundaries
```

Mock only when the real implementation is slow, non-deterministic, or has uncontrollable side effects (external APIs, file system paths outside tmp).

---

## Test Anti-Patterns to Avoid

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

After completing any implementation:

```
- [ ] Every new behaviour has a corresponding test
- [ ] All tests pass: python -m pytest
- [ ] Bug fixes include a reproduction test that failed before the fix
- [ ] Test names describe the behaviour being verified
- [ ] No tests were skipped or disabled
- [ ] Exception paths are explicit (no silent `except` blocks in touched code)
- [ ] Deterministic outputs remain stable (report/export tests)
- [ ] If a feature was removed, its tests were also removed
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll write tests after the code works" | You won't. Tests written after the fact test implementation, not behaviour. |
| "This is too simple to test" | Simple code gets complicated. The test documents the expected behaviour. |
| "I tested it manually" | Manual testing does not persist. Tomorrow's change may break it silently. |
| "The tests pass, so it's good" | Tests are necessary but not sufficient. They do not catch architecture problems or security issues. |

## Red Flags

- Writing code without any corresponding tests
- Tests that pass on the first run without a failing state first
- Bug fixes without reproduction tests
- Test names that do not describe the expected behaviour
- Skipping tests to make the suite pass
- Removing tests without removing the feature they cover
