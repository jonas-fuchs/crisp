#!/usr/bin/env python3
"""
Validate CRISP customizations for VS Code Copilot.

Checks:
1. YAML frontmatter parses in all agent, skill, and prompt files
2. Skill names match their directory names
3. Referenced agents exist (agent handoffs point to real .agent.md files)
4. Tool names are valid (no deprecated 'todo' — should be 'todos')
5. Literature/research agents have 'web' tool access
6. Markdown links in skill files resolve to existing files
7. Skill descriptions are sufficiently distinct from each other
8. Instruction files have .instructions.md extension and an applyTo rule
9. Installation manifest references only existing files
10. Agent/skill/prompt file naming conventions are followed

Usage:
    python scripts/validate_customizations.py [--root PATH]

Exit code 0 = all checks passed, 1 = one or more failures.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print('ERROR: PyYAML is required. Install with: pip install pyyaml')
    sys.exit(1)


# --- Configuration ----------------------------------------------------------

VALID_TOOLS = {'read', 'search', 'edit', 'execute', 'todos', 'web', 'agent'}
DEPRECATED_TOOLS = {'todo'}

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


# --- Helpers ----------------------------------------------------------------

def parse_frontmatter(filepath: Path) -> dict | None:
    """Parse YAML frontmatter from a markdown file. Returns None if missing or invalid."""
    text = filepath.read_text(encoding='utf-8')
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def find_files(root: Path, pattern: str) -> list[Path]:
    """Find all files matching a glob pattern, sorted."""
    return sorted(root.rglob(pattern))


class CheckResult:
    """Accumulator for validation results."""

    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def report(self) -> None:
        if self.warnings:
            for w in self.warnings:
                print(f'  WARN: {w}')
        if self.errors:
            for e in self.errors:
                print(f'  FAIL: {e}')
        else:
            print('  PASS')


# --- Checks -----------------------------------------------------------------

def check_frontmatter(result: CheckResult, files: list[Path], label: str) -> list[tuple[Path, dict]]:
    """Check that all files have parseable YAML frontmatter. Return (path, frontmatter) pairs."""
    parsed = []
    for f in files:
        fm = parse_frontmatter(f)
        if fm is None:
            result.error(f'{label} {f.name}: missing or invalid YAML frontmatter')
        else:
            parsed.append((f, fm))
    return parsed


def check_skill_names(result: CheckResult, skills: list[Path]) -> None:
    """Skill directory name must match the 'name' field in frontmatter."""
    for f in skills:
        fm = parse_frontmatter(f)
        if fm is None:
            return  # already reported by check_frontmatter
        name = fm.get('name', '')
        dir_name = f.parent.name
        if name != dir_name:
            result.error(
                f'skill {f}: name="{name}" does not match directory "{dir_name}"'
            )


def check_agent_handoffs(result: CheckResult, agents: list[Path], root: Path) -> None:
    """Agent handoffs must reference existing agents by name or file stem."""
    agent_names = {f.stem.replace('.agent', '') for f in agents}
    # Also collect frontmatter 'name' fields
    frontmatter_names = set()
    for f in agents:
        fm = parse_frontmatter(f)
        if fm:
            frontmatter_names.add(fm.get('name', ''))
    all_known = agent_names | frontmatter_names

    for f in agents:
        fm = parse_frontmatter(f)
        if fm is None:
            return
        handoffs = fm.get('handoffs', [])
        if not handoffs:
            continue
        if isinstance(handoffs, dict):
            handoffs = [handoffs]
        for h in handoffs:
            if isinstance(h, dict):
                agent_ref = h.get('agent', '')
                if agent_ref and agent_ref not in all_known:
                    result.error(
                        f'agent {f.name}: handoff references unknown agent "{agent_ref}"'
                    )


def check_tool_names(result: CheckResult, agents: list[Path]) -> None:
    """Tool names must be valid and not use deprecated names."""
    for f in agents:
        fm = parse_frontmatter(f)
        if fm is None:
            return
        tools = fm.get('tools', [])
        if isinstance(tools, str):
            tools = [t.strip() for t in tools.split(',')]
        for tool in tools:
            if tool in DEPRECATED_TOOLS:
                result.error(
                    f'agent {f.name}: uses deprecated tool "{tool}" — use "todos" instead'
                )
            elif tool not in VALID_TOOLS:
                result.warn(
                    f'agent {f.name}: unknown tool "{tool}" — may not be recognized by VS Code'
                )


def check_web_access(result: CheckResult, agents: list[Path]) -> None:
    """Agents doing literature research must have 'web' tool access."""
    for f in agents:
        fm = parse_frontmatter(f)
        if fm is None:
            return
        name = fm.get('name', '')
        desc = fm.get('description', '')
        tools = fm.get('tools', [])
        if isinstance(tools, str):
            tools = [t.strip() for t in tools.split(',')]
        # Check for research/literature agents
        keywords = ['research', 'literature', 'scientific research', 'bioinformatics']
        if any(kw in name.lower() or kw in desc.lower() for kw in keywords):
            if 'web' not in tools:
                result.error(
                    f'agent {f.name}: research/literature agent lacks "web" tool access'
                )


def check_markdown_links(result: CheckResult, files: list[Path], root: Path) -> None:
    """Relative markdown links in skill files should resolve to existing files."""
    link_re = re.compile(r'\[@[^\]]+\]\(([^)]+)\)|\[([^\]]+)\]\(([^)]+)\)')
    for f in files:
        text = f.read_text(encoding='utf-8')
        for match in link_re.finditer(text):
            link = match.group(1) or match.group(3)
            if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
                continue
            # Resolve relative to the file's directory
            resolved = (f.parent / link).resolve()
            if not resolved.exists():
                result.warn(
                    f'{f.name}: link "{link}" does not resolve to an existing file'
                )


def check_skill_descriptions(result: CheckResult, skills: list[Path]) -> None:
    """Skill descriptions should be sufficiently distinct (not near-duplicates)."""
    desc_map: dict[str, str] = {}
    for f in skills:
        fm = parse_frontmatter(f)
        if fm is None:
            return
        desc = fm.get('description', '')
        if not desc:
            result.warn(f'skill {f.name}: missing description')
            continue
        # Check for near-duplicate descriptions (first 50 chars)
        prefix = desc.strip().lower()[:50]
        for existing_name, existing_prefix in desc_map.items():
            if prefix == existing_prefix:
                result.warn(
                    f'skills "{f.parent.name}" and "{existing_name}" have very similar descriptions'
                )
        desc_map[f.parent.name] = prefix


def check_instruction_files(result: CheckResult, root: Path) -> None:
    """Instruction files must have .instructions.md extension and applyTo rule."""
    instr_dir = root / 'instructions'
    if not instr_dir.exists():
        result.error('instructions/ directory not found')
        return

    for f in sorted(instr_dir.iterdir()):
        if f.is_dir():
            continue
        if not f.name.endswith('.instructions.md'):
            result.error(f'instruction file {f.name}: must end with .instructions.md')
            continue
        fm = parse_frontmatter(f)
        if fm is None:
            result.error(f'instruction file {f.name}: missing or invalid frontmatter')
            continue
        apply_to = fm.get('applyTo')
        if not apply_to:
            result.error(f'instruction file {f.name}: missing "applyTo" field')


def check_manifest(result: CheckResult, root: Path) -> None:
    """Check that all files referenced in the install manifest exist."""
    manifest_path = root / 'scripts' / 'install.sh'
    if not manifest_path.exists():
        result.warn('scripts/install.sh not found — cannot validate manifest')
        return

    text = manifest_path.read_text(encoding='utf-8')
    # Extract manifest entries: "source:target" pairs
    entry_re = re.compile(r'"([^"]+):([^"]+)"')
    in_manifest = False
    for line in text.splitlines():
        if 'MANIFEST=(' in line:
            in_manifest = True
        if in_manifest:
            for match in entry_re.finditer(line):
                source_rel = match.group(1)
                source = root / source_rel
                if not source.exists():
                    result.error(f'manifest references missing file: {source_rel}')
        if in_manifest and line.strip() == ')':
            in_manifest = False


def check_naming_conventions(result: CheckResult, agents: list[Path], skills: list[Path], prompts: list[Path]) -> None:
    """Check that files follow naming conventions."""
    for f in agents:
        if not f.name.endswith('.agent.md'):
            result.error(f'agent file {f.name}: must end with .agent.md')
    for f in skills:
        if f.name != 'SKILL.md':
            result.error(f'skill file {f.name}: must be named SKILL.md')
    for f in prompts:
        if not f.name.endswith('.prompt.md'):
            result.error(f'prompt file {f.name}: must end with .prompt.md')


# --- Main -------------------------------------------------------------------

def main() -> int:
    root = Path(sys.argv[sys.argv.index('--root') + 1]) if '--root' in sys.argv else Path(__file__).resolve().parent.parent

    print(f'Validating CRISP customizations at: {root}')
    print()

    agents = find_files(root / 'agents', '*.agent.md') if (root / 'agents').exists() else []
    skills = find_files(root / 'skills' / '*', 'SKILL.md') if (root / 'skills').exists() else []
    # Also find skills in subdirectories
    skills = sorted(set(skills + [f for f in (root / 'skills').rglob('SKILL.md') if f.is_file()])) if (root / 'skills').exists() else []
    prompts = find_files(root / 'prompts', '*.prompt.md') if (root / 'prompts').exists() else []
    instructions = sorted((root / 'instructions').glob('*.instructions.md')) if (root / 'instructions').exists() else []

    print(f'Found: {len(agents)} agents, {len(skills)} skills, {len(prompts)} prompts, {len(instructions)} instruction files')
    print()

    all_ok = True

    # 1. Frontmatter
    print('1. YAML frontmatter parsing')
    r = CheckResult()
    check_frontmatter(r, agents, 'agent')
    check_frontmatter(r, skills, 'skill')
    check_frontmatter(r, prompts, 'prompt')
    r.report()
    all_ok &= r.ok

    # 2. Skill names match directories
    print('2. Skill names match directory names')
    r = CheckResult()
    check_skill_names(r, skills)
    r.report()
    all_ok &= r.ok

    # 3. Agent handoffs reference existing agents
    print('3. Agent handoff references')
    r = CheckResult()
    check_agent_handoffs(r, agents, root)
    r.report()
    all_ok &= r.ok

    # 4. Tool names valid
    print('4. Agent tool names')
    r = CheckResult()
    check_tool_names(r, agents)
    r.report()
    all_ok &= r.ok

    # 5. Web access for research agents
    print('5. Web access for research agents')
    r = CheckResult()
    check_web_access(r, agents)
    r.report()
    all_ok &= r.ok

    # 6. Markdown links resolve
    print('6. Markdown link resolution')
    r = CheckResult()
    check_markdown_links(r, skills, root)
    check_markdown_links(r, agents, root)
    r.report()
    all_ok &= r.ok

    # 7. Skill descriptions distinct
    print('7. Skill description distinctness')
    r = CheckResult()
    check_skill_descriptions(r, skills)
    r.report()
    all_ok &= r.ok

    # 8. Instruction files
    print('8. Instruction file conventions')
    r = CheckResult()
    check_instruction_files(r, root)
    r.report()
    all_ok &= r.ok

    # 9. Manifest
    print('9. Install manifest references')
    r = CheckResult()
    check_manifest(r, root)
    r.report()
    all_ok &= r.ok

    # 10. Naming conventions
    print('10. File naming conventions')
    r = CheckResult()
    check_naming_conventions(r, agents, skills, prompts)
    r.report()
    all_ok &= r.ok

    print()
    if all_ok:
        print('✅ All checks passed.')
        return 0
    else:
        print('❌ One or more checks failed. See above.')
        return 1


if __name__ == '__main__':
    sys.exit(main())
