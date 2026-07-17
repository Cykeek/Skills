"""
Contract Tests for Output Manager
==================================
Tests for OutputManager and ProgressTracker.
"""

import json
import sys
from io import StringIO
from unittest.mock import MagicMock

import pytest

from cal_booking_skill.output_manager import (
    OutputManager,
    OutputFormat,
    ProgressTracker,
)


class TestOutputManager:
    """Tests for OutputManager."""

    @pytest.fixture
    def output_stream(self):
        return StringIO()

    @pytest.fixture
    def manager(self, output_stream):
        return OutputManager(format=OutputFormat.JSON, stream=output_stream, color=False)

    def test_output_json(self, manager, output_stream):
        """Test JSON output."""
        data = {"key": "value", "number": 42}
        manager.output(data)
        output = output_stream.getvalue()
        parsed = json.loads(output.strip())
        assert parsed == data

    def test_output_yaml(self, output_stream):
        """Test YAML output."""
        try:
            import yaml
            manager = OutputManager(format=OutputFormat.YAML, stream=output_stream, color=False)
            data = {"key": "value", "list": [1, 2, 3]}
            manager.output(data)
            output = output_stream.getvalue()
            parsed = yaml.safe_load(output)
            assert parsed == data
        except ImportError:
            pytest.skip("PyYAML not installed")

    def test_output_text(self, manager, output_stream):
        """Test text output."""
        manager.format = OutputFormat.TEXT
        data = {"name": "John", "age": 30}
        manager.output(data)
        output = output_stream.getvalue()
        assert "name: John" in output
        assert "age: 30" in output

    def test_output_table_list(self, output_stream):
        """Test table output for list of dicts."""
        try:
            from tabulate import tabulate
            manager = OutputManager(format=OutputFormat.TABLE, stream=output_stream, color=False)
            data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
            manager.output(data)
            output = output_stream.getvalue()
            assert "John" in output
            assert "Jane" in output
            assert "30" in output
        except ImportError:
            pytest.skip("tabulate not installed")

    def test_output_table_dict(self, output_stream):
        """Test table output for single dict."""
        try:
            from tabulate import tabulate
            manager = OutputManager(format=OutputFormat.TABLE, stream=output_stream, color=False)
            data = {"name": "John", "age": 30}
            manager.output(data)
            output = output_stream.getvalue()
            assert "John" in output
            assert "30" in output
        except ImportError:
            pytest.skip("tabulate not installed")

    def test_agent_mode_output(self, output_stream):
        """Test agent mode structured output."""
        manager = OutputManager(format=OutputFormat.JSON, stream=output_stream, color=False, agent_mode=True)
        data = {"status": "success"}
        manager.output(data)
        output = output_stream.getvalue()
        parsed = json.loads(output.strip())
        assert "timestamp" in parsed
        assert "format_version" in parsed
        assert parsed["data"] == data

    def test_success_message(self, manager, output_stream):
        """Test success message output."""
        manager.success("Operation completed", {"id": 123})
        output = output_stream.getvalue()
        assert "Operation completed" in output

    def test_error_message(self, manager, output_stream):
        """Test error message output."""
        manager.error("Something failed", {"code": 500})
        output = output_stream.getvalue()
        assert "Something failed" in output

    def test_warning_message(self, manager, output_stream):
        """Test warning message output."""
        manager.warning("This is a warning")
        output = output_stream.getvalue()
        assert "This is a warning" in output

    def test_info_message(self, manager, output_stream):
        """Test info message output."""
        manager.info("Information")
        output = output_stream.getvalue()
        assert "Information" in output

    def test_progress_message(self, manager, output_stream):
        """Test progress message output."""
        manager.progress("Processing...")
        output = output_stream.getvalue()
        assert "Processing..." in output

    def test_table_from_list(self, output_stream):
        """Test table_from_list method."""
        try:
            from tabulate import tabulate
            manager = OutputManager(format=OutputFormat.TABLE, stream=output_stream, color=False)
            items = [{"name": "A", "value": 1}, {"name": "B", "value": 2}]
            manager.table_from_list(items, columns=["name"], title="Test Table")
            output = output_stream.getvalue()
            assert "Test Table" in output
            assert "A" in output
            assert "B" in output
        except ImportError:
            pytest.skip("tabulate not installed")

    def test_paginate(self, manager, output_stream):
        """Test paginate method."""
        items = list(range(100))
        manager.paginate(items, page=2, per_page=10)
        output = output_stream.getvalue()
        parsed = json.loads(output.strip())
        assert parsed["pagination"]["page"] == 2
        assert parsed["pagination"]["per_page"] == 10
        assert parsed["pagination"]["total"] == 100
        assert parsed["items"] == list(range(10, 20))

    def test_streaming_output_json(self, manager, output_stream):
        """Test streaming JSON output."""
        def generator():
            yield {"id": 1}
            yield {"id": 2}

        manager.streaming_output(generator())
        output = output_stream.getvalue()
        lines = output.strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0]) == {"id": 1}
        assert json.loads(lines[1]) == {"id": 2}

    def test_streaming_output_agent(self, output_stream):
        """Test streaming agent output."""
        manager = OutputManager(format=OutputFormat.JSON, stream=output_stream, color=False, agent_mode=True)

        def generator():
            yield {"id": 1}

        manager.streaming_output(generator())
        output = output_stream.getvalue()
        parsed = json.loads(output.strip())
        assert parsed["stream"] is True
        assert parsed["data"] == {"id": 1}


class TestProgressTracker:
    """Tests for ProgressTracker."""

    @pytest.fixture
    def output_stream(self):
        return StringIO()

    @pytest.fixture
    def manager(self, output_stream):
        return OutputManager(format=OutputFormat.JSON, stream=output_stream, color=False)

    def test_progress_tracker_increment(self, manager):
        """Test progress tracker increment."""
        tracker = ProgressTracker(manager, total=10, label="Test")
        tracker.increment(3)
        assert tracker.current == 3

    def test_progress_tracker_finish(self, manager, output_stream):
        """Test progress tracker finish."""
        tracker = ProgressTracker(manager, total=10, label="Test")
        tracker.increment(10)
        tracker.finish("Done")
        output = output_stream.getvalue()
        assert "Done" in output

    def test_progress_tracker_agent_mode(self, output_stream):
        """Test progress tracker in agent mode."""
        manager = OutputManager(format=OutputFormat.JSON, stream=output_stream, color=False, agent_mode=True)
        tracker = ProgressTracker(manager, total=10, label="Test")
        tracker.increment(5)
        tracker.finish("Complete")
        output = output_stream.getvalue()
        parsed = json.loads(output.strip())
        assert parsed["status"] == "complete"
        assert parsed["message"] == "Complete"