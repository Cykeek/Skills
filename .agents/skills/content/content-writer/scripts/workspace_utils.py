#!/usr/bin/env python3
"""
Workspace Utilities for Skills
==============================
Provides workspace detection and standardized output folder management
for all skills in the AI-Workflows system.

Usage in skill scripts:
    from workspace_utils import get_skill_output_dir, create_task_dir

    output_dir = get_skill_output_dir("my-skill")
    task_dir = create_task_dir("my-skill", "analysis")

Environment Variables:
    CLAUDE_WORKSPACE: Explicit workspace root (takes priority)
    If not set, uses current working directory.

Output Structure:
    <workspace-root>/outputs/<skill-name>/           # Skill master output dir
    <workspace-root>/outputs/<skill-name>/<task>_<timestamp>/  # Per-invocation dir
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


MASTER_OUTPUT_DIR = "outputs"
SKILL_OUTPUT_DIR_PATTERN = "{skill_name}"
TASK_DIR_PATTERN = "{task_type}_{timestamp}"


def get_workspace_root(start_path: Optional[Path] = None) -> Path:
    """
    Detect the workspace root directory.

    Priority:
    1. CLAUDE_WORKSPACE environment variable (explicit override)
    2. Current working directory (or provided start_path)

    Note: Unlike git-root detection, we use CWD directly since users
    often work from subdirectories and expect outputs relative to where they ran the command.

    Args:
        start_path: Optional starting path (defaults to Path.cwd())

    Returns:
        Path to workspace root
    """
    # Check explicit environment variable first
    env_workspace = os.environ.get("CLAUDE_WORKSPACE")
    if env_workspace:
        path = Path(env_workspace).expanduser().resolve()
        if path.exists():
            return path
        # Fall through to CWD if env var points to non-existent path

    # Use current working directory (or provided start_path)
    current = (start_path or Path.cwd()).resolve()
    return current


def get_master_output_dir(workspace_root: Optional[Path] = None) -> Path:
    """
    Get the master outputs directory for the workspace.

    Args:
        workspace_root: Optional workspace root (auto-detected if not provided)

    Returns:
        Path to <workspace>/outputs/
    """
    root = workspace_root or get_workspace_root()
    master_dir = root / MASTER_OUTPUT_DIR
    master_dir.mkdir(parents=True, exist_ok=True)
    return master_dir


def get_skill_output_dir(
    skill_name: str,
    workspace_root: Optional[Path] = None
) -> Path:
    """
    Get (or create) the skill-specific output directory.

    This is the main entry point for skills to get their output folder.
    Creates: <workspace>/outputs/<skill-name>/

    Args:
        skill_name: Kebab-case skill name (e.g., "content-writer", "resume-doctor")
        workspace_root: Optional workspace root (auto-detected if not provided)

    Returns:
        Path to skill output directory
    """
    master = get_master_output_dir(workspace_root)
    skill_dir = master / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    return skill_dir


def create_task_dir(
    skill_name: str,
    task_type: str,
    workspace_root: Optional[Path] = None,
    timestamp: Optional[str] = None
) -> Path:
    """
    Create a timestamped task subdirectory for a specific skill invocation.

    Creates: <workspace>/outputs/<skill-name>/<task_type>_<YYYYMMDD_HHMMSS>/

    Args:
        skill_name: Kebab-case skill name
        task_type: Short descriptor (e.g., "analysis", "generation", "audit", "build")
        workspace_root: Optional workspace root
        timestamp: Optional custom timestamp (defaults to now)

    Returns:
        Path to created task directory
    """
    skill_dir = get_skill_output_dir(skill_name, workspace_root)

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Sanitize task_type to be filesystem-safe
    safe_task_type = "".join(c if c.isalnum() or c in "-_" else "_" for c in task_type)

    task_dir_name = TASK_DIR_PATTERN.format(
        task_type=safe_task_type,
        timestamp=timestamp
    )
    task_dir = skill_dir / task_dir_name
    task_dir.mkdir(parents=True, exist_ok=True)

    return task_dir


def ensure_skill_output_dir(
    skill_name: str,
    workspace_root: Optional[Path] = None
) -> Path:
    """
    Idempotent convenience function: ensure skill output directory exists.

    Equivalent to get_skill_output_dir() but with clearer intent for
    "make sure it's there before I write files."

    Args:
        skill_name: Kebab-case skill name
        workspace_root: Optional workspace root

    Returns:
        Path to skill output directory
    """
    return get_skill_output_dir(skill_name, workspace_root)


def list_skill_outputs(
    skill_name: str,
    workspace_root: Optional[Path] = None
) -> list[Path]:
    """
    List all task directories for a skill, sorted newest first.

    Args:
        skill_name: Kebab-case skill name
        workspace_root: Optional workspace root

    Returns:
        List of task directory paths (newest first)
    """
    skill_dir = get_skill_output_dir(skill_name, workspace_root)
    if not skill_dir.exists():
        return []

    task_dirs = [d for d in skill_dir.iterdir() if d.is_dir()]
    # Sort by modification time, newest first
    task_dirs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return task_dirs


def get_latest_task_dir(
    skill_name: str,
    workspace_root: Optional[Path] = None
) -> Optional[Path]:
    """
    Get the most recent task directory for a skill.

    Args:
        skill_name: Kebab-case skill name
        workspace_root: Optional workspace root

    Returns:
        Path to latest task directory, or None if none exist
    """
    tasks = list_skill_outputs(skill_name, workspace_root)
    return tasks[0] if tasks else None


# CLI for testing/debugging
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python workspace_utils.py <command> [args...]")
        print("Commands:")
        print("  workspace-root          - Print detected workspace root")
        print("  master-output-dir       - Print master outputs directory")
        print("  skill-output-dir <name> - Print skill output directory")
        print("  create-task <skill> <type> - Create task dir and print path")
        print("  list-tasks <skill>      - List all task dirs for skill")
        print("  latest-task <skill>     - Print latest task dir for skill")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "workspace-root":
        print(get_workspace_root())
    elif cmd == "master-output-dir":
        print(get_master_output_dir())
    elif cmd == "skill-output-dir" and len(sys.argv) > 2:
        print(get_skill_output_dir(sys.argv[2]))
    elif cmd == "create-task" and len(sys.argv) > 3:
        print(create_task_dir(sys.argv[2], sys.argv[3]))
    elif cmd == "list-tasks" and len(sys.argv) > 2:
        tasks = list_skill_outputs(sys.argv[2])
        for t in tasks:
            print(t)
    elif cmd == "latest-task" and len(sys.argv) > 2:
        latest = get_latest_task_dir(sys.argv[2])
        if latest:
            print(latest)
        else:
            print("No tasks found", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)