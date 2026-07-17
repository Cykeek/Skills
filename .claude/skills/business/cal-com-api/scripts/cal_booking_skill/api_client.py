"""
Cal.com API Client
==================
Production-ready Cal.com API v2 client with:
- Three authentication methods (API Key, OAuth 2.0 PKCE, Platform)
- Token bucket rate limiting (120 req/min default)
- Schema-first validation
- Comprehensive error handling with retry logic
- Async webhook processing support
"""

import asyncio
import hashlib
import hmac
import json
import time
import uuid
from . import __version__
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
import jsonschema

from .validation import validate_request, validate_response, ValidationError as SchemaValidationError
from .output_manager import OutputManager, OutputFormat


class AuthMethod(Enum):
    """Authentication methods supported by Cal.com API v2."""
    API_KEY = "api_key"
    OAUTH2_PKCE = "oauth2_pkce"
    PLATFORM = "platform"  # Deprecated but supported


class CalComError(Exception):
    """Base exception for Cal.com API errors."""

    def __init__(self, message: str, code: str = "unknown", details: Dict = None, status_code: int = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code


class AuthError(CalComError):
    """Authentication/authorization errors (401, 403)."""
    pass


class RateLimitError(CalComError):
    """Rate limit exceeded (429)."""

    def __init__(self, message: str, retry_after: int = 60, **kwargs):
        super().__init__(message, code="rate_limit_exceeded", **kwargs)
        self.retry_after = retry_after


class ValidationError(CalComError):
    """Request validation errors (400, 422)."""
    pass


class NotFoundError(CalComError):
    """Resource not found (404)."""
    pass


class ConflictError(CalComError):
    """Resource conflict (409)."""
    pass


class ServerError(CalComError):
    """Server errors (5xx)."""
    pass


# Error classification mapping
ERROR_CODE_MAP = {
    400: {
        "validation_error": ValidationError,
        "invalid_json": ValidationError,
        "missing_required_field": ValidationError,
    },
    401: {
        "unauthorized": AuthError,
        "invalid_token": AuthError,
        "token_expired": AuthError,
        "invalid_api_key": AuthError,
    },
    403: {
        "insufficient_scope": AuthError,
        "team_access_denied": AuthError,
        "organization_access_denied": AuthError,
    },
    404: {
        "not_found": NotFoundError,
    },
    409: {
        "conflict": ConflictError,
        "duplicate_webhook": ConflictError,
        "slot_taken": ConflictError,
    },
    422: {
        "unprocessable_entity": ValidationError,
        "invalid_timezone": ValidationError,
        "past_booking": ValidationError,
        "booking_window_exceeded": ValidationError,
        "minimum_notice_not_met": ValidationError,
        "maximum_attendees_exceeded": ValidationError,
        "recurring_booking_invalid": ValidationError,
    },
    429: {
        "rate_limit_exceeded": RateLimitError,
    },
    500: {
        "internal_error": ServerError,
    },
    503: {
        "service_unavailable": ServerError,
    },
}


class TokenBucket:
    """Token bucket rate limiter for client-side rate limiting."""

    def __init__(self, rate: int = 120, per: int = 60):
        """
        Initialize token bucket.

        Args:
            rate: Maximum requests per period
            per: Period in seconds
        """
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> None:
        """Acquire tokens, blocking until available."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(self.rate, self.tokens + elapsed * self.rate / self.per)

            if self.tokens >= tokens:
                self.tokens -= tokens
                self.last_update = now
                return

            # Wait for tokens
            wait_time = (tokens - self.tokens) * self.per / self.rate
            await asyncio.sleep(wait_time)
            self.tokens = 0
            self.last_update = time.monotonic()

    def try_acquire(self, tokens: int = 1) -> bool:
        """Try to acquire tokens without blocking."""
        now = time.monotonic()
        elapsed = now - self.last_update
        self.tokens = min(self.rate, self.tokens + elapsed * self.rate / self.per)

        if self.tokens >= tokens:
            self.tokens -= tokens
            self.last_update = now
            return True
        return False


class CalComClient:
    """
    Cal.com API v2 Client.

    Supports three authentication methods:
    - API Key (cal_/cal_live_ prefix)
    - OAuth 2.0 with PKCE
    - Platform API (deprecated but supported)

    Features:
    - Token bucket rate limiting (120 req/min default)
    - Automatic retry with exponential backoff
    - Schema-first request/response validation
    - Webhook signature verification
    - Idempotency key support
    """

    BASE_URL = "https://api.cal.com/v2/"
    DEFAULT_RATE_LIMIT = 120  # requests per minute
    DEFAULT_TIMEOUT = 30.0  # seconds

    # Error codes that should trigger retry
    RETRYABLE_CODES = {
        "rate_limit_exceeded",
        "internal_error",
        "service_unavailable",
    }

    # HTTP status codes that should trigger retry
    RETRYABLE_STATUS = {429, 500, 502, 503, 504}

    def __init__(
        self,
        api_key: str = None,
        oauth_token: str = None,
        platform_key: str = None,
        auth_method: AuthMethod = AuthMethod.API_KEY,
        base_url: str = None,
        rate_limit: int = DEFAULT_RATE_LIMIT,
        timeout: float = DEFAULT_TIMEOUT,
        api_version: str = "2024-08-13",
        output_manager: OutputManager = None,
        validate_requests: bool = True,
        validate_responses: bool = True,
    ):
        """
        Initialize Cal.com client.

        Args:
            api_key: API key (cal_ or cal_live_ prefix)
            oauth_token: OAuth 2.0 access token
            platform_key: Platform API key (deprecated)
            auth_method: Authentication method to use
            base_url: Custom base URL (for self-hosted)
            rate_limit: Requests per minute limit
            timeout: Request timeout in seconds
            api_version: Cal.com API version header
            output_manager: Output manager for structured output
            validate_requests: Enable request schema validation
            validate_responses: Enable response schema validation
        """
        self.auth_method = auth_method
        self.api_key = api_key
        self.oauth_token = oauth_token
        self.platform_key = platform_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.api_version = api_version
        self.output_manager = output_manager or OutputManager(OutputFormat.JSON)
        self.validate_requests = validate_requests
        self.validate_responses = validate_responses

        # Rate limiter
        self.rate_limiter = TokenBucket(rate=rate_limit, per=60)

        # HTTP client
        self._client: Optional[httpx.AsyncClient] = None
        self._client_sync: Optional[httpx.Client] = None

        # Idempotency tracking
        self._idempotency_keys: set = set()

    def _require_auth(self) -> None:
        """Validate that authentication is configured for API calls."""
        if not any([self.api_key, self.oauth_token, self.platform_key]):
            raise ValueError("At least one authentication method must be provided for API calls")

    @property
    def headers(self) -> Dict[str, str]:
        """Get request headers based on auth method."""
        headers = {
            "cal-api-version": self.api_version,
            "Content-Type": "application/json",
            "User-Agent": f"cal-booking-skill/{__version__}",
        }

        if self.auth_method == AuthMethod.API_KEY and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif self.auth_method == AuthMethod.OAUTH2_PKCE and self.oauth_token:
            headers["Authorization"] = f"Bearer {self.oauth_token}"
        elif self.auth_method == AuthMethod.PLATFORM and self.platform_key:
            headers["Authorization"] = f"Bearer {self.platform_key}"

        return headers

    async def __aenter__(self) -> "CalComClient":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def __enter__(self) -> "CalComClient":
        """Sync context manager entry."""
        self._client_sync = httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Sync context manager exit."""
        if self._client_sync:
            self._client_sync.close()
            self._client_sync = None

    def _get_client(self, async_mode: bool = True) -> Union[httpx.AsyncClient, httpx.Client]:
        """Get HTTP client, creating if needed."""
        if async_mode:
            if not self._client:
                self._client = httpx.AsyncClient(
                    base_url=self.base_url,
                    headers=self.headers,
                    timeout=self.timeout,
                )
            return self._client
        else:
            if not self._client_sync:
                self._client_sync = httpx.Client(
                    base_url=self.base_url,
                    headers=self.headers,
                    timeout=self.timeout,
                )
            return self._client_sync

    async def _request(
        self,
        method: str,
        path: str,
        params: Dict = None,
        json_data: Dict = None,
        idempotency_key: str = None,
        validate_request_schema: str = None,
        validate_response_schema: str = None,
    ) -> Dict:
        """
        Make HTTP request with rate limiting, validation, and error handling.
        """
        # Validate authentication before making API calls
        self._require_auth()

        # Rate limiting
        await self.rate_limiter.acquire()

        # Request validation
        if self.validate_requests and validate_request_schema and json_data:
            validate_request(validate_request_schema, json_data)

        # Prepare headers
        headers = dict(self.headers)
        if idempotency_key:
            if idempotency_key in self._idempotency_keys:
                raise ValidationError(f"Idempotency key already used: {idempotency_key}")
            headers["Idempotency-Key"] = idempotency_key
            self._idempotency_keys.add(idempotency_key)

        client = self._get_client(async_mode=True)

        # Retry logic
        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries + 1):
            try:
                response = await client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_data,
                    headers=headers,
                )

                # Handle rate limit headers
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    raise RateLimitError(
                        "Rate limit exceeded",
                        retry_after=retry_after,
                        status_code=429,
                    )

                # Parse response
                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    response_data = {"status": "error", "data": {"message": response.text, "code": "invalid_json"}}

                # Check for API error envelope
                if response_data.get("status") == "error":
                    error_data = response_data.get("data", {})
                    error_code = error_data.get("code", "unknown")
                    error_message = error_data.get("message", "Unknown error")
                    error_details = error_data.get("details")

                    # Classify error
                    error_class = ERROR_CODE_MAP.get(response.status_code, {}).get(
                        error_code, CalComError
                    )

                    # Special handling for rate limit
                    if response.status_code == 429:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        raise RateLimitError(
                            error_message,
                            retry_after=retry_after,
                            code=error_code,
                            details=error_details,
                            status_code=response.status_code,
                        )

                    raise error_class(
                        error_message,
                        code=error_code,
                        details=error_details,
                        status_code=response.status_code,
                    )

                # Response validation
                if self.validate_responses and validate_response_schema and response_data.get("data"):
                    validate_response(validate_response_schema, response_data["data"])

                return response_data.get("data")

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                if attempt == max_retries:
                    raise CalComError(f"Request failed after {max_retries} retries: {e}") from e
                await asyncio.sleep(base_delay * (2 ** attempt))

            except RateLimitError as e:
                if attempt == max_retries:
                    raise
                await asyncio.sleep(e.retry_after)

            except CalComError:
                # Don't retry client errors (4xx except 429)
                raise

            except Exception as e:
                if attempt == max_retries:
                    raise CalComError(f"Unexpected error: {e}") from e
                await asyncio.sleep(base_delay * (2 ** attempt))

        raise CalComError("Max retries exceeded")

    def _request_sync(
        self,
        method: str,
        path: str,
        params: Dict = None,
        json_data: Dict = None,
        idempotency_key: str = None,
        validate_request_schema: str = None,
        validate_response_schema: str = None,
    ) -> Dict:
        """Synchronous version of _request."""
        # Validate authentication before making API calls
        self._require_auth()

        # Rate limiting (sync)
        if not self.rate_limiter.try_acquire():
            # Simple sync wait - in production use async
            time.sleep(60 / self.rate_limiter.rate)

        if self.validate_requests and validate_request_schema and json_data:
            validate_request(validate_request_schema, json_data)

        headers = dict(self.headers)
        if idempotency_key:
            if idempotency_key in self._idempotency_keys:
                raise ValidationError(f"Idempotency key already used: {idempotency_key}")
            headers["Idempotency-Key"] = idempotency_key
            self._idempotency_keys.add(idempotency_key)

        client = self._get_client(async_mode=False)

        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries + 1):
            try:
                response = client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_data,
                    headers=headers,
                )

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    raise RateLimitError(
                        "Rate limit exceeded",
                        retry_after=retry_after,
                        status_code=429,
                    )

                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    response_data = {"status": "error", "data": {"message": response.text, "code": "invalid_json"}}

                if response_data.get("status") == "error":
                    error_data = response_data.get("data", {})
                    error_code = error_data.get("code", "unknown")
                    error_message = error_data.get("message", "Unknown error")
                    error_details = error_data.get("details")

                    error_class = ERROR_CODE_MAP.get(response.status_code, {}).get(
                        error_code, CalComError
                    )

                    if response.status_code == 429:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        raise RateLimitError(
                            error_message,
                            retry_after=retry_after,
                            code=error_code,
                            details=error_details,
                            status_code=response.status_code,
                        )

                    raise error_class(
                        error_message,
                        code=error_code,
                        details=error_details,
                        status_code=response.status_code,
                    )

                if self.validate_responses and validate_response_schema and response_data.get("data"):
                    validate_response(validate_response_schema, response_data["data"])

                return response_data.get("data")

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                if attempt == max_retries:
                    raise CalComError(f"Request failed after {max_retries} retries: {e}") from e
                time.sleep(base_delay * (2 ** attempt))

            except RateLimitError as e:
                if attempt == max_retries:
                    raise
                time.sleep(e.retry_after)

            except CalComError:
                raise

            except Exception as e:
                if attempt == max_retries:
                    raise CalComError(f"Unexpected error: {e}") from e
                time.sleep(base_delay * (2 ** attempt))

        raise CalComError("Max retries exceeded")

    # ==================== Bookings API ====================

    async def create_booking(
        self,
        start: str,
        attendee: Dict,
        event_type_id: int = None,
        event_type_slug: str = None,
        username: str = None,
        organization_slug: str = None,
        responses: Dict = None,
        metadata: Dict = None,
        instant: bool = False,
        recurrence_count: int = None,
        seat_reference: str = None,
        idempotency_key: str = None,
    ) -> Dict:
        """
        Create a booking.

        Args:
            start: UTC start time in ISO 8601 (e.g., "2026-07-20T14:00:00Z")
            attendee: Attendee dict with name, email, timeZone, optional phoneNumber, language, metadata
            event_type_id: Event type ID (numeric)
            event_type_slug: Event type slug (requires username or organization_slug)
            username: Username for slug lookup
            organization_slug: Organization slug for org event types
            responses: Custom booking form responses
            metadata: Custom metadata (supports idempotencyKey)
            instant: Instant booking for team event types
            recurrence_count: Number of occurrences for recurring bookings
            seat_reference: Seat reference for multi-seat events
            idempotency_key: UUID for idempotent creation

        Returns:
            Booking object
        """
        payload = {
            "start": start,
            "attendee": attendee,
        }

        if event_type_id:
            payload["eventTypeId"] = event_type_id
        if event_type_slug:
            payload["eventTypeSlug"] = event_type_slug
        if username:
            payload["username"] = username
        if organization_slug:
            payload["organizationSlug"] = organization_slug
        if responses:
            payload["responses"] = responses
        if metadata:
            payload["metadata"] = metadata
        if instant:
            payload["instant"] = instant
        if recurrence_count:
            payload["recurrenceCount"] = recurrence_count
        if seat_reference:
            payload["seatReference"] = seat_reference

        if not idempotency_key:
            idempotency_key = str(uuid.uuid4())

        return await self._request(
            "POST",
            "/bookings",
            json_data=payload,
            idempotency_key=idempotency_key,
            validate_request_schema="booking-request",
            validate_response_schema="booking-response",
        )

    def create_booking_sync(self, **kwargs) -> Dict:
        """Synchronous create_booking."""
        return asyncio.run(self.create_booking(**kwargs))

    async def list_bookings(
        self,
        status: str = None,
        start_time: str = None,
        end_time: str = None,
        attendee_email: str = None,
        page: int = 1,
        limit: int = 50,
    ) -> Dict:
        """
        List bookings with filtering and pagination.

        Args:
            status: Filter by status (PENDING, ACCEPTED, CANCELLED, REJECTED)
            start_time: Filter bookings after this time (ISO 8601)
            end_time: Filter bookings before this time (ISO 8601)
            attendee_email: Filter by attendee email
            page: Page number (1-indexed)
            limit: Items per page (max 100)

        Returns:
            Paginated booking list
        """
        params = {"page": page, "limit": min(limit, 100)}
        if status:
            params["status"] = status
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if attendee_email:
            params["attendeeEmail"] = attendee_email

        return await self._request(
            "GET",
            "/bookings",
            params=params,
            validate_response_schema="booking-list-response",
        )

    async def get_booking(self, booking_id: Union[int, str]) -> Dict:
        """Get a single booking by ID or UID."""
        return await self._request(
            "GET",
            f"/bookings/{booking_id}",
            validate_response_schema="booking-response",
        )

    async def cancel_booking(
        self,
        booking_id: Union[int, str],
        cancel_reason: str = None,
        canceler: str = "ATTENDEE",
    ) -> Dict:
        """
        Cancel a booking.

        Args:
            booking_id: Booking ID or UID
            cancel_reason: Reason for cancellation
            canceler: Who is cancelling (ATTENDEE or HOST)

        Returns:
            Cancelled booking object
        """
        payload = {}
        if cancel_reason:
            payload["cancelReason"] = cancel_reason
        if canceler:
            payload["canceler"] = canceler

        return await self._request(
            "POST",
            f"/bookings/{booking_id}/cancel",
            json_data=payload,
            validate_response_schema="booking-response",
        )

    async def reschedule_booking(
        self,
        booking_id: Union[int, str],
        start_time: str,
        end_time: str = None,
    ) -> Dict:
        """
        Reschedule a booking.

        Args:
            booking_id: Booking ID or UID
            start_time: New start time (ISO 8601)
            end_time: New end time (ISO 8601, optional - calculated from event type length)

        Returns:
            Rescheduled booking object
        """
        payload = {"startTime": start_time}
        if end_time:
            payload["endTime"] = end_time

        return await self._request(
            "POST",
            f"/bookings/{booking_id}/reschedule",
            json_data=payload,
            validate_response_schema="booking-response",
        )

    # ==================== Event Types API ====================

    async def create_event_type(self, config: Dict) -> Dict:
        """
        Create an event type.

        Args:
            config: Event type configuration (validated against event-type-config schema)

        Returns:
            Created event type object
        """
        return await self._request(
            "POST",
            "/event-types",
            json_data=config,
            validate_request_schema="event-type-config",
            validate_response_schema="event-type-response",
        )

    async def list_event_types(
        self,
        username: str = None,
        team_slug: str = None,
        organization_slug: str = None,
        page: int = 1,
        limit: int = 50,
    ) -> Dict:
        """List event types for user/team/org."""
        params = {"page": page, "limit": min(limit, 100)}
        if username:
            params["username"] = username
        if team_slug:
            params["teamSlug"] = team_slug
        if organization_slug:
            params["organizationSlug"] = organization_slug

        return await self._request(
            "GET",
            "/event-types",
            params=params,
        )

    async def get_event_type(self, event_type_id: int) -> Dict:
        """Get event type by ID."""
        return await self._request(
            "GET",
            f"/event-types/{event_type_id}",
        )

    async def update_event_type(self, event_type_id: int, config: Dict) -> Dict:
        """Update an event type."""
        return await self._request(
            "PATCH",
            f"/event-types/{event_type_id}",
            json_data=config,
            validate_request_schema="event-type-config",
        )

    async def delete_event_type(self, event_type_id: int) -> Dict:
        """Delete an event type."""
        return await self._request(
            "DELETE",
            f"/event-types/{event_type_id}",
        )

    # ==================== Schedules API ====================

    async def create_schedule(self, config: Dict) -> Dict:
        """Create a schedule."""
        return await self._request(
            "POST",
            "/schedules",
            json_data=config,
            validate_request_schema="schedule-config",
        )

    async def list_schedules(self) -> Dict:
        """List all schedules for the authenticated user."""
        return await self._request("GET", "/schedules")

    async def get_schedule(self, schedule_id: int) -> Dict:
        """Get schedule by ID."""
        return await self._request("GET", f"/schedules/{schedule_id}")

    async def update_schedule(self, schedule_id: int, config: Dict) -> Dict:
        """Update a schedule."""
        return await self._request(
            "PATCH",
            f"/schedules/{schedule_id}",
            json_data=config,
            validate_request_schema="schedule-config",
        )

    async def delete_schedule(self, schedule_id: int) -> Dict:
        """Delete a schedule."""
        return await self._request("DELETE", f"/schedules/{schedule_id}")

    # ==================== Availability API ====================

    async def get_availability(self, query: Dict) -> Dict:
        """
        Get available time slots.

        Args:
            query: Availability query (validated against availability-query schema)

        Returns:
            Available slots grouped by date
        """
        return await self._request(
            "POST",
            "/slots",
            json_data=query,
            validate_request_schema="availability-query",
            validate_response_schema="availability-response",
        )

    async def get_availability_sync(self, **kwargs) -> Dict:
        """Synchronous get_availability."""
        return asyncio.run(self.get_availability(kwargs))

    # ==================== Webhooks API ====================

    async def create_webhook(
        self,
        url: str,
        events: List[str],
        secret: str = None,
        active: bool = True,
    ) -> Dict:
        """
        Create a webhook subscription.

        Args:
            url: Webhook endpoint URL (must be HTTPS)
            events: List of trigger events (e.g., ["BOOKING_CREATED", "BOOKING_CANCELLED"])
            secret: HMAC secret for signature verification (auto-generated if not provided)
            active: Whether webhook is active

        Returns:
            Created webhook object
        """
        payload = {
            "url": url,
            "events": events,
            "active": active,
        }
        if secret:
            payload["secret"] = secret

        return await self._request(
            "POST",
            "/webhooks",
            json_data=payload,
        )

    async def list_webhooks(self) -> Dict:
        """List all webhooks."""
        return await self._request("GET", "/webhooks")

    async def get_webhook(self, webhook_id: int) -> Dict:
        """Get webhook by ID."""
        return await self._request("GET", f"/webhooks/{webhook_id}")

    async def update_webhook(
        self,
        webhook_id: int,
        url: str = None,
        events: List[str] = None,
        secret: str = None,
        active: bool = None,
    ) -> Dict:
        """Update a webhook."""
        payload = {}
        if url:
            payload["url"] = url
        if events:
            payload["events"] = events
        if secret:
            payload["secret"] = secret
        if active is not None:
            payload["active"] = active

        return await self._request("PATCH", f"/webhooks/{webhook_id}", json_data=payload)

    async def delete_webhook(self, webhook_id: int) -> Dict:
        """Delete a webhook."""
        return await self._request("DELETE", f"/webhooks/{webhook_id}")

    # ==================== Webhook Verification ====================

    @staticmethod
    def verify_webhook_signature(
        payload: bytes,
        signature_header: str,
        timestamp_header: str,
        secret: str,
        tolerance_seconds: int = 300,
    ) -> bool:
        """
        Verify Cal.com webhook signature.

        Args:
            payload: Raw request body bytes
            signature_header: Value of cal-signature header
            timestamp_header: Value of cal-timestamp header
            secret: Webhook secret
            tolerance_seconds: Max timestamp drift (default 5 min)

        Returns:
            True if signature is valid

        Raises:
            ValueError: If headers are missing or invalid
        """
        if not signature_header or not timestamp_header:
            raise ValueError("Missing signature or timestamp header")

        # Check timestamp
        try:
            timestamp = int(timestamp_header)
        except ValueError:
            raise ValueError("Invalid timestamp header")

        now = int(time.time())
        if abs(now - timestamp) > tolerance_seconds:
            raise ValueError(f"Timestamp outside tolerance: {abs(now - timestamp)}s > {tolerance_seconds}s")

        # Verify signature
        expected_signature = hmac.new(
            secret.encode(),
            f"{timestamp}.{payload.decode()}".encode(),
            hashlib.sha256,
        ).hexdigest()

        # Constant-time comparison
        return hmac.compare_digest(signature_header, expected_signature)

    @staticmethod
    def parse_webhook_payload(payload: Dict) -> Dict:
        """
        Parse and validate webhook payload.

        Args:
            payload: Parsed JSON payload

        Returns:
            Validated payload with triggerEvent and data
        """
        validate_request("webhook-payload", payload)
        return payload

    # ==================== User/Team API ====================

    async def get_me(self) -> Dict:
        """Get authenticated user info."""
        return await self._request("GET", "/me")

    async def create_team(self, config: Dict) -> Dict:
        """Create a team."""
        return await self._request(
            "POST",
            "/teams",
            json_data=config,
            validate_request_schema="team-config",
        )

    async def list_teams(self) -> Dict:
        """List teams for authenticated user."""
        return await self._request("GET", "/teams")

    # ==================== Utility Methods ====================

    async def test_auth(self) -> Dict:
        """Test authentication by calling /me endpoint."""
        return await self.get_me()

    def test_auth_sync(self) -> Dict:
        """Synchronous test_auth."""
        return asyncio.run(self.test_auth())

    @staticmethod
    def generate_idempotency_key() -> str:
        """Generate a new idempotency key."""
        return str(uuid.uuid4())

    def set_output_format(self, format: OutputFormat) -> None:
        """Set output format for CLI commands."""
        self.output_manager.format = format

    def output(self, data: Any, format: OutputFormat = None) -> None:
        """Output data using configured output manager."""
        self.output_manager.output(data, format)