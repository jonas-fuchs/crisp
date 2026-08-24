---
name: release-summary
description: 'Summarize Git changes from the last tag to HEAD, organized by folder. Use for release notes, understanding branch scope, or identifying changed modules.'
argument-hint: 'Optional: focus folder, detail level (brief/standard)'
user-invocable: true
disable-model-invocation: false
---

# Release Summary

## Overview

Analyzes Git history from the last tag to current HEAD and produces a concise summary of changes organized by folder/module.

## When to Use

- Preparing release notes
- Understanding what changed in a feature branch
- Identifying which modules were most affected
- Providing context for code review

## Output

```markdown
# Release Summary: <tag> → HEAD

**Commits**: <n>  **Files**: <n>  **Lines**: +<n> / -<n>

## Changes by Folder

### <folder>/
**Impact**: High/Medium/Low
**Files**: <n>  **Lines**: +<n> / -<n>
**Key commits**:
- <sha>: <message>
- <sha>: <message>

## Notable Changes
- Breaking: <list if any>
- Config: <list if any>
```

## Usage

```bash
# Standard summary
python scripts/release_summary.py

# Focused on folder
python scripts/release_summary.py --focus src/api

# Brief output
python scripts/release_summary.py --detail brief
```

## Integration

Reviewer invokes this skill to understand the scope and impact of changes before starting the six-axis review. Use the folder impact assessment to prioritize review attention.