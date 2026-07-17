#!/usr/bin/env python3
"""
CLI Commands for Cal.com Booking Skill
======================================
Maps CLI commands to CalComClient methods with proper validation and output.
Outputs results cleanly formatted using json.dumps via client.output().
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .api_client import CalComClient, AuthMethod, OutputFormat, OutputManager
from .validation import validate_request, validate_response
from .output_manager import OutputManager as OM


class CLI:
    """CLI command handler for Cal.com Booking Skill."""

    def __init__(self, client: CalComClient):
        self.client = client
        self.output_manager = client.output_manager

    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with all commands."""
        parser = argparse.ArgumentParser(
            prog="cal-booking",
            description="Cal.com Booking Skill CLI - Manage bookings, event types, and schedules",
        )
        parser.add_argument(
            "--api-key",
            help="Cal.com API key (cal_ or cal_live_ prefix)",
        )
        parser.add_argument(
            "--oauth-token",
            help="OAuth 2.0 access token",
        )
        parser.add_argument(
            "--auth-method",
            choices=["api_key", "oauth2_pkce", "platform"],
            default="api_key",
            help="Authentication method",
        )
        parser.add_argument(
            "--base-url",
            default="https://api.cal.com/v2/",
            help="Cal.com API base URL",
        )
        parser.add_argument(
            "--rate-limit",
            type=int,
            default=120,
            help="Requests per minute limit",
        )
        parser.add_argument(
            "--output",
            choices=["json", "yaml", "table", "text"],
            default="json",
            help="Output format",
        )
        parser.add_argument(
            "--no-validate",
            action="store_true",
            help="Disable request/response validation",
        )
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Verbose output",
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # ========== Booking Commands ==========
        booking_parser = subparsers.add_parser("create-booking", help="Create a new booking")
        booking_parser.add_argument("--start", required=True, help="Start time (ISO 8601, UTC)")
        booking_parser.add_argument("--attendee-name", required=True, help="Attendee name")
        booking_parser.add_argument("--attendee-email", required=True, help="Attendee email")
        booking_parser.add_argument("--attendee-timezone", required=True, help="Attendee timezone (IANA)")
        booking_parser.add_argument("--attendee-phone", help="Attendee phone (E.164)")
        booking_parser.add_argument("--attendee-language", help="Attendee language (e.g., en-US)")
        booking_parser.add_argument("--event-type-id", type=int, help="Event type ID")
        booking_parser.add_argument("--event-type-slug", help="Event type slug")
        booking_parser.add_argument("--username", help="Username for slug lookup")
        booking_parser.add_argument("--org-slug", help="Organization slug")
        booking_parser.add_argument("--responses", help="JSON string of custom form responses")
        booking_parser.add_argument("--metadata", help="JSON string of metadata")
        booking_parser.add_argument("--idempotency-key", help="Idempotency key (auto-generated if omitted)")
        booking_parser.add_argument("--instant", action="store_true", help="Instant booking (team events)")
        booking_parser.add_argument("--recurrence-count", type=int, help="Recurring booking count")
        booking_parser.add_argument("--seat-reference", help="Seat reference for multi-seat events")

        list_bookings_parser = subparsers.add_parser("list-bookings", help="List bookings")
        list_bookings_parser.add_argument("--status", choices=["PENDING", "ACCEPTED", "CANCELLED", "REJECTED"])
        list_bookings_parser.add_argument("--start-time", help="Filter after (ISO 8601)")
        list_bookings_parser.add_argument("--end-time", help="Filter before (ISO 8601)")
        list_bookings_parser.add_argument("--attendee-email", help="Filter by attendee email")
        list_bookings_parser.add_argument("--page", type=int, default=1)
        list_bookings_parser.add_argument("--limit", type=int, default=50)

        get_booking_parser = subparsers.add_parser("get-booking", help="Get a booking by ID/UID")
        get_booking_parser.add_argument("booking_id", help="Booking ID or UID")

        cancel_booking_parser = subparsers.add_parser("cancel-booking", help="Cancel a booking")
        cancel_booking_parser.add_argument("booking_id", help="Booking ID or UID")
        cancel_booking_parser.add_argument("--reason", help="Cancellation reason")
        cancel_booking_parser.add_argument("--canceler", choices=["ATTENDEE", "HOST"], default="ATTENDEE")

        reschedule_parser = subparsers.add_parser("reschedule-booking", help="Reschedule a booking")
        reschedule_parser.add_argument("booking_id", help="Booking ID or UID")
        reschedule_parser.add_argument("--start-time", required=True, help="New start time (ISO 8601)")
        reschedule_parser.add_argument("--end-time", help="New end time (ISO 8601)")

        # ========== Event Type Commands ==========
        create_et_parser = subparsers.add_parser("create-event-type", help="Create an event type")
        create_et_parser.add_argument("--config-file", required=True, help="Path to event type config JSON")
        create_et_parser.add_argument("--title", help="Event type title (overrides config)")
        create_et_parser.add_argument("--slug", help="Event type slug (overrides config)")
        create_et_parser.add_argument("--length", type=int, help="Length in minutes (overrides config)")

        list_et_parser = subparsers.add_parser("list-event-types", help="List event types")
        list_et_parser.add_argument("--username", help="Filter by username")
        list_et_parser.add_argument("--team-slug", help="Filter by team slug")
        list_et_parser.add_argument("--org-slug", help="Filter by organization slug")
        list_et_parser.add_argument("--page", type=int, default=1)
        list_et_parser.add_argument("--limit", type=int, default=50)

        get_et_parser = subparsers.add_parser("get-event-type", help="Get event type by ID")
        get_et_parser.add_argument("event_type_id", type=int)

        update_et_parser = subparsers.add_parser("update-event-type", help="Update an event type")
        update_et_parser.add_argument("event_type_id", type=int)
        update_et_parser.add_argument("--config-file", required=True, help="Path to updated config JSON")

        delete_et_parser = subparsers.add_parser("delete-event-type", help="Delete an event type")
        delete_et_parser.add_argument("event_type_id", type=int)

        # ========== Schedule Commands ==========
        create_sched_parser = subparsers.add_parser("create-schedule", help="Create a schedule")
        create_sched_parser.add_argument("--config-file", required=True, help="Path to schedule config JSON")
        create_sched_parser.add_argument("--name", help="Schedule name (overrides config)")
        create_sched_parser.add_argument("--timezone", help="Timezone (overrides config)")
        create_sched_parser.add_argument("--default", action="store_true", help="Set as default schedule")

        list_sched_parser = subparsers.add_parser("list-schedules", help="List schedules")
        get_sched_parser = subparsers.add_parser("get-schedule", help="Get schedule by ID")
        get_sched_parser.add_argument("schedule_id", type=int)

        update_sched_parser = subparsers.add_parser("update-schedule", help="Update a schedule")
        update_sched_parser.add_argument("schedule_id", type=int)
        update_sched_parser.add_argument("--config-file", required=True, help="Path to updated config JSON")

        delete_sched_parser = subparsers.add_parser("delete-schedule", help="Delete a schedule")
        delete_sched_parser.add_argument("schedule_id", type=int)

        # ========== Availability Commands ==========
        avail_parser = subparsers.add_parser("check-availability", help="Check available time slots")
        avail_parser.add_argument("--start-time", required=True, help="Query window start (ISO 8601)")
        avail_parser.add_argument("--end-time", required=True, help="Query window end (ISO 8601)")
        avail_parser.add_argument("--timezone", required=True, help="Attendee timezone (IANA)")
        avail_parser.add_argument("--event-type-id", type=int, help="Event type ID")
        avail_parser.add_argument("--event-type-slug", help="Event type slug")
        avail_parser.add_argument("--username", help="Username for slug lookup")
        avail_parser.add_argument("--team-slug", help="Team slug")
        avail_parser.add_argument("--org-slug", help="Organization slug")

        # ========== Webhook Commands ==========
        webhook_parser = subparsers.add_parser("setup-webhook", help="Create a webhook subscription")
        webhook_parser.add_argument("--url", required=True, help="Webhook endpoint URL (HTTPS)")
        webhook_parser.add_argument("--events", required=True, nargs="+", help="Trigger events")
        webhook_parser.add_argument("--secret", help="HMAC secret (auto-generated if omitted)")
        webhook_parser.add_argument("--inactive", action="store_true", help="Create as inactive")

        list_webhook_parser = subparsers.add_parser("list-webhooks", help="List webhooks")
        get_webhook_parser = subparsers.add_parser("get-webhook", help="Get webhook by ID")
        get_webhook_parser.add_argument("webhook_id", type=int)

        update_webhook_parser = subparsers.add_parser("update-webhook", help="Update a webhook")
        update_webhook_parser.add_argument("webhook_id", type=int)
        update_webhook_parser.add_argument("--url", help="New webhook URL")
        update_webhook_parser.add_argument("--events", nargs="+", help="New trigger events")
        update_webhook_parser.add_argument("--secret", help="New HMAC secret")
        update_webhook_parser.add_argument("--active", type=bool, help="Set active status")

        delete_webhook_parser = subparsers.add_parser("delete-webhook", help="Delete a webhook")
        delete_webhook_parser.add_argument("webhook_id", type=int)

        # ========== Utility Commands ==========
        test_auth_parser = subparsers.add_parser("test-auth", help="Test authentication")

        verify_webhook_parser = subparsers.add_parser("verify-webhook", help="Verify webhook signature")
        verify_webhook_parser.add_argument("--payload-file", required=True, help="Path to payload JSON file")
        verify_webhook_parser.add_argument("--signature", required=True, help="cal-signature header value")
        verify_webhook_parser.add_argument("--timestamp", required=True, help="cal-timestamp header value")
        verify_webhook_parser.add_argument("--secret", required=True, help="Webhook secret")

        return parser

    async def run_async(self, args: argparse.Namespace) -> int:
        """Run command asynchronously."""
        try:
            if args.command == "create-booking":
                return await self.cmd_create_booking(args)
            elif args.command == "list-bookings":
                return await self.cmd_list_bookings(args)
            elif args.command == "get-booking":
                return await self.cmd_get_booking(args)
            elif args.command == "cancel-booking":
                return await self.cmd_cancel_booking(args)
            elif args.command == "reschedule-booking":
                return await self.cmd_reschedule_booking(args)
            elif args.command == "create-event-type":
                return await self.cmd_create_event_type(args)
            elif args.command == "list-event-types":
                return await self.cmd_list_event_types(args)
            elif args.command == "get-event-type":
                return await self.cmd_get_event_type(args)
            elif args.command == "update-event-type":
                return await self.cmd_update_event_type(args)
            elif args.command == "delete-event-type":
                return await self.cmd_delete_event_type(args)
            elif args.command == "create-schedule":
                return await self.cmd_create_schedule(args)
            elif args.command == "list-schedules":
                return await self.cmd_list_schedules(args)
            elif args.command == "get-schedule":
                return await self.cmd_get_schedule(args)
            elif args.command == "update-schedule":
                return await self.cmd_update_schedule(args)
            elif args.command == "delete-schedule":
                return await self.cmd_delete_schedule(args)
            elif args.command == "check-availability":
                return await self.cmd_check_availability(args)
            elif args.command == "setup-webhook":
                return await self.cmd_setup_webhook(args)
            elif args.command == "list-webhooks":
                return await self.cmd_list_webhooks(args)
            elif args.command == "get-webhook":
                return await self.cmd_get_webhook(args)
            elif args.command == "update-webhook":
                return await self.cmd_update_webhook(args)
            elif args.command == "delete-webhook":
                return await self.cmd_delete_webhook(args)
            elif args.command == "test-auth":
                return await self.cmd_test_auth(args)
            elif args.command == "verify-webhook":
                return await self.cmd_verify_webhook(args)
            else:
                self.output_manager.output({"error": f"Unknown command: {args.command}"})
                return 1
        except Exception as e:
            self.output_manager.output({"error": str(e), "type": type(e).__name__})
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1

    def run(self, args: List[str] = None) -> int:
        """Run CLI with given arguments."""
        parser = self.create_parser()
        parsed = parser.parse_args(args)

        if not parsed.command:
            parser.print_help()
            return 0

        # Configure client from args
        if parsed.api_key:
            self.client.api_key = parsed.api_key
            self.client.auth_method = AuthMethod.API_KEY
        if parsed.oauth_token:
            self.client.oauth_token = parsed.oauth_token
            self.client.auth_method = AuthMethod.OAUTH2_PKCE
        if parsed.base_url:
            self.client.base_url = parsed.base_url
        if parsed.rate_limit:
            self.client.rate_limiter = self.client.rate_limiter.__class__(rate=parsed.rate_limit, per=60)
        if parsed.no_validate:
            self.client.validate_requests = False
            self.client.validate_responses = False

        output_format = OutputFormat(parsed.output)
        self.client.set_output_format(output_format)

        return asyncio.run(self.run_async(parsed))

    # ========== Command Implementations ==========

    async def cmd_create_booking(self, args) -> int:
        """Create a booking."""
        attendee = {
            "name": args.attendee_name,
            "email": args.attendee_email,
            "timeZone": args.attendee_timezone,
        }
        if args.attendee_phone:
            attendee["phoneNumber"] = args.attendee_phone
        if args.attendee_language:
            attendee["language"] = args.attendee_language

        responses = json.loads(args.responses) if args.responses else None
        metadata = json.loads(args.metadata) if args.metadata else None

        result = await self.client.create_booking(
            start=args.start,
            attendee=attendee,
            event_type_id=args.event_type_id,
            event_type_slug=args.event_type_slug,
            username=args.username,
            organization_slug=args.org_slug,
            responses=responses,
            metadata=metadata,
            idempotency_key=args.idempotency_key,
            instant=args.instant,
            recurrence_count=args.recurrence_count,
            seat_reference=args.seat_reference,
        )

        self.client.output(result)
        return 0

    async def cmd_list_bookings(self, args) -> int:
        """List bookings."""
        result = await self.client.list_bookings(
            status=args.status,
            start_time=args.start_time,
            end_time=args.end_time,
            attendee_email=args.attendee_email,
            page=args.page,
            limit=args.limit,
        )
        self.client.output(result)
        return 0

    async def cmd_get_booking(self, args) -> int:
        """Get a booking."""
        booking_id = int(args.booking_id) if args.booking_id.isdigit() else args.booking_id
        result = await self.client.get_booking(booking_id)
        self.client.output(result)
        return 0

    async def cmd_cancel_booking(self, args) -> int:
        """Cancel a booking."""
        booking_id = int(args.booking_id) if args.booking_id.isdigit() else args.booking_id
        result = await self.client.cancel_booking(
            booking_id=booking_id,
            cancel_reason=args.reason,
            canceler=args.canceler,
        )
        self.client.output(result)
        return 0

    async def cmd_reschedule_booking(self, args) -> int:
        """Reschedule a booking."""
        booking_id = int(args.booking_id) if args.booking_id.isdigit() else args.booking_id
        result = await self.client.reschedule_booking(
            booking_id=booking_id,
            start_time=args.start_time,
            end_time=args.end_time,
        )
        self.client.output(result)
        return 0

    async def cmd_create_event_type(self, args) -> int:
        """Create an event type."""
        with open(args.config_file) as f:
            config = json.load(f)

        if args.title:
            config["title"] = args.title
        if args.slug:
            config["slug"] = args.slug
        if args.length:
            config["lengthInMinutes"] = args.length

        result = await self.client.create_event_type(config)
        self.client.output(result)
        return 0

    async def cmd_list_event_types(self, args) -> int:
        """List event types."""
        result = await self.client.list_event_types(
            username=args.username,
            team_slug=args.team_slug,
            organization_slug=args.org_slug,
            page=args.page,
            limit=args.limit,
        )
        self.client.output(result)
        return 0

    async def cmd_get_event_type(self, args) -> int:
        """Get event type."""
        result = await self.client.get_event_type(args.event_type_id)
        self.client.output(result)
        return 0

    async def cmd_update_event_type(self, args) -> int:
        """Update event type."""
        with open(args.config_file) as f:
            config = json.load(f)

        result = await self.client.update_event_type(args.event_type_id, config)
        self.client.output(result)
        return 0

    async def cmd_delete_event_type(self, args) -> int:
        """Delete event type."""
        result = await self.client.delete_event_type(args.event_type_id)
        self.client.output(result)
        return 0

    async def cmd_create_schedule(self, args) -> int:
        """Create a schedule."""
        with open(args.config_file) as f:
            config = json.load(f)

        if args.name:
            config["name"] = args.name
        if args.timezone:
            config["timeZone"] = args.timezone
        if args.default:
            config["isDefault"] = True

        result = await self.client.create_schedule(config)
        self.client.output(result)
        return 0

    async def cmd_list_schedules(self, args) -> int:
        """List schedules."""
        result = await self.client.list_schedules()
        self.client.output(result)
        return 0

    async def cmd_get_schedule(self, args) -> int:
        """Get schedule."""
        result = await self.client.get_schedule(args.schedule_id)
        self.client.output(result)
        return 0

    async def cmd_update_schedule(self, args) -> int:
        """Update schedule."""
        with open(args.config_file) as f:
            config = json.load(f)

        result = await self.client.update_schedule(args.schedule_id, config)
        self.client.output(result)
        return 0

    async def cmd_delete_schedule(self, args) -> int:
        """Delete schedule."""
        result = await self.client.delete_schedule(args.schedule_id)
        self.client.output(result)
        return 0

    async def cmd_check_availability(self, args) -> int:
        """Check availability."""
        query = {
            "startTime": args.start_time,
            "endTime": args.end_time,
            "timeZone": args.timezone,
        }
        if args.event_type_id:
            query["eventTypeId"] = args.event_type_id
        if args.event_type_slug:
            query["eventTypeSlug"] = args.event_type_slug
        if args.username:
            query["username"] = args.username
        if args.team_slug:
            query["teamSlug"] = args.team_slug
        if args.org_slug:
            query["organizationSlug"] = args.org_slug

        result = await self.client.get_availability(query)
        self.client.output(result)
        return 0

    async def cmd_setup_webhook(self, args) -> int:
        """Create webhook."""
        result = await self.client.create_webhook(
            url=args.url,
            events=args.events,
            secret=args.secret,
            active=not args.inactive,
        )
        self.client.output(result)
        return 0

    async def cmd_list_webhooks(self, args) -> int:
        """List webhooks."""
        result = await self.client.list_webhooks()
        self.client.output(result)
        return 0

    async def cmd_get_webhook(self, args) -> int:
        """Get webhook."""
        result = await self.client.get_webhook(args.webhook_id)
        self.client.output(result)
        return 0

    async def cmd_update_webhook(self, args) -> int:
        """Update webhook."""
        result = await self.client.update_webhook(
            webhook_id=args.webhook_id,
            url=args.url,
            events=args.events,
            secret=args.secret,
            active=args.active,
        )
        self.client.output(result)
        return 0

    async def cmd_delete_webhook(self, args) -> int:
        """Delete webhook."""
        result = await self.client.delete_webhook(args.webhook_id)
        self.client.output(result)
        return 0

    async def cmd_test_auth(self, args) -> int:
        """Test authentication."""
        result = await self.client.test_auth()
        self.client.output({"status": "success", "user": result})
        return 0

    async def cmd_verify_webhook(self, args) -> int:
        """Verify webhook signature."""
        with open(args.payload_file, "rb") as f:
            payload = f.read()

        try:
            valid = CalComClient.verify_webhook_signature(
                payload=payload,
                signature_header=args.signature,
                timestamp_header=args.timestamp,
                secret=args.secret,
            )
            self.client.output({"valid": valid})
            return 0 if valid else 1
        except ValueError as e:
            self.client.output({"valid": False, "error": str(e)})
            return 1


def main():
    """Main CLI entry point."""
    # Parse args first to get auth info
    parser = argparse.ArgumentParser(
        prog="cal-booking",
        description="Cal.com Booking Skill CLI - Manage bookings, event types, and schedules",
        add_help=False  # We'll add help after parsing
    )
    parser.add_argument(
        "--api-key",
        help="Cal.com API key (cal_ or cal_live_ prefix)",
    )
    parser.add_argument(
        "--oauth-token",
        help="OAuth 2.0 access token",
    )
    parser.add_argument(
        "--auth-method",
        choices=["api_key", "oauth2_pkce", "platform"],
        default="api_key",
        help="Authentication method",
    )
    parser.add_argument(
        "--base-url",
        default="https://api.cal.com/v2/",
        help="Cal.com API base URL",
    )
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=120,
        help="Requests per minute limit",
    )
    parser.add_argument(
        "--output",
        choices=["json", "yaml", "table", "text"],
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Disable request/response validation",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show help",
    )

    # Parse known args first to get auth config
    known_args, remaining = parser.parse_known_args()

    # Show help if requested - do this BEFORE creating client
    if known_args.help:
        # Create full parser and show help
        from .api_client import CalComClient, AuthMethod, OutputFormat, OutputManager
        from .validation import validate_request, validate_response
        # Create a temporary client to get the full parser with all subcommands
        # Use dummy auth since we just need the parser
        temp_client = CalComClient(api_key="dummy_for_help")
        temp_cli = CLI(temp_client)
        full_parser = temp_cli.create_parser()
        full_parser.print_help()
        return 0

    # Create client with auth from args (only if not showing help)
    from .api_client import CalComClient, AuthMethod, OutputFormat, OutputManager
    from .validation import validate_request, validate_response

    auth_method = AuthMethod.API_KEY
    if known_args.auth_method == "oauth2_pkce":
        auth_method = AuthMethod.OAUTH2_PKCE
    elif known_args.auth_method == "platform":
        auth_method = AuthMethod.PLATFORM

    client = CalComClient(
        api_key=known_args.api_key,
        oauth_token=known_args.oauth_token,
        auth_method=auth_method,
        base_url=known_args.base_url,
        rate_limit=known_args.rate_limit,
    )
    if known_args.no_validate:
        client.validate_requests = False
        client.validate_responses = False
    client.set_output_format(OutputFormat(known_args.output))

    cli = CLI(client)
    return cli.run(remaining)


if __name__ == "__main__":
    sys.exit(main())