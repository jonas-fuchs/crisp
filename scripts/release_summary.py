#!/usr/bin/env python3
"""
Simple release summary: changes from last tag to HEAD, grouped by folder.
"""

import subprocess
import re
from collections import defaultdict


def git(*args):
    """Run git command and return stdout."""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_last_tag():
    """Get last tag or root commit."""
    tag = git("describe", "--tags", "--abbrev=0")
    if not tag:
        tag = git("rev-list", "--max-parents=0", "HEAD")
    return tag


def classify_commit(msg):
    """Classify commit type."""
    if re.search(r"^(feat|feature|add|implement)", msg, re.I):
        return "Feature"
    if re.search(r"^(fix|bugfix|patch|resolve)", msg, re.I):
        return "Fix"
    if re.search(r"^(refactor|clean|restructure)", msg, re.I):
        return "Refactor"
    if re.search(r"^(test|spec)", msg, re.I):
        return "Test"
    return "Other"


def main():
    since = get_last_tag()
    head = git("rev-parse", "HEAD")[:7]
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    
    # Basic stats
    commits = git("rev-list", "--count", f"{since}..HEAD")
    diff_stat = git("diff", "--shortstat", f"{since}..HEAD")
    
    # Parse line changes
    ins = re.search(r"(\d+) insertion", diff_stat)
    dels = re.search(r"(\d+) deletion", diff_stat)
    ins_count = ins.group(1) if ins else "0"
    dels_count = dels.group(1) if dels else "0"
    
    # Folder stats
    folders = defaultdict(lambda: {"files": 0, "ins": 0, "dels": 0, "commits": []})
    
    # Get all changed files with stats
    diff_output = git("diff", "--numstat", f"{since}..HEAD")
    for line in diff_output.split("\n"):
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 3:
            ins_val = 0 if parts[0] == "-" else int(parts[0])
            del_val = 0 if parts[1] == "-" else int(parts[1])
            filepath = parts[2]
            
            # Get top-level folder
            folder = filepath.split("/")[0] if "/" in filepath else "."
            folders[folder]["files"] += 1
            folders[folder]["ins"] += ins_val
            folders[folder]["dels"] += del_val
    
    # Get commits per folder
    log_output = git("log", "--oneline", f"{since}..HEAD")
    for line in log_output.split("\n"):
        if not line:
            continue
        sha = line.split()[0]
        msg = line[len(sha)+1:]
        
        # Find which folders this commit touches
        files = git("diff-tree", "--no-commit-id", "--name-only", "-r", sha)
        for filepath in files.split("\n"):
            if filepath:
                folder = filepath.split("/")[0] if "/" in filepath else "."
                if sha not in folders[folder]["commits"]:
                    folders[folder]["commits"].append(f"{sha}: {msg}")
    
    # Print summary
    print(f"# Release Summary: {since} → {branch}")
    print(f"\n**Commits**: {commits}  **Files**: {len(folders)}  **Lines**: +{ins_count} / -{dels_count}\n")
    print("## Changes by Folder\n")
    
    # Sort by files changed
    for folder in sorted(folders.keys(), key=lambda f: folders[f]["files"], reverse=True):
        stats = folders[folder]
        impact = "High" if stats["files"] > 10 else "Medium" if stats["files"] > 3 else "Low"
        
        print(f"### {folder}/")
        print(f"**Impact**: {impact}")
        print(f"**Files**: {stats['files']}  **Lines**: +{stats['ins']} / -{stats['dels']}")
        print("**Key commits**:")
        for commit in stats["commits"][:3]:
            print(f"- {commit}")
        print()
    
    # Check for breaking changes
    breaking = git("log", "--grep=breaking", "--oneline", f"{since}..HEAD")
    if breaking:
        print("## ⚠ Breaking Changes\n")
        for line in breaking.split("\n"):
            if line:
                print(f"- {line}")
        print()


if __name__ == "__main__":
    main()