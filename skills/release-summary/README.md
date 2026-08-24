# Release Summary

Simple Git release summary: changes from last tag to HEAD, grouped by folder.

## Usage

```bash
# Standard summary
python scripts/release_summary.py

# Output example:
# Release Summary: v1.2.0 → main
# 
# **Commits**: 15  **Files**: 8  **Lines**: +847 / -234
# 
# ## Changes by Folder
# 
# ### src/api/
# **Impact**: High
# **Files**: 12  **Lines**: +523 / -89
# **Key commits**:
# - a3f7b2c: Implement new authentication flow
# - b8e4d1a: Add rate limiting middleware
```

## Integration

The Reviewer agent can invoke this skill to understand the scope and impact of changes before starting the six-axis review.

## Output

- **Commits**: Total number since last tag
- **Files**: Number of folders with changes
- **Lines**: Total insertions/deletions
- **Per folder**: Impact level (High/Medium/Low), file count, line changes, key commits
- **Breaking changes**: Flagged if any commits mention "breaking"