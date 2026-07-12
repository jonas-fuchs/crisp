#!/usr/bin/env bash
#
# CRISP — Copilot Research Infrastructure for Scientific Python
# Deterministic installer for VS Code Copilot customizations.
#
# Usage:
#   ./scripts/install.sh              Install (copy) all customizations
#   ./scripts/install.sh --dry-run    Show what would be installed without copying
#   ./scripts/install.sh --backup     Backup existing files before installing
#   ./scripts/install.sh --link       Symlink instead of copy (for active development)
#   ./scripts/install.sh --uninstall  Remove all installed customizations
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${CRISP_TARGET:-$HOME/.copilot}"

# --- Manifest ---------------------------------------------------------------
# Each line: <source relative path>:<target relative path>
# Files are installed from SOURCE_DIR to TARGET_DIR preserving structure.
MANIFEST=(
    "instructions/general.instructions.md:instructions/general.instructions.md"
    "instructions/python.instructions.md:instructions/python.instructions.md"
    "instructions/tests.instructions.md:instructions/tests.instructions.md"
    "instructions/scientific.instructions.md:instructions/scientific.instructions.md"
    "agents/builder.agent.md:agents/builder.agent.md"
    "agents/scientific-reviewer.agent.md:agents/scientific-reviewer.agent.md"
    "agents/researcher.agent.md:agents/researcher.agent.md"
    "skills/scientific-testing/SKILL.md:skills/scientific-testing/SKILL.md"
    "skills/software-quality-audit/SKILL.md:skills/software-quality-audit/SKILL.md"
    "skills/architecture-audit/SKILL.md:skills/architecture-audit/SKILL.md"
    "skills/security-review/SKILL.md:skills/security-review/SKILL.md"
    "skills/reproducibility-audit/SKILL.md:skills/reproducibility-audit/SKILL.md"
    "skills/scientific-validation/SKILL.md:skills/scientific-validation/SKILL.md"
    "skills/grill-me/SKILL.md:skills/grill-me/SKILL.md"
    "skills/delivery-planning/SKILL.md:skills/delivery-planning/SKILL.md"
    "skills/diagnose/SKILL.md:skills/diagnose/SKILL.md"
    "skills/profiling/SKILL.md:skills/profiling/SKILL.md"
    "skills/graphify/SKILL.md:skills/graphify/SKILL.md"
    "prompts/plan-change.prompt.md:prompts/plan-change.prompt.md"
    "prompts/prepare-pr.prompt.md:prompts/prepare-pr.prompt.md"
    "prompts/reproduce-result.prompt.md:prompts/reproduce-result.prompt.md"
    "prompts/review-change.prompt.md:prompts/review-change.prompt.md"
    "templates/SCIENTIFIC_CONTRACT.md:templates/SCIENTIFIC_CONTRACT.md"
    "templates/TODO.md:templates/TODO.md"
)

# --- Flags ------------------------------------------------------------------
DRY_RUN=false
BACKUP=false
LINK=false
UNINSTALL=false

for arg in "$@"; do
    case "$arg" in
        --dry-run)    DRY_RUN=true ;;
        --backup)     BACKUP=true ;;
        --link)       LINK=true ;;
        --uninstall)  UNINSTALL=true ;;
        --help|-h)
            grep '^#' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *)
            echo "Unknown flag: $arg" >&2
            echo "Run with --help for usage." >&2
            exit 1
            ;;
    esac
done

# --- Uninstall --------------------------------------------------------------
if $UNINSTALL; then
    echo "Uninstalling CRISP customizations from $TARGET_DIR ..."
    for entry in "${MANIFEST[@]}"; do
        target_rel="${entry##*:}"
        target="$TARGET_DIR/$target_rel"
        if [[ -e "$target" || -L "$target" ]]; then
            $DRY_RUN && echo "  [dry-run] rm $target" || rm -f "$target"
            # Remove empty parent directories (best effort)
            $DRY_RUN || rmdir "$(dirname "$target")" 2>/dev/null || true
        fi
    done
    echo "Uninstall complete."
    exit 0
fi

# --- Install ----------------------------------------------------------------
installed=0
skipped=0

echo "Installing CRISP customizations to $TARGET_DIR ..."
$LINK && echo "  (symlink mode)" || echo "  (copy mode)"
$DRY_RUN && echo "  (dry run — no files will be written)"

for entry in "${MANIFEST[@]}"; do
    source_rel="${entry%%:*}"
    target_rel="${entry##*:}"
    source="$SOURCE_DIR/$source_rel"
    target="$TARGET_DIR/$target_rel"

    if [[ ! -f "$source" ]]; then
        echo "  WARN: source missing: $source" >&2
        ((skipped++))
        continue
    fi

    # Backup if requested and target exists
    if $BACKUP && [[ -e "$target" && ! -L "$target" ]] && ! $DRY_RUN; then
        backup="${target}.bak.$(date +%Y%m%d%H%M%S)"
        cp "$target" "$backup"
        echo "  backup: $target → $backup"
    fi

    # Create parent directory
    if ! $DRY_RUN; then
        mkdir -p "$(dirname "$target")"
    fi

    if $LINK; then
        if $DRY_RUN; then
            echo "  [dry-run] ln -sf $source $target"
        else
            ln -sf "$source" "$target"
        fi
    else
        if $DRY_RUN; then
            echo "  [dry-run] cp $source $target"
        else
            cp "$source" "$target"
        fi
    fi
    ((installed++))
done

echo "Done: $installed files $(${LINK} && echo 'linked' || echo 'copied'), $skipped skipped."
$DRY_RUN && echo "(dry run — nothing was actually changed)"
