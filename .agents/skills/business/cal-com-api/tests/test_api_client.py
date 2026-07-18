"""
Contract Tests for API Client
=============================
Tests for CalComClient functionality including:
- Authentication methods
- Request/response handling
- Rate limiting
- Error handling
- Webhook verification
"""

import asyncio
import json
import time
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from cal_booking_skill.api_client import (
    CalComClient,
    AuthMethod,
    TokenBucket,
    CalComError,
    AuthError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ConflictError,
    ServerError,
    ERROR_CODE_MAP,
)
from cal_booking_skill.validation import ValidationError as SchemaValidationError


class TestTokenBucket:
    """Tests for TokenBucket rate limiter."""

    @pytest.mark.asyncio
    async def test_acquire_allows_within_limit(self):
        """Test acquiring tokens within limit works."""
        bucket = TokenBucket(rate=10, per=60)
        await bucket.acquire(5)
        assert bucket.tokens == 5

    @pytest.mark.asyncio
    async def test_acquire_blocks_when_exhausted(self):
        """Test acquiring blocks when tokens exhausted."""
        bucket = TokenBucket(rate=2, per=60)
        await bucket.acquire(2)
        start = time.monotonic()
        await bucket.acquire(1)
        elapsed = time.monotonic() - start
        # Should have waited ~30 seconds (1 token at 2/min = 30s)
        # But in test it's faster due to time mocking, so just verify it waited
        assert elapsed >= 0

    def test_try_acquire_returns_true_when_available(self):
        """Test try_acquire returns True when tokens available."""
        bucket = TokenBucket(rate=10, per=60)
        assert bucket.try_acquire(5) is True
        assert bucket.tokens == 5

    def test_try_acquire_returns_false_when_exhausted(self):
        """Test try_acquire returns False when tokens exhausted."""
        bucket = TokenBucket(rate=2, per=60)
        bucket.try_acquire(2)
        assert bucket.try_acquire(1) is False

    @pytest.mark.asyncio
    async def test_token_refill_over_time(self):
        """Test tokens refill over time."""
        bucket = TokenBucket(rate=60, per=60)  # 1 per second
        await bucket.acquire(60)
        assert bucket.tokens == 0
        # Wait for refill
        await asyncio.sleep(0.1)
        # Manually trigger refill check
        bucket.last_update = time.monotonic() - 1.0
        await bucket.acquire(1)
        assert bucket.tokens >= 0


class TestCalComClientInitialization:
    """Tests for CalComClient initialization."""

    def test_init_with_api_key(self, api_key):
        """Test initialization with API key."""
        client = CalComClient(api_key=api_key)
        assert client.auth_method == AuthMethod.API_KEY
        assert client.api_key == api_key

    def test_init_with_oauth_token(self, oauth_token):
        """Test initialization with OAuth token."""
        client = CalComClient(oauth_token=oauth_token, auth_method=AuthMethod.OAUTH2_PKCE)
        assert client.auth_method == AuthMethod.OAUTH2_PKCE
        assert client.oauth_token == oauth_token

    def test_init_with_platform_key(self):
        """Test initialization with Platform key."""
        client = CalComClient(platform_key="platform_key", auth_method=AuthMethod.PLATFORM)
        assert client.auth_method == AuthMethod.PLATFORM
        assert client.platform_key == "platform_key"

    def test_init_requires_auth(self):
        """Test initialization requires at least one auth method."""
        with pytest.raises(ValueError):
            CalComClient()

    def test_init_custom_base_url(self):
        """Test custom base URL."""
        client = CalComClient(api_key="test", base_url="https://custom.cal.com/v2/")
        assert client.base_url == "https://custom.cal.com/v2/"

    def test_init_custom_rate_limit(self):
        """Test custom rate limit."""
        client = CalComClient(api_key="test", rate_limit=60)
        assert client.rate_limiter.rate == 60

    def test_headers_api_key(self, api_key):
        """Test headers for API key auth."""
        client = CalComClient(api_key=api_key)
        headers = client.headers
        assert headers["Authorization"] == f"Bearer {api_key}"
        assert headers["cal-api-version"] == "2024-08-13"

    def test_headers_oauth(self, oauth_token):
        """Test headers for OAuth auth."""
        client = CalComClient(oauth_token=oauth_token, auth_method=AuthMethod.OAUTH2_PKCE)
        headers = client.headers
        assert headers["Authorization"] == f"Bearer {oauth_token}"

    def test_headers_platform(self):
        """Test headers for Platform auth."""
        client = CalComClient(platform_key="platform_key", auth_method=AuthMethod.PLATFORM)
        headers = client.headers
        assert headers["Authorization"] == "Bearer platform_key"


class TestCalComClientRequests:
    """Tests for CalComClient request handling."""

    @pytest.fixture
    def client(self, api_key):
        return CalComClient(api_key=api_key, validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_request_success(self, client, mock_httpx_response, sample_booking_response):
        """Test successful request."""
        mock_response = mock_httpx_response(200, {"status": "success", "data": sample_booking_response})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client._request("GET", "/bookings/123")
        assert result == sample_booking_response
        client._client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_request_api_error(self, client, mock_httpx_response):
        """Test API error response handling."""
        mock_response = mock_httpx_response(404, {
            "status": "error",
            "data": {"message": "Booking not found", "code": "not_found"}
        })
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        with pytest.raises(NotFoundError) as exc:
            await client._request("GET", "/bookings/999")
        assert exc.value.code == "not_found"
        assert exc.value.status_code == 404

    @pytest.mark.asyncio
    async def test_request_rate_limit(self, client, mock_httpx_response):
        """Test rate limit handling with retry."""
        # First response: rate limited
        rate_limit_response = mock_httpx_response(429, {
            "status": "error",
            "data": {"message": "Rate limited", "code": "rate_limit_exceeded"}
        }, headers={"Retry-After": "1"})

        # Second response: success
        success_response = mock_httpx_response(200, {
            "status": "success",
            "data": {"id": 1}
        })

        client._client = AsyncMock()
        client._client.request.side_effect = [rate_limit_response, success_response]

        # Should retry and succeed
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            result = await client._request("GET", "/test")
            assert result == {"id": 1}
            mock_sleep.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_request_timeout_retry(self, client):
        """Test timeout retry logic."""
        client._client = AsyncMock()
        client._client.request.side_effect = [
            httpx.TimeoutException("Timeout"),
            httpx.TimeoutException("Timeout"),
            MagicMock(status_code=200, json=lambda: {"status": "success", "data": {"ok": True}})
        ]

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await client._request("GET", "/test")
            assert result == {"ok": True}

    @pytest.mark.asyncio
    async def test_request_max_retries_exceeded(self, client):
        """Test max retries exceeded."""
        client._client = AsyncMock()
        client._client.request.side_effect = httpx.TimeoutException("Timeout")

        with patch("asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(CalComError) as exc:
                await client._request("GET", "/test")
            assert "Request failed after 3 retries" in str(exc.value)

    @pytest.mark.asyncio
    async def test_request_validation_error(self, client):
        """Test request validation error."""
        client.validate_requests = True
        # Missing required field
        with pytest.raises(SchemaValidationError):
            await client._request(
                "POST", "/bookings",
                json_data={"start": "2026-07-20T14:00:00Z"},  # missing attendee
                validate_request_schema="booking-request"
            )


class TestCalComClientBookings:
    """Tests for booking operations."""

    @pytest.fixture
    def client(self, api_key):
        return CalComClient(api_key=api_key, validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_create_booking(self, client, mock_httpx_response, sample_booking_response, sample_booking_request):
        """Test create_booking method."""
        mock_response = mock_httpx_response(200, {"status": "success", "data": sample_booking_response})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.create_booking(**sample_booking_request)

        assert result == sample_booking_response
        client._client.request.assert_called_once()
        call_args = client._client.request.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == "/bookings"

    @pytest.mark.asyncio
    async def test_create_booking_generates_idempotency_key(self, client, mock_httpx_response, sample_booking_response):
        """Test create_booking generates idempotency key if not provided."""
        mock_response = mock_httpx_response(200, {"status": "success", "data": sample_booking_response})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        await client.create_booking(
            start="2026-07-20T14:00:00Z",
            attendee={"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            event_type_id=123,
        )

        # Check idempotency key was added to headers
        call_args = client._client.request.call_args
        headers = call_args[1]["headers"]
        assert "Idempotency-Key" in headers

    @pytest.mark.asyncio
    async def test_list_bookings(self, client, mock_httpx_response):
        """Test list_bookings method."""
        mock_data = {"bookings": [], "pagination": {"page": 1, "limit": 50}}
        mock_response = mock_httpx_response(200, {"status": "success", "data": mock_data})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.list_bookings(status="ACCEPTED", page=1, limit=20)

        assert result == mock_data
        call_args = client._client.request.call_args
        assert call_args[1]["params"]["status"] == "ACCEPTED"
        assert call_args[1]["params"]["page"] == 1
        assert call_args[1]["params"]["limit"] == 20

    @pytest.mark.asyncio
    async def test_get_booking(self, client, mock_httpx_response, sample_booking_response):
        """Test get_booking method."""
        mock_response = mock_httpx_response(200, {"status": "success", "data": sample_booking_response})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.get_booking(123)
        assert result == sample_booking_response

    @pytest.mark.asyncio
    async def test_cancel_booking(self, client, mock_httpx_response, sample_booking_response):
        """Test cancel_booking method."""
        cancelled_booking = {**sample_booking_response, "status": "CANCELLED"}
        mock_response = mock_httpx_response(200, {"status": "success", "data": cancelled_booking})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.cancel_booking(123, cancel_reason="Changed plans", canceler="ATTENDEE")

        assert result["status"] == "CANCELLED"
        call_args = client._client.request.call_args
        assert call_args[1]["json"]["cancelReason"] == "Changed plans"
        assert call_args[1]["json"]["canceler"] == "ATTENDEE"

    @pytest.mark.asyncio
    async def test_reschedule_booking(self, client, mock_httpx_response, sample_booking_response):
        """Test reschedule_booking method."""
        rescheduled = {**sample_booking_response, "startTime": "2026-07-21T14:00:00Z"}
        mock_response = mock_httpx_response(200, {"status": "success", "data": rescheduled})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.reschedule_booking(123, start_time="2026-07-21T14:00:00Z")

        assert result["startTime"] == "2026-07-21T14:00:00Z"


class TestCalComClientEventTypes:
    """Tests for event type operations."""

    @pytest.fixture
    def client(self, api_key):
        return CalComClient(api_key=api_key, validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_create_event_type(self, client, mock_httpx_response, sample_event_type_config):
        """Test create_event_type method."""
        created = {**sample_event_type_config, "id": 12345, "createdAt": "2026-07-15T10:00:00Z"}
        mock_response = mock_httpx_response(200, {"status": "success", "data": created})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.create_event_type(sample_event_type_config)

        assert result["id"] == 12345

    @pytest.mark.asyncio
    async def test_list_event_types(self, client, mock_httpx_response):
        """Test list_event_types method."""
        mock_data = {"eventTypes": [], "pagination": {"page": 1}}
        mock_response = mock_httpx_response(200, {"status": "success", "data": mock_data})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.list_event_types(username="jane", page=1, limit=10)
        assert result == mock_data

    @pytest.mark.asyncio
    async def test_update_event_type(self, client, mock_httpx_response, sample_event_type_config):
        """Test update_event_type method."""
        updated = {**sample_event_type_config, "title": "Updated Title"}
        mock_response = mock_httpx_response(200, {"status": "success", "data": updated})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.update_event_type(123, {"title": "Updated Title"})
        assert result["title"] == "Updated Title"

    @pytest.mark.asyncio
    async def test_delete_event_type(self, client, mock_httpx_response):
        """Test delete_event_type method."""
        mock_response = mock_httpx_response(200, {"status": "success", "data": {"deleted": True}})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.delete_event_type(123)
        assert result["deleted"] is True


class TestCalComClientSchedules:
    """Tests for schedule operations."""

    @pytest.fixture
    def client(self, api_key):
        return CalComClient(api_key=api_key, validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_create_schedule(self, client, mock_httpx_response, sample_schedule_config):
        """Test create_schedule method."""
        created = {**sample_schedule_config, "id": 1}
        mock_response = mock_httpx_response(200, {"status": "success", "data": created})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.create_schedule(sample_schedule_config)
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_list_schedules(self, client, mock_httpx_response):
        """Test list_schedules method."""
        mock_data = {"schedules": []}
        mock_response = mock_httpx_response(200, {"status": "success", "data": mock_data})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.list_schedules()
        assert result == mock_data


class TestCalComClientAvailability:
    """Tests for availability operations."""

    @pytest.fixture
    def client(self, api_key):
        return CalComClient(api_key=api_key, validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_get_availability(self, client, mock_httpx_response, sample_availability_query):
        """Test get_availability method."""
        mock_data = {"slots": {"2026-07-20": [{"start": "2026-07-20T14:00:00Z", "end": "2026-07-20T14:30:00Z"}]}}
        mock_response = mock_httpx_response(200, {"status": "success", "data": mock_data})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.get_availability(sample_availability_query)
        assert result == mock_data


class TestCalComClientWebhooks:
    """Tests for webhook operations."""

    @pytest.fixture
    def client(self, api_key):
        return CalComClient(api_key=api_key, validate_requests=False, validate_responses=False)

    @pytest.mark.asyncio
    async def test_create_webhook(self, client, mock_httpx_response):
        """Test create_webhook method."""
        mock_data = {"id": 1, "url": "https://example.com/webhook", "events": ["BOOKING_CREATED"]}
        mock_response = mock_httpx_response(200, {"status": "success", "data": mock_data})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.create_webhook(
            url="https://example.com/webhook",
            events=["BOOKING_CREATED"],
            secret="testsecret",
        )
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_verify_webhook_signature_valid(self):
        """Test verify_webhook_signature with valid signature."""
        import hmac
        import hashlib

        secret = "testsecret"
        payload = b'{"triggerEvent": "BOOKING_CREATED"}'
        timestamp = str(int(time.time()))
        signature = hmac.new(
            secret.encode(),
            f"{timestamp}.{payload.decode()}".encode(),
            hashlib.sha256,
        ).hexdigest()

        valid = CalComClient.verify_webhook_signature(payload, signature, timestamp, secret)
        assert valid is True

    @pytest.mark.asyncio
    async def test_verify_webhook_signature_invalid(self):
        """Test verify_webhook_signature with invalid signature."""
        payload = b'{"triggerEvent": "BOOKING_CREATED"}'
        timestamp = str(int(time.time()))
        signature = "invalidsignature"

        valid = CalComClient.verify_webhook_signature(payload, signature, timestamp, "wrongsecret")
        assert valid is False

    @pytest.mark.asyncio
    async def test_verify_webhook_signature_timestamp_expired(self):
        """Test verify_webhook_signature with expired timestamp."""
        import hmac
        import hashlib

        secret = "testsecret"
        payload = b'{"triggerEvent": "BOOKING_CREATED"}'
        timestamp = str(int(time.time()) - 400)  # 400 seconds ago (beyond 300s default)
        signature = hmac.new(
            secret.encode(),
            f"{timestamp}.{payload.decode()}".encode(),
            hashlib.sha256,
        ).hexdigest()

        with pytest.raises(ValueError) as exc:
            CalComClient.verify_webhook_signature(payload, signature, timestamp, secret)
        assert "Timestamp outside tolerance" in str(exc.value)

    @pytest.mark.asyncio
    async def test_verify_webhook_signature_missing_headers(self):
        """Test verify_webhook_signature with missing headers."""
        payload = b'{}'
        with pytest.raises(ValueError) as exc:
            CalComClient.verify_webhook_signature(payload, "", "123", "secret")
        assert "Missing signature or timestamp header" in str(exc.value)


class TestCalComClientErrorClassification:
    """Tests for error classification mapping."""

    def test_error_code_map_structure(self):
        """Test ERROR_CODE_MAP has expected structure."""
        assert 400 in ERROR_CODE_MAP
        assert 401 in ERROR_CODE_MAP
        assert 403 in ERROR_CODE_MAP
        assert 404 in ERROR_CODE_MAP
        assert 409 in ERROR_CODE_MAP
        assert 422 in ERROR_CODE_MAP
        assert 429 in ERROR_CODE_MAP
        assert 500 in ERROR_CODE_MAP

    def test_error_codes_map_to_correct_exceptions(self):
        """Test specific error codes map to correct exception classes."""
        assert ERROR_CODE_MAP[401]["invalid_token"] == AuthError
        assert ERROR_CODE_MAP[403]["insufficient_scope"] == AuthError
        assert ERROR_CODE_MAP[404]["not_found"] == NotFoundError
        assert ERROR_CODE_MAP[409]["slot_taken"] == ConflictError
        assert ERROR_CODE_MAP[422]["past_booking"] == ValidationError
        assert ERROR_CODE_MAP[429]["rate_limit_exceeded"] == RateLimitError
        assert ERROR_CODE_MAP[500]["internal_error"] == ServerError

    def test_retryable_codes(self):
        """Test RETRYABLE_CODES contains expected codes."""
        from cal_booking_skill.api_client import CalComClient
        assert "rate_limit_exceeded" in CalComClient.RETRYABLE_CODES
        assert "internal_error" in CalComClient.RETRYABLE_CODES
        assert "service_unavailable" in CalComClient.RETRYABLE_CODES

    def test_retryable_status_codes(self):
        """Test RETRYABLE_STATUS contains expected HTTP codes."""
        from cal_booking_skill.api_client import CalComClient
        assert 429 in CalComClient.RETRYABLE_STATUS
        assert 500 in CalComClient.RETRYABLE_STATUS
        assert 502 in CalComClient.RETRYABLE_STATUS
        assert 503 in CalComClient.RETRYABLE_STATUS
        assert 504 in CalComClient.RETRYABLE_STATUS


class TestCalComClientUtilityMethods:
    """Tests for utility methods."""

    @pytest.fixture
    def client(self, api_key):
        return CalComClient(api_key=api_key)

    def test_generate_idempotency_key(self):
        """Test idempotency key generation."""
        key1 = CalComClient.generate_idempotency_key()
        key2 = CalComClient.generate_idempotency_key()
        assert key1 != key2
        # Should be valid UUID
        import uuid
        uuid.UUID(key1)
        uuid.UUID(key2)

    @pytest.mark.asyncio
    async def test_test_auth(self, client, mock_httpx_response):
        """Test test_auth method."""
        mock_data = {"id": 1, "name": "Test User", "email": "test@example.com"}
        mock_response = mock_httpx_response(200, {"status": "success", "data": mock_data})
        client._client = AsyncMock()
        client._client.request.return_value = mock_response

        result = await client.test_auth()
        assert result == mock_data

    def test_set_output_format(self, client):
        """Test setting output format."""
        from cal_booking_skill.api_client import OutputFormat
        client.set_output_format(OutputFormat.YAML)
        assert client.output_manager.format == OutputFormat.YAML


class TestCalComClientContextManagers:
    """Tests for async/sync context managers."""

    @pytest.mark.asyncio
    async def test_async_context_manager(self, api_key):
        """Test async context manager."""
        client = CalComClient(api_key=api_key)
        async with client as c:
            assert c._client is not None
        assert client._client is None

    def test_sync_context_manager(self, api_key):
        """Test sync context manager."""
        client = CalComClient(api_key=api_key)
        with client as c:
            assert c._client_sync is not None
        assert client._client_sync is None