---
name: release-summary
description: 'Summarize conceptual changes from the last tag to HEAD, organized by folder. Use for release notes, understanding branch scope, or reviewing what changed in a release.'
argument-hint: 'Optional: focus folder'
user-invocable: true
disable-model-invocation: false
---

# Release Summary

## Overview

Summarize the conceptual changes between the last Git tag and HEAD, organized by folder. The output is pasted directly into the chat — do not create a file. Focus on what changed conceptually (new features, behaviour changes, removed capabilities, refactors), not on lines of code.

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

### 2. Group commits by folder

For each commit, determine which top-level folders it touches:

```bash
git diff-tree --no-commit-id --name-only -r <sha>
```

Group commits under their primary folder. A commit touching multiple folders appears under each.

### 3. Extract the conceptual change per commit

For each commit, read the message and the diff summary. Capture the conceptual change in one sentence — what behaviour was added, changed, removed, or restructured. Do not report line counts, file counts, or insertions/deletions.

Classify each change as one of:

- **Added** — new capability, module, or behaviour
- **Changed** — existing behaviour modified
- **Removed** — capability, file, or behaviour deleted
- **Fixed** — bug or incorrect behaviour corrected
- **Refactor** — internal restructuring with no behaviour change

### 4. Summarize per folder

For each folder, synthesize the commits into a short paragraph describing the main conceptual changes. Lead with the most significant change. If a folder has only trivial changes (e.g. config tweaks), say so in one line.

### 5. Flag breaking changes

Identify commits that remove, rename, or change public interfaces, configuration formats, or documented behaviour. List these explicitly at the end.

## Output Format

Paste this directly into the chat. No emojis. No file creation.

```
Release Summary: <tag> to <branch>

<one or two sentence overview of the release as a whole>

Changes by folder

<folder>/
<short paragraph describing the main conceptual changes>

<folder>/
<short paragraph describing the main conceptual changes>

Breaking changes
- <description, or "None">
```

## Guidelines

- Keep it short. One paragraph per folder, two to four sentences.
- Write for a reader who understands the codebase but has not followed the branch.
- Prefer concrete nouns over commit hashes. Name the feature, module, or behaviour.
- Omit folders with only cosmetic changes unless the user asked for them.
- Do not list every commit. Synthesize.
- Do not report line counts, file counts, or diff statistics.

## Integration

The Reviewer agent invokes this skill to understand the scope and conceptual impact of changes before starting the six-axis review. The per-folder summary guides which modules deserve deeper attention.