"""
Test Configuration and Fixtures
===============================
Shared fixtures and configuration for cal_booking_skill tests.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import httpx


@pytest.fixture
def schemas_dir():
    """Path to schemas directory."""
    return Path(__file__).parent.parent / "schemas"


@pytest.fixture
def sample_booking_request():
    """Valid booking request payload."""
    return {
        "start": "2026-07-20T14:00:00Z",
        "attendee": {
            "name": "John Doe",
            "email": "john@example.com",
            "timeZone": "America/Los_Angeles",
        },
        "event_type_id": 12345,
        "metadata": {
            "idempotencyKey": "550e8400-e29b-41d4-a716-446655440000"
        }
    }


@pytest.fixture
def sample_booking_response():
    """Sample booking response from API."""
    return {
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


@pytest.fixture
def sample_event_type_config():
    """Valid event type configuration."""
    return {
        "title": "30 Minute Meeting",
        "slug": "30min",
        "lengthInMinutes": 30,
        "description": "A quick 30 minute meeting",
        "hidden": False,
        "schedulingType": "PERSONAL",
        "price": 0,
        "currency": "USD",
        "seatsPerTimeSlot": 1,
        "periodType": "RANGE",
        "periodDays": 30,
        "minimumBookingNotice": 0,
        "beforeEventBuffer": 0,
        "afterEventBuffer": 0
    }


@pytest.fixture
def sample_availability_query():
    """Valid availability query."""
    return {
        "startTime": "2026-07-20T00:00:00Z",
        "endTime": "2026-07-27T00:00:00Z",
        "timeZone": "America/Los_Angeles",
        "event_type_id": 12345
    }


@pytest.fixture
def sample_schedule_config():
    """Valid schedule configuration."""
    return {
        "name": "Business Hours",
        "timeZone": "America/Los_Angeles",
        "isDefault": True,
        "availability": [
            {"days": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00"}
        ],
        "dateOverrides": [
            {"date": "2026-07-04", "availability": []}
        ]
    }


@pytest.fixture
def sample_team_config():
    """Valid team configuration."""
    return {
        "name": "Sales Team",
        "slug": "sales-team",
        "timezone": "America/New_York",
        "brandColor": "#0066CC"
    }


@pytest.fixture
def sample_webhook_payload():
    """Sample webhook payload."""
    return {
        "triggerEvent": "BOOKING_CREATED",
        "createdAt": "2026-07-15T10:00:00Z",
        "payload": {
            "uid": "abc123",
            "id": 12345,
            "title": "30min Meeting",
            "startTime": "2026-07-20T14:00:00Z",
            "endTime": "2026-07-20T14:30:00Z",
            "status": "ACCEPTED",
            "attendees": [{
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "timeZone": "America/Los_Angeles"
            }],
            "organizer": {
                "id": 100,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "timeZone": "UTC"
            }
        }
    }


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx response."""
    def _create_response(status_code: int, json_data: dict, headers: dict = None):
        response = MagicMock(spec=httpx.Response)
        response.status_code = status_code
        response.json.return_value = json_data
        response.headers = headers or {}
        response.text = json.dumps(json_data)
        return response
    return _create_response


@pytest.fixture
def mock_async_client():
    """Create a mock async httpx client."""
    client = AsyncMock(spec=httpx.AsyncClient)
    return client


@pytest.fixture
def api_key():
    """Test API key."""
    return "cal_test_abcdef123456"


@pytest.fixture
def oauth_token():
    """Test OAuth token."""
    return "oauth_access_token_12345"