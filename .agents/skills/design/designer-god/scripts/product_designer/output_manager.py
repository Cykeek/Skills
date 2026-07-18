#!/usr/bin/env python3
"""
Product Designer Output Manager
===============================
Manages CLI output formatting for Product Designer Skill.
"""

import json
import sys
from typing import Any, Optional
from enum import Enum
from pathlib import Path

# Import workspace utilities for standardized output directory management
try:
    from workspace_utils import get_skill_output_dir, create_task_dir
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from workspace_utils import get_skill_output_dir, create_task_dir


class OutputFormat(Enum):
    JSON = "json"
    TEXT = "text"
    TABLE = "table"


class OutputManager:
    """Manages CLI output formatting."""

    def __init__(
        self,
        format: OutputFormat = OutputFormat.JSON,
        task_dir: Optional[str] = None,
        skill_name: str = "designer-god",
        task_type: str = "run"
    ):
        self.format = format
        self.skill_name = skill_name
        self.task_type = task_type
        self._task_dir = task_dir
        self._output_count = 0

    @property
    def task_dir(self) -> Optional[str]:
        """Get or create task directory for JSON file output."""
        if self._task_dir is None:
            self._task_dir = str(create_task_dir(self.skill_name, self.task_type))
        return self._task_dir

    def output(self, data: Any, format: OutputFormat = None, write_file: bool = False) -> None:
        """Output data in the configured format."""
        fmt = format or self.format

        if fmt == OutputFormat.JSON:
            self._output_json(data, write_file)
        elif fmt == OutputFormat.TEXT:
            self._output_text(data)
        elif fmt == OutputFormat.TABLE:
            self._output_table(data)

    def _output_json(self, data: Any, write_file: bool = False) -> None:
        """Output as JSON."""
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        print(json_str)

        # Also write to file in task_dir if requested
        if write_file and self.task_dir:
            self._output_count += 1
            output_file = Path(self.task_dir) / f"output_{self._output_count:03d}.json"
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(json_str)
            except OSError:
                pass  # Silently ignore file write errors

    def _output_text(self, data: Any, indent: int = 0) -> None:
        """Output as formatted text."""
        prefix = "  " * indent
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    print(f"{prefix}{key}:")
                    self._output_text(value, indent + 1)
                else:
                    print(f"{prefix}{key}: {value}")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    print(f"{prefix}[{i}]:")
                    self._output_text(item, indent + 1)
                else:
                    print(f"{prefix}- {item}")
        else:
            print(f"{prefix}{data}")

    def _output_table(self, data: Any) -> None:
        """Output as simple table."""
        if isinstance(data, list) and data and isinstance(data[0], dict):
            headers = list(data[0].keys())
            # Print headers
            print(" | ".join(headers))
            print("-" * (sum(len(h) for h in headers) + 3 * len(headers)))
            # Print rows
            for row in data:
                print(" | ".join(str(row.get(h, "")) for h in headers))
        else:
            self._output_text(data)

    def set_format(self, format: OutputFormat | str) -> None:
        """Set output format."""
        if isinstance(format, str):
            self.format = OutputFormat(format)
        else:
            self.format = format

    def error(self, message: str, code: int = 1, details: Any = None) -> None:
        """Output error and exit."""
        error_data = {"error": message, "code": code}
        if details:
            error_data["details"] = details
        self.output(error_data)
        sys.exit(code)

    def success(self, message: str, data: Any = None) -> None:
        """Output success message."""
        result = {"status": "success", "message": message}
        if data:
            result["data"] = data
        self.output(result)