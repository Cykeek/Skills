#!/usr/bin/env python3
"""
Wix Support Output Manager
==========================
Manages CLI output formatting for Wix Support Skill.
"""

import json
import sys
from typing import Any, Optional
from enum import Enum
from pathlib import Path

# Import workspace utilities for standardized output management
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
try:
    from workspace_utils import get_skill_output_dir, create_task_dir
except ImportError:
    pass


class OutputFormat(Enum):
    JSON = "json"
    TEXT = "text"
    TABLE = "table"


class OutputManager:
    """Manages CLI output formatting."""

    def __init__(self, format: OutputFormat = OutputFormat.JSON):
        self.format = format

    def output(self, data: Any) -> None:
        """Output data in the configured format."""
        if self.format == OutputFormat.JSON:
            self._output_json(data)
        elif self.format == OutputFormat.TEXT:
            self._output_text(data)
        elif self.format == OutputFormat.TABLE:
            self._output_table(data)

    def _output_json(self, data: Any) -> None:
        """Output as JSON."""
        print(json.dumps(data, indent=2, ensure_ascii=False))

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