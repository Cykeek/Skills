"""
Integration Tests
=================
End-to-end tests for the cal_booking_skill package.
"""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from cal_booking_skill.api_client import CalComClient, AuthMethod
from cal_booking_skill.validation import validate_request, validate_response
from cal_booking_skill.output_manager import OutputManager, OutputFormat


class TestIntegrationBookingFlow:
    """Integration tests for complete booking flow."""

    @pytest.fixture
    def client(self):
        return CalComClient(
            api_key="cal_test_123",
            validate_requests=True,
            validate_responses=True,
        )

    @pytest.mark.asyncio
    async def test_complete_booking_flow(self, client):
        """Test complete booking creation and retrieval flow."""
        # Mock responses
        booking_response = {
            "id": 12345,
            "uid": "abc123",
            "title": "30min Meeting with John Doe",
            "startTime": "2026-07-20T14:00:00Z",
            "endTime": "2026-07-20T14:30:00Z",
            "status": "ACCEPTED",
            "attendees": [{
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "timeZone": "America/Los_Angeles",
                "phoneNumber": None,
                "language": None,
                "metadata": {}
            }],
            "organizer": {
                "id": 100,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "timeZone": "UTC"
            },
            "eventType": {
                "id": 12345,
                "title": "30min Meeting",
                "slug": "30min",
                "lengthInMinutes": 30
            },
            "location": "https://meet.google.com/abc-def-ghi",
            "metadata": {},
            "createdAt": "2026-07-15T10:00:00Z",
            "updatedAt": "2026-07-15T10:00:00Z"
        }

        list_response = {
            "bookings": [booking_response],
            "pagination": {"page": 1, "limit": 50, "total": 1}
        }

        client._client = AsyncMock()
        client._client.request.side_effect = [
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": booking_response}),
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": list_response}),
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": booking_response}),
        ]

        # Create booking
        created = await client.create_booking(
            start="2026-07-20T14:00:00Z",
            attendee={
                "name": "John Doe",
                "email": "john@example.com",
                "timeZone": "America/Los_Angeles",
            },
            event_type_id=12345,
        )

        assert created["id"] == 12345
        assert created["status"] == "ACCEPTED"

        # List bookings
        listed = await client.list_bookings(status="ACCEPTED")
        assert len(listed["bookings"]) == 1

        # Get booking
        retrieved = await client.get_booking(12345)
        assert retrieved["uid"] == "abc123"


class TestIntegrationEventTypeFlow:
    """Integration tests for event type management flow."""

    @pytest.fixture
    def client(self):
        return CalComClient(
            api_key="cal_test_123",
            validate_requests=True,
            validate_responses=True,
        )

    @pytest.mark.asyncio
    async def test_event_type_crud(self, client):
        """Test create, read, update, delete event type flow."""
        config = {
            "title": "Team Sync",
            "slug": "team-sync",
            "lengthInMinutes": 30,
            "description": "Weekly team sync",
        }

        created = {**config, "id": 1, "createdAt": "2026-07-15T10:00:00Z"}
        updated = {**created, "title": "Updated Team Sync"}
        listed = {"eventTypes": [created], "pagination": {"page": 1}}

        client._client = AsyncMock()
        client._client.request.side_effect = [
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": created}),
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": listed}),
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": created}),
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": updated}),
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": {"deleted": True}}),
        ]

        # Create
        result = await client.create_event_type(config)
        assert result["id"] == 1

        # List
        result = await client.list_event_types()
        assert len(result["eventTypes"]) == 1

        # Get
        result = await client.get_event_type(1)
        assert result["slug"] == "team-sync"

        # Update
        result = await client.update_event_type(1, {"title": "Updated Team Sync"})
        assert result["title"] == "Updated Team Sync"

        # Delete
        result = await client.delete_event_type(1)
        assert result["deleted"] is True


class TestIntegrationWebhookFlow:
    """Integration tests for webhook handling."""

    @pytest.fixture
    def client(self):
        return CalComClient(api_key="cal_test_123")

    @pytest.mark.asyncio
    async def test_webhook_create_and_verify(self, client):
        """Test webhook creation and signature verification."""
        import hmac
        import hashlib
        import time

        # Create webhook
        webhook_data = {
            "id": 1,
            "url": "https://example.com/webhook",
            "events": ["BOOKING_CREATED", "BOOKING_CANCELLED"],
            "secret": "webhook_secret_123",
            "active": True,
        }

        client._client = AsyncMock()
        client._client.request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "success", "data": webhook_data}
        )

        created = await client.create_webhook(
            url="https://example.com/webhook",
            events=["BOOKING_CREATED", "BOOKING_CANCELLED"],
            secret="webhook_secret_123",
        )

        assert created["id"] == 1
        assert created["secret"] == "webhook_secret_123"

        # Verify webhook signature
        payload = json.dumps({
            "triggerEvent": "BOOKING_CREATED",
            "createdAt": "2026-07-15T10:00:00Z",
            "payload": {"uid": "abc123"}
        }).encode()

        timestamp = str(int(time.time()))
        signature = hmac.new(
            "webhook_secret_123".encode(),
            f"{timestamp}.{payload.decode()}".encode(),
            hashlib.sha256,
        ).hexdigest()

        valid = CalComClient.verify_webhook_signature(
            payload=payload,
            signature_header=signature,
            timestamp_header=timestamp,
            secret="webhook_secret_123",
        )

        assert valid is True


class TestIntegrationValidationFlow:
    """Integration tests for validation pipeline."""

    def test_request_validation_pipeline(self):
        """Test request validation catches errors before API call."""
        # Valid request
        valid_booking = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {
                "name": "John",
                "email": "john@example.com",
                "timeZone": "America/Los_Angeles",
            },
            "event_type_id": 123,
        }
        validate_request("booking-request", valid_booking)  # Should not raise

        # Invalid request - should raise
        invalid_booking = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {
                "name": "John",
                # missing email and timeZone
            },
        }
        with pytest.raises(Exception):
            validate_request("booking-request", invalid_booking)

    def test_response_validation_pipeline(self, sample_booking_response):
        """Test response validation."""
        validate_response("booking-response", sample_booking_response)


class TestIntegrationOutputModes:
    """Integration tests for dual output modes."""

    def test_cli_mode_output(self):
        """Test CLI mode output formatting."""
        from io import StringIO
        stream = StringIO()
        manager = OutputManager(format=OutputFormat.JSON, stream=stream, color=False, agent_mode=False)
        manager.output({"status": "success", "data": {"id": 1}})
        output = stream.getvalue()
        parsed = json.loads(output.strip())
        assert parsed["data"]["id"] == 1
        assert "timestamp" not in parsed  # CLI mode doesn't add envelope

    def test_agent_mode_output(self):
        """Test agent mode output formatting."""
        from io import StringIO
        stream = StringIO()
        manager = OutputManager(format=OutputFormat.JSON, stream=stream, color=False, agent_mode=True)
        manager.output({"status": "success", "data": {"id": 1}})
        output = stream.getvalue()
        parsed = json.loads(output.strip())
        assert "timestamp" in parsed
        assert "format_version" in parsed
        assert parsed["data"]["data"]["id"] == 1


class TestIntegrationErrorHandling:
    """Integration tests for error handling."""

    @pytest.fixture
    def client(self):
        return CalComClient(api_key="cal_test_123", validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_auth_error_handling(self, client):
        """Test authentication error handling."""
        client._client = AsyncMock()
        client._client.request.return_value = MagicMock(
            status_code=401,
            json=lambda: {
                "status": "error",
                "data": {"message": "Invalid API key", "code": "invalid_api_key"}
            }
        )

        from cal_booking_skill.api_client import AuthError
        with pytest.raises(AuthError) as exc:
            await client.test_auth()

        assert exc.value.code == "invalid_api_key"
        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    async def test_rate_limit_handling(self, client):
        """Test rate limit handling with retry."""
        client._client = AsyncMock()
        client._client.request.side_effect = [
            MagicMock(
                status_code=429,
                json=lambda: {"status": "error", "data": {"message": "Rate limited", "code": "rate_limit_exceeded"}},
                headers={"Retry-After": "1"}
            ),
            MagicMock(
                status_code=200,
                json=lambda: {"status": "success", "data": {"id": 1}}
            ),
        ]

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await client._request("GET", "/test")
            assert result == {"id": 1}

    @pytest.mark.asyncio
    async def test_not_found_handling(self, client):
        """Test not found error handling."""
        client._client = AsyncMock()
        client._client.request.return_value = MagicMock(
            status_code=404,
            json=lambda: {"status": "error", "data": {"message": "Not found", "code": "not_found"}}
        )

        from cal_booking_skill.api_client import NotFoundError
        with pytest.raises(NotFoundError) as exc:
            await client.get_booking(999999)

        assert exc.value.code == "not_found"


class TestIntegrationIdempotency:
    """Integration tests for idempotency handling."""

    @pytest.fixture
    def client(self):
        return CalComClient(api_key="cal_test_123", validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_idempotency_key_generation(self, client):
        """Test automatic idempotency key generation."""
        client._client = AsyncMock()
        client._client.request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "success", "data": {"id": 1}}
        )

        await client.create_booking(
            start="2026-07-20T14:00:00Z",
            attendee={"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            event_type_id=123,
        )

        # Check that Idempotency-Key header was added
        call_args = client._client.request.call_args
        headers = call_args[1]["headers"]
        assert "Idempotency-Key" in headers
        # Should be valid UUID
        import uuid
        uuid.UUID(headers["Idempotency-Key"])

    @pytest.mark.asyncio
    async def test_custom_idempotency_key(self, client):
        """Test custom idempotency key."""
        custom_key = "550e8400-e29b-41d4-a716-446655440000"
        client._client = AsyncMock()
        client._client.request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "success", "data": {"id": 1}}
        )

        await client.create_booking(
            start="2026-07-20T14:00:00Z",
            attendee={"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            event_type_id=123,
            idempotency_key=custom_key,
        )

        call_args = client._client.request.call_args
        headers = call_args[1]["headers"]
        assert headers["Idempotency-Key"] == custom_key

    @pytest.mark.asyncio
    async def test_duplicate_idempotency_key_rejected(self, client):
        """Test duplicate idempotency key is rejected client-side."""
        custom_key = "550e8400-e29b-41d4-a716-446655440000"
        client._client = AsyncMock()
        client._client.request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "success", "data": {"id": 1}}
        )

        # First request
        await client.create_booking(
            start="2026-07-20T14:00:00Z",
            attendee={"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            event_type_id=123,
            idempotency_key=custom_key,
        )

        # Second request with same key should fail
        from cal_booking_skill.api_client import ValidationError
        with pytest.raises(ValidationError) as exc:
            await client.create_booking(
                start="2026-07-20T14:00:00Z",
                attendee={"name": "John", "email": "j@example.com", "timeZone": "UTC"},
                event_type_id=123,
                idempotency_key=custom_key,
            )

        assert "already used" in str(exc.value)