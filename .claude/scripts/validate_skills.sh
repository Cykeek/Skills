#!/usr/bin/env bash
# validate_skills.sh - Shell-based validation for skills library
# Usage: ./validate_skills.sh [domain] [skill]
# Can run without Python - uses grep, find, awk

set -euo pipefail

SKILLS_ROOT="${1:-.claude/skills}"
DOMAIN_FILTER="${2:-}"
SKILL_FILTER="${3:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0
CHECKED=0

log_error() {
    echo -e "${RED}❌ $1${NC}"
    ((ERRORS++)) || true
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++)) || true
}

log_ok() {
    echo -e "${GREEN}✅ $1${NC}"
}

check_frontmatter() {
    local skill_md="$1"
    local skill_path="$2"

    # Check frontmatter exists
    if ! head -1 "$skill_md" | grep -q "^---$"; then
        log_error "$skill_path: Missing frontmatter (must start with ---)"
        return 1
    fi

    # Extract frontmatter
    local fm=$(sed -n '1,/^---$/p' "$skill_md" | head -n -1 | tail -n +2)

    # Check name field
    if ! echo "$fm" | grep -q "^name:"; then
        log_error "$skill_path: Frontmatter missing 'name' field"
    else
        local name=$(echo "$fm" | grep "^name:" | cut -d' ' -f2-)
        if ! echo "$name" | grep -qE '^[a-z0-9-]+$'; then
            log_error "$skill_path: Skill name must be kebab-case: '$name'"
        fi
    fi

    # Check description field
    if ! echo "$fm" | grep -q "^description:"; then
        log_error "$skill_path: Frontmatter missing 'description' field"
    else
        local desc=$(echo "$fm" | sed -n '/^description:/,/^[a-z]*:/p' | head -n -1 | sed 's/^description: *//')
        if ! echo "$desc" | grep -qiE '(Use when|Use for)'; then
            log_error "$skill_path: Description must contain 'Use when' or 'Use for' trigger phrase"
        fi
        if [ ${#desc} -gt 300 ]; then
            log_warn "$skill_path: Description exceeds 300 chars (${#desc})"
        fi
    fi
}

check_structure() {
    local skill_dir="$1"
    local skill_name=$(basename "$skill_dir")

    # Required directories
    for dir in scripts references assets; do
        if [ ! -d "$skill_dir/$dir" ]; then
            log_warn "$skill_name: Missing directory: $dir/"
        fi
    done

    # SKILL.md exists
    if [ ! -f "$skill_dir/SKILL.md" ]; then
        log_error "$skill_name: Missing SKILL.md"
        return 1
    fi

    # Check line count
    local lines=$(wc -l < "$skill_dir/SKILL.md")
    if [ "$lines" -gt 500 ]; then
        log_error "$skill_name: SKILL.md exceeds 500 lines ($lines)"
    fi

    # Check file size
    local size=$(stat -c%s "$skill_dir/SKILL.md" 2>/dev/null || stat -f%z "$skill_dir/SKILL.md")
    if [ "$size" -gt 10240 ]; then
        log_warn "$skill_name: SKILL.md exceeds 10KB ($size bytes)"
    fi
}

check_em_dashes() {
    local skill_md="$1"
    local skill_path="$2"

    # Check for em dashes outside code blocks
    local in_code=0
    local line_num=0
    while IFS= read -r line; do
        ((line_num++))
        if echo "$line" | grep -q '^```'; then
            in_code=$((1 - in_code))
            continue
        fi
        if [ $in_code -eq 0 ] && echo "$line" | grep -q '—'; then
            # Skip frontmatter area
            if [ $line_num -gt 20 ]; then
                log_error "$skill_path: Line $line_num contains em dash (—) in prose"
            fi
        fi
    done < "$skill_md"
}

check_required_sections() {
    local skill_md="$1"
    local skill_path="$2"

    local required=(
        "Anti-Patterns"
        "Short-Circuit"
        "Related Skills"
        "Reference Files"
        "Quality Loop"
    )

    for section in "${required[@]}"; do
        if ! grep -qiE "##.*$section" "$skill_md"; then
            log_error "$skill_path: Missing required section: $section"
        fi
    done
}

check_related_skills_table() {
    local skill_md="$1"
    local skill_path="$2"

    # Find Related Skills table
    local table=$(sed -n '/##.*Related Skills/,/^## /p' "$skill_md" | head -n -1)

    if [ -z "$table" ]; then
        log_error "$skill_path: Related Skills table not found"
        return
    fi

    # Count rows (excluding header and separator)
    local rows=$(echo "$table" | grep '^|' | grep -v '^|[- ]*|' | wc -l)
    if [ "$rows" -lt 3 ]; then
        log_warn "$skill_path: Related Skills table has only $rows entries (recommended: 3-7)"
    elif [ "$rows" -gt 7 ]; then
        log_warn "$skill_path: Related Skills table has $rows entries (recommended: max 7)"
    fi

    # Check each row has when/when-not
    while IFS= read -r row; do
        if echo "$row" | grep -q '^|' && ! echo "$row" | grep -q '^|[- ]*|'; then
            local cols=$(echo "$row" | sed 's/^|//;s/|$//' | tr '|' '\n' | wc -l)
            if [ "$cols" -lt 3 ]; then
                log_warn "$skill_path: Related Skills row missing columns: $row"
            fi
        fi
    done <<< "$table"
}

check_references() {
    local skill_dir="$1"
    local skill_md="$2"
    local skill_path="$3"

    local refs_dir="$skill_dir/references"
    if [ ! -d "$refs_dir" ]; then
        log_warn "$skill_path: No references/ directory"
        return
    fi

    # Get actual reference files
    local actual_refs=$(find "$refs_dir" -name "*.md" -exec basename {} \; | sort)

    # Get listed references from SKILL.md
    local listed_refs=$(grep -A 20 'Reference Files Index' "$skill_md" | grep '`.*\.md`' | sed 's/.*`\([^`]*\)`.*/\1/' | sort -u)

    # Check for unlisted files
    for ref in $actual_refs; do
        if ! echo "$listed_refs" | grep -qx "$ref"; then
            log_warn "$skill_path: Reference file not in index: $ref"
        fi
    done

    # Check for missing files
    for ref in $listed_refs; do
        if [ ! -f "$refs_dir/$ref" ]; then
            log_warn "$skill_path: Listed reference file missing: $ref"
        fi
    done
}

check_scripts() {
    local skill_dir="$1"
    local skill_path="$2"

    local scripts_dir="$skill_dir/scripts"
    if [ ! -d "$scripts_dir" ]; then
        return
    fi

    for script in "$scripts_dir"/*.py; do
        [ -f "$script" ] || continue
        local script_name=$(basename "$script")

        # Check shebang
        if ! head -1 "$script" | grep -q '^#!/usr/bin/env python3'; then
            log_warn "$skill_path: $script_name missing python3 shebang"
        fi

        # Check for argparse
        if ! grep -q 'argparse' "$script"; then
            log_warn "$skill_path: $script_name: No argparse (CLI interface recommended)"
        fi

        # Check for JSON output
        if ! grep -q 'json.dumps\|print(json' "$script"; then
            log_warn "$skill_path: $script_name: No JSON output detected"
        fi

        # Check for non-stdlib imports
        local imports=$(grep -E '^(from|import) ' "$script" | sed -E 's/^(from|import) +([a-zA-Z_][a-zA-Z0-9_]*).*/\2/' | sort -u)
        local stdlib="argparse json sys os pathlib typing re datetime collections itertools functools subprocess tempfile hashlib uuid dataclasses"

        for imp in $imports; do
            if ! echo "$stdlib" | grep -qw "$imp" && ! [[ "$imp" =~ ^_ ]] && [ ! -f "$scripts_dir/$imp.py" ] && [ ! -d "$scripts_dir/$imp" ]; then
                log_warn "$skill_path: $script_name: Possible non-stdlib import: $imp"
            fi
        done

        # Syntax check (requires python)
        if command -v python3 >/dev/null 2>&1; then
            if ! python3 -m py_compile "$script" 2>/dev/null; then
                log_error "$skill_path: $script_name: Syntax error"
            fi
        fi
    done
}

validate_skill() {
    local skill_dir="$1"
    local skill_name=$(basename "$skill_dir")
    local domain_name=$(basename "$(dirname "$skill_dir")")
    local skill_path="$domain_name/$skill_name"
    local skill_md="$skill_dir/SKILL.md"

    ((CHECKED++)) || true
    echo "Checking $skill_path..."

    check_structure "$skill_dir" || true
    check_frontmatter "$skill_md" "$skill_path" || true
    check_em_dashes "$skill_md" "$skill_path" || true
    check_required_sections "$skill_md" "$skill_path" || true
    check_related_skills_table "$skill_md" "$skill_path" || true
    check_references "$skill_dir" "$skill_md" "$skill_path" || true
    check_scripts "$skill_dir" "$skill_path" || true
}

main() {
    echo "=== Skills Library Validation ==="
    echo "Root: $SKILLS_ROOT"
    echo ""

    if [ ! -d "$SKILLS_ROOT" ]; then
        echo "Error: Skills root not found: $SKILLS_ROOT"
        exit 1
    fi

    # Find all skills
    local skills=()
    for domain in "$SKILLS_ROOT"/*/; do
        local domain_name=$(basename "$domain")
        [ "$domain_name" = "templates" ] && continue
        [ "$domain_name" = "standards" ] && continue
        [ -n "$DOMAIN_FILTER" ] && [ "$domain_name" != "$DOMAIN_FILTER" ] && continue

        for skill in "$domain"*/; do
            [ -d "$skill" ] || continue
            [ -f "$skill/SKILL.md" ] || continue
            local skill_name=$(basename "$skill")
            [ -n "$SKILL_FILTER" ] && [ "$skill_name" != "$SKILL_FILTER" ] && continue
            skills+=("$skill")
        done
    done

    if [ ${#skills[@]} -eq 0 ]; then
        echo "No skills found matching criteria"
        exit 0
    fi

    echo "Found ${#skills[@]} skill(s)"
    echo ""

    for skill in "${skills[@]}"; do
        validate_skill "$skill"
    done

    echo ""
    echo "=== Summary ==="
    echo "Checked: $CHECKED skills"
    echo "Errors: $ERRORS"
    echo "Warnings: $WARNINGS"

    if [ $ERRORS -gt 0 ]; then
        exit 1
    fi
}

main "$@"