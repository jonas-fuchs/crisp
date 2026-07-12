---
name: review-change
description: 'Review a completed change before merge. Runs the 6-axis software quality audit plus scientific validation review. Returns APPROVE or CHANGES REQUIRED.'
---

# Review a Change

Use the `software-quality-audit` skill to conduct this review. Delegate to `security-review`, `architecture-audit`, or `reproducibility-audit` if deeper analysis is needed.

## Steps

1. **Understand the context.** Read the TODO.md ticket and the diff summary. What was the goal? Which modules were touched?

2. **Review tests first.**
   - Do tests exist for the change?
   - Do they test behaviour, not implementation details?
   - Are edge cases covered?
   - For scientific code: is validation independent (not derived from the implementation under test)?
   - Are tolerances justified?

3. **Run the 6-axis review.**
   - **Correctness:** Does it match the spec? Are edge cases and error paths handled?
   - **Readability:** Are names clear? Is control flow straightforward? No dead code?
   - **Architecture:** Does it respect module boundaries? Any circular dependencies? Unnecessary duplication?
   - **Security:** Is input validated? SQL parameterised? Paths confined? Secrets out of code?
   - **Performance:** Any N+1 queries? Unbounded loops? Python loops that should be vectorised?
   - **Cleanup:** Dead code, stale comments, magic numbers, one-off helpers?

4. **Check scientific validity** (if applicable).
   - Is there an independent validation source?
   - Are units, shapes, and dtypes consistent with the scientific contract?
   - Are random seeds pinned for stochastic code?
   - Is the Git commit recorded for reproducibility?

5. **Run the review checklist.** Validate each axis with the checklist from the `software-quality-audit` skill.

6. **Categorize findings.**
   - Critical: blocks merge
   - Required: must address before merge
   - Nit: optional
   - Suggestion: worth considering

7. **Return verdict.**

```
## Review Summary

**Verdict:** APPROVE | CHANGES REQUIRED

**Overview:** [1-2 sentence assessment]

### Critical Issues
- [file] [finding and fix]

### Required Changes
- [file] [finding and fix]

### Cleanup Findings
- [rule tag] [file] [finding]

### Suggestions
- [file] [suggestion]

### What's Done Well
- [positive observation]

### Verification
- Tests reviewed: [yes/no]
- Scientific validation: [yes/no/n/a]
- Security checked: [yes/no]
- Deterministic output: [yes/no/n/a]
```

Do not modify any files. Return the verdict only.
