---
name: prepare-pr
description: 'Prepare a pull request from completed work. Summarizes the change, lists affected files, runs final validation, and produces a PR description.'
---

# Prepare a Pull Request

## Steps

1. **Summarize the change.** Read the diff and the relevant TODO.md ticket. Write a 1-2 sentence summary of what changed and why.

2. **List affected files.** Group by category:
   - Source files changed
   - Test files changed or added
   - Configuration changes
   - Documentation changes

3. **Run final validation.**
   - Discover and run the canonical test command for the repository (check justfile, pyproject.toml, CI config, or README for the command — do not assume).
   - Confirm all tests pass.
   - For scientific code: confirm that validation is independent and tolerances are justified.
   - For report/export code: confirm output is deterministic.

4. **Check completeness.**
   - TODO.md updated in the same change?
   - Documentation updated if behaviour changed?
   - No dead code, stale imports, or commented-out blocks?
   - No secrets or internal paths in error messages?

5. **Generate PR description.**

```
## Summary

[1-2 sentence summary]

## Changes

- [category]: [file — what changed]
- ...

## Validation

- Tests: [command run, result]
- Scientific validation: [source used, tolerance, pass/fail]
- Deterministic output: [yes/no, verified by]

## Checklist

- [ ] TODO.md updated
- [ ] Documentation updated
- [ ] No dead code introduced
- [ ] No secrets in error messages or logs
- [ ] All tests pass
```

6. **Present** the PR description. Do not create the PR unless asked.
