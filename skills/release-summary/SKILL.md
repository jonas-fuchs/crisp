---
name: release-summary
description: 'Summarize conceptual changes from the last tag to HEAD as bullet points grouped by category. Use for release notes, understanding branch scope, or reviewing what changed in a release.'
argument-hint: 'Optional: focus area'
user-invocable: true
disable-model-invocation: false
---

# Release Summary

## Overview

Summarize the conceptual changes between the last Git tag and HEAD as a short bulleted report grouped by category. The output is pasted directly into the chat — do not create a file. Focus on what changed conceptually (new features, behaviour changes, removed capabilities, refactors), not on lines of code or file structure.

## When to Use

- Preparing release notes
- Understanding what changed in a feature branch
- Providing context for code review
- Summarizing a release for stakeholders

## Procedure

### 1. Identify the range

```bash
git describe --tags --abbrev=0      # last tag
git rev-parse --abbrev-ref HEAD     # current branch
git log --oneline <tag>..HEAD       # commits in range
```

If no tag exists, use the root commit: `git rev-list --max-parents=0 HEAD`.

### 2. Read the commits

Read each commit message and, where needed for context, the diff summary. Capture the conceptual change in one sentence — what behaviour was added, changed, removed, or restructured. Do not report line counts, file counts, or insertions/deletions.

### 3. Classify each change

Sort each change into one of these categories:

- **New features** — new capability, module, or behaviour
- **Bug fixes** — incorrect behaviour corrected
- **Improvements** — enhancements to existing behaviour (performance, usability, clarity, refactor)

If a change does not fit any category, omit it unless it is a breaking change.

### 4. Synthesize

Merge related commits into a single bullet. One bullet per distinct conceptual change, not per commit. Lead each bullet with what changed, not with the commit hash.

### 5. Flag breaking changes

Identify changes that remove, rename, or alter public interfaces, configuration formats, or documented behaviour. List these explicitly at the end.

## Output Format

Paste this directly into the chat. No emojis. No file creation.

```
Release Summary: <tag> to <branch>

<one or two sentence overview of the release as a whole>

New features:
- <bullet>
- <bullet>

Bug fixes:
- <bullet>
- <bullet>

Improvements:
- <bullet>
- <bullet>

Breaking changes:
- <bullet, or "None">
```

## Guidelines

- Keep it short. A few bullets per category, not an exhaustive list.
- Write for a reader who understands the codebase but has not followed the branch.
- Name the feature, module, or behaviour — do not lead with commit hashes.
- Merge related commits into one bullet. Synthesize, do not enumerate.
- Do not report line counts, file counts, or diff statistics.
- Omit pure cosmetic or churn-only changes unless the user asked for them.

## Integration

The Reviewer agent invokes this skill to understand the scope and conceptual impact of changes before starting the six-axis review. The summary guides which areas deserve deeper attention.