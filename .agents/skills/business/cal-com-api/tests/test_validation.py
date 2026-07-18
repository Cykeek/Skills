"""
Contract Tests for Validation Module
====================================
Tests for schema validation functions.
"""

import pytest

from cal_booking_skill.validation import (
    validate_request,
    validate_response,
    validate_booking_request,
    validate_event_type_config,
    validate_availability_query,
    validate_schedule_config,
    validate_team_config,
    validate_webhook_payload,
    ValidationError,
    get_schema,
    list_schemas,
)


class TestValidateRequest:
    """Tests for validate_request function."""

    def test_valid_booking_request(self, sample_booking_request):
        """Test validating a valid booking request."""
        validate_request("booking-request", sample_booking_request)

    def test_invalid_booking_request_missing_required(self):
        """Test validation fails for missing required fields."""
        data = {"start": "2026-07-20T14:00:00Z"}  # missing attendee
        with pytest.raises(ValidationError) as exc:
            validate_request("booking-request", data)
        assert "attendee" in str(exc.value).lower() or "required" in str(exc.value).lower()

    def test_invalid_booking_request_bad_email(self):
        """Test validation fails for invalid email."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {"name": "John", "email": "invalid", "timeZone": "UTC"},
            "event_type_id": 123,
        }
        with pytest.raises(ValidationError) as exc:
            validate_request("booking-request", data)
        assert "email" in str(exc.value).lower()

    def test_valid_event_type_config(self, sample_event_type_config):
        """Test validating a valid event type config."""
        validate_request("event-type-config", sample_event_type_config)

    def test_invalid_event_type_config_bad_length(self):
        """Test validation fails for invalid length."""
        data = {**sample_event_type_config, "lengthInMinutes": 25}
        with pytest.raises(ValidationError):
            validate_request("event-type-config", data)

    def test_valid_availability_query(self, sample_availability_query):
        """Test validating a valid availability query."""
        validate_request("availability-query", sample_availability_query)

    def test_invalid_availability_query_missing_event_type(self):
        """Test validation fails when no event type specified."""
        data = {
            "startTime": "2026-07-20T00:00:00Z",
            "endTime": "2026-07-27T00:00:00Z",
            "timeZone": "UTC",
        }
        with pytest.raises(ValidationError):
            validate_request("availability-query", data)

    def test_valid_schedule_config(self, sample_schedule_config):
        """Test validating a valid schedule config."""
        validate_request("schedule-config", sample_schedule_config)

    def test_valid_team_config(self, sample_team_config):
        """Test validating a valid team config."""
        validate_request("team-config", sample_team_config)


class TestValidateResponse:
    """Tests for validate_response function."""

    def test_valid_booking_response(self, sample_booking_response):
        """Test validating a valid booking response."""
        validate_response("booking-response", sample_booking_response)

    def test_invalid_booking_response_missing_fields(self):
        """Test validation fails for missing required fields."""
        data = {"id": 123}  # missing many required fields
        with pytest.raises(ValidationError):
            validate_response("booking-response", data)

    def test_valid_api_response(self):
        """Test validating API response envelope."""
        data = {"status": "success", "data": {"id": 1}}
        validate_response("api-response", data)

    def test_valid_error_response(self):
        """Test validating error response."""
        data = {
            "status": "error",
            "data": {"message": "Error", "code": "not_found"}
        }
        validate_response("error-response", data)


class TestConvenienceFunctions:
    """Tests for convenience validation functions."""

    def test_validate_booking_request(self, sample_booking_request):
        """Test validate_booking_request convenience function."""
        validate_booking_request(sample_booking_request)

    def test_validate_event_type_config(self, sample_event_type_config):
        """Test validate_event_type_config convenience function."""
        validate_event_type_config(sample_event_type_config)

    def test_validate_availability_query(self, sample_availability_query):
        """Test validate_availability_query convenience function."""
        validate_availability_query(sample_availability_query)

    def test_validate_schedule_config(self, sample_schedule_config):
        """Test validate_schedule_config convenience function."""
        validate_schedule_config(sample_schedule_config)

    def test_validate_team_config(self, sample_team_config):
        """Test validate_team_config convenience function."""
        validate_team_config(sample_team_config)


class TestValidateWebhookPayload:
    """Tests for webhook payload validation."""

    def test_valid_webhook_payload(self, sample_webhook_payload):
        """Test validating a valid webhook payload."""
        validate_webhook_payload(sample_webhook_payload)

    def test_invalid_webhook_missing_trigger(self):
        """Test validation fails for missing triggerEvent."""
        data = {"createdAt": "2026-07-15T10:00:00Z", "payload": {}}
        with pytest.raises(ValidationError):
            validate_webhook_payload(data)

    def test_booking_webhook_validation(self):
        """Test booking webhook triggers additional validation."""
        data = {
            "triggerEvent": "BOOKING_CREATED",
            "createdAt": "2026-07-15T10:00:00Z",
            "payload": {"uid": "abc", "id": 1, "title": "Test", "startTime": "2026-07-20T14:00:00Z",
                        "endTime": "2026-07-20T14:30:00Z", "status": "ACCEPTED",
                        "attendees": [{"id": 1, "name": "John", "email": "j@example.com", "timeZone": "UTC"}],
                        "organizer": {"id": 1, "name": "Jane", "email": "j@example.com", "timeZone": "UTC"}}
        }
        validate_webhook_payload(data)


class TestSchemaUtilities:
    """Tests for schema utility functions."""

    def test_get_schema(self):
        """Test get_schema returns schema dict."""
        schema = get_schema("booking-request")
        assert isinstance(schema, dict)
        assert schema["title"] == "Booking Request"

    def test_get_schema_not_found(self):
        """Test get_schema raises for non-existent schema."""
        with pytest.raises(ValidationError):
            get_schema("non-existent-schema")

    def test_list_schemas(self):
        """Test list_schemas returns all schema names."""
        schemas = list_schemas()
        assert isinstance(schemas, list)
        assert "booking-request" in schemas
        assert "event-type-config" in schemas
        assert len(schemas) >= 8