"""
Contract Tests for CLI Commands
================================
Tests for CLI command parsing and execution.
"""

import json
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cal_booking_skill.cli import CLI, main
from cal_booking_skill.api_client import CalComClient, OutputFormat


class TestCLIParser:
    """Tests for CLI argument parsing."""

    @pytest.fixture
    def cli(self):
        client = CalComClient(api_key="test")
        return CLI(client)

    def test_parser_creation(self, cli):
        """Test parser is created with all commands."""
        parser = cli.create_parser()
        assert parser is not None

    def test_global_args(self, cli):
        """Test global arguments are parsed."""
        parser = cli.create_parser()
        args = parser.parse_args([
            "--api-key", "cal_test_123",
            "--output", "yaml",
            "--rate-limit", "60",
            "test-auth"
        ])
        assert args.api_key == "cal_test_123"
        assert args.output == "yaml"
        assert args.rate_limit == 60
        assert args.command == "test-auth"

    def test_create_booking_args(self, cli):
        """Test create-booking command arguments."""
        parser = cli.create_parser()
        args = parser.parse_args([
            "create-booking",
            "--start", "2026-07-20T14:00:00Z",
            "--attendee-name", "John Doe",
            "--attendee-email", "john@example.com",
            "--attendee-timezone", "America/Los_Angeles",
            "--event-type-id", "123",
        ])
        assert args.command == "create-booking"
        assert args.start == "2026-07-20T14:00:00Z"
        assert args.attendee_name == "John Doe"
        assert args.event_type_id == 123

    def test_list_bookings_args(self, cli):
        """Test list-bookings command arguments."""
        parser = cli.create_parser()
        args = parser.parse_args([
            "list-bookings",
            "--status", "ACCEPTED",
            "--page", "2",
            "--limit", "10",
        ])
        assert args.command == "list-bookings"
        assert args.status == "ACCEPTED"
        assert args.page == 2
        assert args.limit == 10

    def test_check_availability_args(self, cli):
        """Test check-availability command arguments."""
        parser = cli.create_parser()
        args = parser.parse_args([
            "check-availability",
            "--start-time", "2026-07-20T00:00:00Z",
            "--end-time", "2026-07-27T00:00:00Z",
            "--timezone", "America/Los_Angeles",
            "--event-type-id", "123",
        ])
        assert args.command == "check-availability"
        assert args.event_type_id == 123

    def test_setup_webhook_args(self, cli):
        """Test setup-webhook command arguments."""
        parser = cli.create_parser()
        args = parser.parse_args([
            "setup-webhook",
            "--url", "https://example.com/webhook",
            "--events", "BOOKING_CREATED", "BOOKING_CANCELLED",
            "--secret", "mysecret",
        ])
        assert args.command == "setup-webhook"
        assert args.url == "https://example.com/webhook"
        assert args.events == ["BOOKING_CREATED", "BOOKING_CANCELLED"]
        assert args.secret == "mysecret"

    def test_create_event_type_args(self, cli):
        """Test create-event-type command arguments."""
        parser = cli.create_parser()
        args = parser.parse_args([
            "create-event-type",
            "--config-file", "config.json",
            "--title", "New Title",
        ])
        assert args.command == "create-event-type"
        assert args.config_file == "config.json"
        assert args.title == "New Title"


class TestCLICommands:
    """Tests for CLI command execution."""

    @pytest.fixture
    def cli(self):
        client = CalComClient(api_key="test", validate_requests=False, validate_responses=False)
        return CLI(client)

    @pytest.mark.asyncio
    async def test_cmd_test_auth(self, cli):
        """Test test-auth command."""
        mock_user = {"id": 1, "name": "Test User", "email": "test@example.com"}
        cli.client.test_auth = AsyncMock(return_value=mock_user)

        args = MagicMock()
        args.verbose = False

        result = await cli.cmd_test_auth(args)
        assert result == 0
        cli.client.test_auth.assert_called_once()

    @pytest.mark.asyncio
    async def test_cmd_create_booking(self, cli, sample_booking_response):
        """Test create-booking command."""
        cli.client.create_booking = AsyncMock(return_value=sample_booking_response)

        args = MagicMock()
        args.start = "2026-07-20T14:00:00Z"
        args.attendee_name = "John Doe"
        args.attendee_email = "john@example.com"
        args.attendee_timezone = "America/Los_Angeles"
        args.attendee_phone = None
        args.attendee_language = None
        args.event_type_id = 123
        args.event_type_slug = None
        args.username = None
        args.org_slug = None
        args.responses = None
        args.metadata = None
        args.idempotency_key = None
        args.instant = False
        args.recurrence_count = None
        args.seat_reference = None
        args.verbose = False

        result = await cli.cmd_create_booking(args)
        assert result == 0
        cli.client.create_booking.assert_called_once()

    @pytest.mark.asyncio
    async def test_cmd_list_bookings(self, cli):
        """Test list-bookings command."""
        mock_data = {"bookings": [], "pagination": {}}
        cli.client.list_bookings = AsyncMock(return_value=mock_data)

        args = MagicMock()
        args.status = "ACCEPTED"
        args.start_time = None
        args.end_time = None
        args.attendee_email = None
        args.page = 1
        args.limit = 50
        args.verbose = False

        result = await cli.cmd_list_bookings(args)
        assert result == 0

    @pytest.mark.asyncio
    async def test_cmd_check_availability(self, cli):
        """Test check-availability command."""
        mock_data = {"slots": {}}
        cli.client.get_availability = AsyncMock(return_value=mock_data)

        args = MagicMock()
        args.start_time = "2026-07-20T00:00:00Z"
        args.end_time = "2026-07-27T00:00:00Z"
        args.timezone = "America/Los_Angeles"
        args.event_type_id = 123
        args.event_type_slug = None
        args.username = None
        args.team_slug = None
        args.org_slug = None
        args.verbose = False

        result = await cli.cmd_check_availability(args)
        assert result == 0

    @pytest.mark.asyncio
    async def test_cmd_setup_webhook(self, cli):
        """Test setup-webhook command."""
        mock_data = {"id": 1, "url": "https://example.com/webhook"}
        cli.client.create_webhook = AsyncMock(return_value=mock_data)

        args = MagicMock()
        args.url = "https://example.com/webhook"
        args.events = ["BOOKING_CREATED"]
        args.secret = "testsecret"
        args.inactive = False
        args.verbose = False

        result = await cli.cmd_setup_webhook(args)
        assert result == 0

    @pytest.mark.asyncio
    async def test_cmd_verify_webhook_valid(self, cli):
        """Test verify-webhook command with valid signature."""
        import hmac
        import hashlib
        import time

        secret = "testsecret"
        payload = b'{"triggerEvent": "BOOKING_CREATED"}'
        timestamp = str(int(time.time()))
        signature = hmac.new(
            secret.encode(),
            f"{timestamp}.{payload.decode()}".encode(),
            hashlib.sha256,
        ).hexdigest()

        args = MagicMock()
        args.payload_file = "test_payload.json"
        args.signature = signature
        args.timestamp = timestamp
        args.secret = secret
        args.verbose = False

        with patch("builtins.open", MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=lambda: payload))))):
            result = await cli.cmd_verify_webhook(args)
            assert result == 0

    @pytest.mark.asyncio
    async def test_cmd_verify_webhook_invalid(self, cli):
        """Test verify-webhook command with invalid signature."""
        args = MagicMock()
        args.payload_file = "test_payload.json"
        args.signature = "invalid"
        args.timestamp = str(int(time.time()))
        args.secret = "wrongsecret"
        args.verbose = False

        with patch("builtins.open", MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=lambda: b'{}'))))):
            result = await cli.cmd_verify_webhook(args)
            assert result == 1


class TestCLIErrorHandling:
    """Tests for CLI error handling."""

    @pytest.fixture
    def cli(self):
        client = CalComClient(api_key="test")
        return CLI(client)

    @pytest.mark.asyncio
    async def test_command_exception_handling(self, cli):
        """Test command exceptions are caught and formatted."""
        cli.client.test_auth = AsyncMock(side_effect=Exception("API Error"))

        args = MagicMock()
        args.verbose = False

        result = await cli.cmd_test_auth(args)
        assert result == 1

    @pytest.mark.asyncio
    async def test_unknown_command(self, cli):
        """Test unknown command returns error."""
        args = MagicMock()
        args.command = "unknown-command"
        args.verbose = False

        result = await cli.run_async(args)
        assert result == 1


class TestMainEntryPoint:
    """Tests for main entry point."""

    @patch("cal_booking_skill.cli.CLI.run")
    def test_main_calls_cli_run(self, mock_run):
        """Test main calls CLI.run with sys.argv."""
        mock_run.return_value = 0
        with patch("sys.argv", ["cal-booking", "test-auth"]):
            result = main()
        assert result == 0
        mock_run.assert_called_once_with(["test-auth"])