"""
Output Manager
==============
Handles structured output for both CLI and agent consumption modes.
"""

import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO, Union

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


class OutputFormat(Enum):
    """Supported output formats."""
    JSON = "json"
    YAML = "yaml"
    TABLE = "table"
    TEXT = "text"
    AGENT = "agent"  # Structured format for agent consumption


class OutputManager:
    """
    Manages output formatting for CLI and agent modes.

    Features:
    - Multiple output formats (JSON, YAML, Table, Text, Agent)
    - Streaming for large datasets
    - Consistent structure for agent consumption
    - Color support for terminal output
    - File output for JSON mode to workspace outputs directory
    """

    def __init__(
        self,
        format: OutputFormat = OutputFormat.JSON,
        stream: TextIO = None,
        color: bool = True,
        agent_mode: bool = False,
        task_dir: Path = None,
    ):
        """
        Initialize output manager.

        Args:
            format: Default output format
            stream: Output stream (default: stdout)
            color: Enable colored output
            agent_mode: Whether running in agent mode (structured output)
            task_dir: Task directory for JSON file output (created by workspace_utils)
        """
        self.format = format
        self.stream = stream or sys.stdout
        self.color = color and sys.stdout.isatty()
        self.agent_mode = agent_mode
        self.task_dir = task_dir

        # Colors for terminal output
        self.colors = {
            "reset": "\033[0m",
            "bold": "\033[1m",
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
        } if self.color else {k: "" for k in ["reset", "bold", "red", "green", "yellow", "blue", "magenta", "cyan"]}

        # Track output count for unique filenames
        self._output_count = 0

    def output(
        self,
        data: Any,
        format: OutputFormat = None,
        stream: TextIO = None,
    ) -> None:
        """
        Output data in specified format.

        Args:
            data: Data to output
            format: Override default format
            stream: Override default stream
        """
        fmt = format or self.format
        out = stream or self.stream

        if self.agent_mode:
            # Agent mode always uses structured JSON with metadata
            self._output_agent(data, out)
        elif fmt == OutputFormat.JSON:
            self._output_json(data, out)
        elif fmt == OutputFormat.YAML:
            self._output_yaml(data, out)
        elif fmt == OutputFormat.TABLE:
            self._output_table(data, out)
        elif fmt == OutputFormat.TEXT:
            self._output_text(data, out)
        else:
            self._output_json(data, out)

    def _output_agent(self, data: Any, stream: TextIO) -> None:
        """Output structured data for agent consumption."""
        envelope = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "format_version": "2.1.0",
            "data": data,
        }
        json.dump(envelope, stream, default=str, separators=(",", ":"))
        stream.write("\n")
        stream.flush()

    def _output_json(self, data: Any, stream: TextIO) -> None:
        """Output as JSON."""
        json.dump(data, stream, default=str, indent=2)
        stream.write("\n")
        stream.flush()

        # Also write to file in task_dir if available
        if self.task_dir and not self.agent_mode:
            self._output_count += 1
            output_file = self.task_dir / f"output_{self._output_count:03d}.json"
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, default=str, indent=2)
            except OSError:
                pass  # Silently ignore file write errors

    def _output_yaml(self, data: Any, stream: TextIO) -> None:
        """Output as YAML."""
        if not HAS_YAML:
            self._output_json(data, stream)
            return
        yaml.dump(data, stream, default_flow_style=False, sort_keys=False)
        stream.flush()

    def _output_table(self, data: Any, stream: TextIO) -> None:
        """Output as table."""
        if not HAS_TABULATE:
            self._output_text(data, stream)
            return

        if isinstance(data, list) and data:
            # List of dicts - table
            headers = list(data[0].keys()) if isinstance(data[0], dict) else ["Value"]
            rows = []
            for item in data:
                if isinstance(item, dict):
                    rows.append([item.get(h, "") for h in headers])
                else:
                    rows.append([str(item)])
            stream.write(tabulate(rows, headers=headers, tablefmt="grid"))
        elif isinstance(data, dict):
            # Single dict - key/value table
            rows = [[k, json.dumps(v, default=str) if isinstance(v, (dict, list)) else v]
                    for k, v in data.items()]
            stream.write(tabulate(rows, headers=["Key", "Value"], tablefmt="grid"))
        else:
            stream.write(str(data))
        stream.write("\n")
        stream.flush()

    def _output_text(self, data: Any, stream: TextIO) -> None:
        """Output as human-readable text."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    stream.write(f"{self.colors['bold']}{key}:{self.colors['reset']}\n")
                    stream.write(json.dumps(value, indent=2, default=str))
                else:
                    stream.write(f"{self.colors['bold']}{key}:{self.colors['reset']} {value}\n")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                stream.write(f"{self.colors['cyan']}[{i}]{self.colors['reset']} ")
                if isinstance(item, dict):
                    stream.write(json.dumps(item, default=str))
                else:
                    stream.write(str(item))
                stream.write("\n")
        else:
            stream.write(str(data))
        stream.write("\n")
        stream.flush()

    def success(self, message: str, data: Any = None) -> None:
        """Output success message."""
        if self.agent_mode:
            self.output({"status": "success", "message": message, "data": data})
        else:
            prefix = f"{self.colors['green']}✓{self.colors['reset']} "
            self.stream.write(prefix + message + "\n")
            if data:
                self.output(data)
            self.stream.flush()

    def error(self, message: str, data: Any = None, exit_code: int = 1) -> None:
        """Output error message."""
        if self.agent_mode:
            self.output({"status": "error", "message": message, "data": data, "exit_code": exit_code})
        else:
            prefix = f"{self.colors['red']}✗{self.colors['reset']} "
            self.stream.write(prefix + message + "\n")
            if data:
                self.output(data)
            self.stream.flush()

    def warning(self, message: str) -> None:
        """Output warning message."""
        if self.agent_mode:
            self.output({"status": "warning", "message": message})
        else:
            prefix = f"{self.colors['yellow']}⚠{self.colors['reset']} "
            self.stream.write(prefix + message + "\n")
            self.stream.flush()

    def info(self, message: str) -> None:
        """Output info message."""
        if self.agent_mode:
            self.output({"status": "info", "message": message})
        else:
            prefix = f"{self.colors['blue']}ℹ{self.colors['reset']} "
            self.stream.write(prefix + message + "\n")
            self.stream.flush()

    def progress(self, message: str) -> None:
        """Output progress message."""
        if not self.agent_mode:
            prefix = f"{self.colors['magenta']}⟳{self.colors['reset']} "
            self.stream.write(prefix + message + "\n")
            self.stream.flush()

    def table_from_list(
        self,
        items: List[Dict],
        columns: List[str] = None,
        title: str = None,
    ) -> None:
        """Output a list of dicts as a formatted table."""
        if not items:
            self.info("No items to display")
            return

        if self.format == OutputFormat.TABLE or self.agent_mode:
            if columns:
                # Filter columns
                filtered = [{k: v for k, v in item.items() if k in columns} for item in items]
            else:
                filtered = items

            if title:
                self.stream.write(f"\n{self.colors['bold']}{title}{self.colors['reset']}\n")

            self.output(filtered, format=OutputFormat.TABLE)
        else:
            self.output(items)

    def paginate(
        self,
        items: List[Any],
        page: int = 1,
        per_page: int = 20,
        formatter: callable = None,
    ) -> None:
        """Paginate output for large lists."""
        total = len(items)
        total_pages = (total + per_page - 1) // per_page
        page = max(1, min(page, total_pages))

        start = (page - 1) * per_page
        end = start + per_page
        page_items = items[start:end]

        if formatter:
            page_items = [formatter(item) for item in page_items]

        self.output({
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
            },
            "items": page_items,
        })

    def streaming_output(self, generator, format: OutputFormat = None) -> None:
        """Output items from a generator (for large datasets)."""
        fmt = format or self.format

        if fmt == OutputFormat.JSON:
            # JSON Lines format for streaming
            for item in generator:
                json.dump(item, self.stream, default=str, separators=(",", ":"))
                self.stream.write("\n")
            self.stream.flush()
        elif fmt == OutputFormat.AGENT:
            # Agent streaming envelope
            for item in generator:
                envelope = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "format_version": "2.1.0",
                    "data": item,
                    "stream": True,
                }
                json.dump(envelope, self.stream, default=str, separators=(",", ":"))
                self.stream.write("\n")
            self.stream.flush()
        else:
            # Collect and output normally
            items = list(generator)
            self.output(items, format=fmt)


class ProgressTracker:
    """Simple progress tracker for long-running operations."""

    def __init__(self, output_manager: OutputManager, total: int, label: str = "Progress"):
        self.output_manager = output_manager
        self.total = total
        self.current = 0
        self.label = label
        self.start_time = datetime.utcnow()

    def increment(self, amount: int = 1) -> None:
        """Increment progress."""
        self.current += amount
        if not self.output_manager.agent_mode:
            percent = (self.current / self.total * 100) if self.total > 0 else 0
            elapsed = (datetime.utcnow() - self.start_time).total_seconds()
            rate = self.current / elapsed if elapsed > 0 else 0
            eta = (self.total - self.current) / rate if rate > 0 else 0

            bar_length = 30
            filled = int(bar_length * self.current / self.total) if self.total > 0 else 0
            bar = "█" * filled + "░" * (bar_length - filled)

            self.output_manager.stream.write(
                f"\r{self.label}: [{bar}] {percent:.1f}% "
                f"({self.current}/{self.total}) "
                f"ETA: {eta:.0f}s"
            )
            self.output_manager.stream.flush()

    def finish(self, message: str = "Complete") -> None:
        """Finish progress tracking."""
        if not self.output_manager.agent_mode:
            self.output_manager.stream.write("\n")
            self.output_manager.success(message)
        else:
            self.output_manager.output({"status": "complete", "message": message})