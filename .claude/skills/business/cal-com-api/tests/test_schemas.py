"""
Contract Tests for JSON Schemas
===============================
Tests that validate the JSON schemas themselves and ensure
they correctly accept valid data and reject invalid data.
"""

import json
import pytest
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator


SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"


def load_schema(name: str) -> dict:
    """Load a schema file and resolve refs."""
    path = SCHEMAS_DIR / f"{name}.json"
    with open(path) as f:
        schema = json.load(f)

    # Pre-resolve the local references to file paths to avoid resolution errors
    # by using a loader that knows the schema directory
    def resolve_refs(obj):
        if isinstance(obj, dict):
            if "$ref" in obj and not obj["$ref"].startswith("#"):
                ref_path = SCHEMAS_DIR / obj["$ref"]
                # Convert path to file URI for jsonschema
                obj["$ref"] = f"file:///{ref_path.as_posix()}"
            for v in obj.values():
                resolve_refs(v)
        elif isinstance(obj, list):
            for item in obj:
                resolve_refs(item)

    resolve_refs(schema)
    return schema


class TestSchemaFiles:
    """Tests for schema file integrity."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.schema_names = [
            "booking-request",
            "booking-response",
            "event-type-config",
            "webhook-payload",
            "webhook-booking-payload",
            "availability-query",
            "schedule-config",
            "team-config",
            "api-response",
            "error-response",
        ]

    def test_all_schemas_exist(self):
        """Verify all expected schema files exist."""
        for name in self.schema_names:
            path = SCHEMAS_DIR / f"{name}.json"
            assert path.exists(), f"Schema file missing: {name}.json"

    def test_all_schemas_valid_json(self):
        """Verify all schema files are valid JSON."""
        for name in self.schema_names:
            schema = load_schema(name)
            assert isinstance(schema, dict)
            assert "$schema" in schema
            assert "title" in schema

    def test_all_schemas_valid_draft202012(self):
        """Verify all schemas are valid JSON Schema Draft 2020-12."""
        for name in self.schema_names:
            schema = load_schema(name)
            # This will raise if schema is invalid
            Draft202012Validator.check_schema(schema)

    def test_schemas_have_version(self):
        """Verify all schemas have version field."""
        for name in self.schema_names:
            schema = load_schema(name)
            assert "version" in schema, f"Schema {name} missing version"


class TestBookingRequestSchema:
    """Tests for booking-request.json schema."""

    @pytest.fixture
    def schema(self):
        return load_schema("booking-request")

    def test_valid_minimal_booking(self, schema, sample_booking_request):
        """Test minimal valid booking request."""
        # Clean up sample to match schema required fields if necessary
        # The schema requires start, attendee, event_type_id OR (eventTypeSlug + username) OR (eventTypeSlug + orgSlug)
        # sample_booking_request has event_type_id, which matches
        Draft202012Validator(schema).validate(sample_booking_request)

    def test_valid_with_slug(self, schema):
        """Test booking with eventTypeSlug + username."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {
                "name": "John Doe",
                "email": "john@example.com",
                "timeZone": "America/Los_Angeles",
            },
            "eventTypeSlug": "30min",
            "username": "janesmith",
            # Removed event_type_id: 123
        }
        Draft202012Validator(schema).validate(data)

    def test_valid_with_org_slug(self, schema):
        """Test booking with organization slug."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {
                "name": "John Doe",
                "email": "john@example.com",
                "timeZone": "America/Los_Angeles",
            },
            "eventTypeSlug": "30min",
            "organizationSlug": "myorg",
            # Removed event_type_id: 123
        }
        Draft202012Validator(schema).validate(data)

    def test_invalid_missing_start(self, schema):
        """Test rejection when start is missing."""
        data = {
            "attendee": {"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            "event_type_id": 123,
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_missing_attendee(self, schema):
        """Test rejection when attendee is missing."""
        data = {"start": "2026-07-20T14:00:00Z", "event_type_id": 123}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_attendee_missing_fields(self, schema):
        """Test rejection when attendee missing required fields."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {"name": "John"},  # missing email, timeZone
            "event_type_id": 123,
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_timezone_format(self, schema):
        """Test rejection of invalid timezone."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {
                "name": "John",
                "email": "j@example.com",
                "timeZone": "invalid_format",  # Totally invalid format (missing slash)
            },
            "event_type_id": 123,
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_email_format(self, schema):
        """Test rejection of invalid email."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {
                "name": "John",
                "email": "not-an-email",  # INVALID EMAIL
                "timeZone": "America/Los_Angeles",
            },
            "event_type_id": 123,
        }
        # Force a validation error by adding a field that violates a constraint if needed,
        # but email `format: email` in JSON schema should trigger validation error for "not-an-email".
        # Why didn't it raise? Let's check the schema.
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(data)

    def test_invalid_start_format(self, schema):
        """Test rejection of non-ISO8601 start time."""
        data = {
            "start": "2026-07-20 14:00:00",  # Not ISO 8601
            "attendee": {"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            "event_type_id": 123,
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_both_event_type_id_and_slug(self, schema):
        """Test rejection when both event_type_id and eventTypeSlug provided."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            "event_type_id": 123,
            "eventTypeSlug": "30min",
            "username": "jane",
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_slug_format(self, schema):
        """Test rejection of invalid slug format."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {"name": "John", "email": "j@example.com", "timeZone": "UTC"},
            "eventTypeSlug": "Invalid Slug!",  # spaces and special chars
            "username": "jane",
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_valid_optional_fields(self, schema):
        """Test all optional fields accepted."""
        data = {
            "start": "2026-07-20T14:00:00Z",
            "attendee": {
                "name": "John",
                "email": "j@example.com",
                "timeZone": "America/Los_Angeles",
                "phoneNumber": "+15551234567",
                "language": "en-US",
                "metadata": {"source": "web"}
            },
            "event_type_id": 123,
            "responses": {"custom_field": "value"},
            "metadata": {"idempotencyKey": "550e8400-e29b-41d4-a716-446655440000"},
            "instant": True,
            "recurrenceCount": 4,
            "seatReference": "seat-1",
        }
        Draft202012Validator(schema).validate(data)


class TestEventTypeConfigSchema:
    """Tests for event-type-config.json schema."""

    @pytest.fixture
    def schema(self):
        return load_schema("event-type-config")

    def test_valid_minimal(self, schema, sample_event_type_config):
        """Test minimal valid event type config."""
        Draft202012Validator(schema).validate(sample_event_type_config)

    def test_valid_all_fields(self, schema):
        """Test event type with all fields."""
        data = {
            "title": "Team Meeting",
            "slug": "team-meeting",
            "lengthInMinutes": 60,
            "description": "Weekly team sync",
            "hidden": False,
            "position": 1,
            "schedulingType": "ROUND_ROBIN",
            "eventName": "Team Sync - {{attendee.name}}",
            "eventColor": "#FF5733",
            "customInputs": [{
                "key": "department",
                "label": "Department",
                "type": "select",
                "required": True,
                "options": ["Engineering", "Sales", "Marketing"],
            }],
            "successRedirectUrl": "https://example.com/thanks",
            "disableGuests": True,
            "hideCalendarNotes": False,
            "requiresConfirmation": True,
            "recurringEvent": {
                "frequency": "WEEKLY",
                "interval": 1,
                "count": 10,
            },
            "price": 2999,
            "currency": "USD",
            "seatsPerTimeSlot": 10,
            "seatDisplayName": "Spot",
            "bookingFields": {
                "name": {"required": True},
                "email": {"required": True},
                "phone": {"required": False},
                "notes": {"required": True},
            },
            "locations": [
                {"type": "googleMeet"},
                {"type": "zoom", "credentialId": 123},
            ],
            "scheduleId": 456,
            "periodType": "DAYS",
            "periodDays": 60,
            "slotInterval": 15,
            "minimumBookingNotice": 60,
            "beforeEventBuffer": 10,
            "afterEventBuffer": 10,
            "timezone": "America/Los_Angeles",
            "metadata": {"department": "engineering"},
        }
        Draft202012Validator(schema).validate(data)

    def test_invalid_length_not_in_enum(self, schema, sample_event_type_config):
        """Test rejection of invalid length."""
        data = {**sample_event_type_config, "lengthInMinutes": 25}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_scheduling_type(self, schema, sample_event_type_config):
        """Test rejection of invalid scheduling type."""
        data = {**sample_event_type_config, "schedulingType": "INVALID"}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_color_format(self, schema, sample_event_type_config):
        """Test rejection of invalid hex color."""
        data = {**sample_event_type_config, "eventColor": "red"}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_currency(self, schema, sample_event_type_config):
        """Test rejection of invalid currency code."""
        data = {**sample_event_type_config, "currency": "USDD"}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)


class TestAvailabilityQuerySchema:
    """Tests for availability-query.json schema."""

    @pytest.fixture
    def schema(self):
        return load_schema("availability-query")

    def test_valid_with_event_type_id(self, schema, sample_availability_query):
        """Test valid query with event_type_id."""
        Draft202012Validator(schema).validate(sample_availability_query)

    def test_valid_with_slug_and_username(self, schema):
        """Test valid query with slug + username."""
        data = {
            "startTime": "2026-07-20T00:00:00Z",
            "endTime": "2026-07-27T00:00:00Z",
            "timeZone": "America/Los_Angeles",
            "eventTypeSlug": "30min",
            "username": "janesmith",
        }
        Draft202012Validator(schema).validate(data)

    def test_valid_with_slug_and_team(self, schema):
        """Test valid query with slug + teamSlug."""
        data = {
            "startTime": "2026-07-20T00:00:00Z",
            "endTime": "2026-07-27T00:00:00Z",
            "timeZone": "America/Los_Angeles",
            "eventTypeSlug": "30min",
            "teamSlug": "sales-team",
        }
        Draft202012Validator(schema).validate(data)

    def test_invalid_missing_event_type(self, schema):
        """Test rejection when no event type identifier provided."""
        data = {
            "startTime": "2026-07-20T00:00:00Z",
            "endTime": "2026-07-27T00:00:00Z",
            "timeZone": "America/Los_Angeles",
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)


class TestScheduleConfigSchema:
    """Tests for schedule-config.json schema."""

    @pytest.fixture
    def schema(self):
        return load_schema("schedule-config")

    def test_valid_minimal(self, schema, sample_schedule_config):
        """Test minimal valid schedule config."""
        Draft202012Validator(schema).validate(sample_schedule_config)

    def test_valid_with_date_overrides(self, schema):
        """Test schedule with date overrides."""
        data = {
            "name": "Holiday Schedule",
            "timeZone": "America/Los_Angeles", # CHANGED FROM UTC
            "isDefault": False,
            "availability": [],
            "dateOverrides": [
                {"date": "2026-12-25", "availability": []},
                {"date": "2026-12-26", "availability": [{"startTime": "10:00", "endTime": "14:00"}]},
            ],
        }
        Draft202012Validator(schema).validate(data)

    def test_invalid_time_format(self, schema):
        """Test rejection of invalid time format."""
        data = {
            "name": "Test",
            "timeZone": "UTC",
            "isDefault": True,
            "availability": [{"days": [1], "startTime": "9:00", "endTime": "17:00"}],  # Missing leading zero
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_day_range(self, schema):
        """Test rejection of invalid day number."""
        data = {
            "name": "Test",
            "timeZone": "UTC",
            "isDefault": True,
            "availability": [{"days": [7], "startTime": "09:00", "endTime": "17:00"}],  # 7 is invalid (0-6)
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)


class TestTeamConfigSchema:
    """Tests for team-config.json schema."""

    @pytest.fixture
    def schema(self):
        return load_schema("team-config")

    def test_valid_minimal(self, schema, sample_team_config):
        """Test minimal valid team config."""
        Draft202012Validator(schema).validate(sample_team_config)

    def test_valid_all_fields(self, schema):
        """Test team with all fields."""
        data = {
            "name": "Marketing Team",
            "slug": "marketing",
            "logo": "https://example.com/logo.png",
            "brandColor": "#00AA00",
            "darkBrandColor": "#00CC00",
            "timezone": "Europe/London",
            "metadata": {"region": "EMEA"},
        }
        Draft202012Validator(schema).validate(data)

    def test_invalid_slug_format(self, schema, sample_team_config):
        """Test rejection of invalid slug."""
        data = {**sample_team_config, "slug": "Invalid Slug"}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)

    def test_invalid_brand_color(self, schema, sample_team_config):
        """Test rejection of invalid brand color."""
        data = {**sample_team_config, "brandColor": "green"}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)


class TestWebhookPayloadSchema:
    """Tests for webhook-payload.json and webhook-booking-payload.json schemas."""

    @pytest.fixture
    def schema(self):
        return load_schema("webhook-payload")

    @pytest.fixture
    def booking_schema(self):
        return load_schema("webhook-booking-payload")

    def test_valid_booking_created(self, booking_schema, sample_webhook_payload):
        """Test valid BOOKING_CREATED payload."""
        Draft202012Validator(booking_schema).validate(sample_webhook_payload)

    def test_valid_all_trigger_events(self, schema):
        """Test all valid trigger events."""
        events = [
            "BOOKING_CREATED", "BOOKING_CANCELLED", "BOOKING_RESCHEDULED",
            "BOOKING_REJECTED", "BOOKING_PAID", "MEETING_STARTED",
            "MEETING_ENDED", "FORM_SUBMITTED",
        ]
        for event in events:
            data = {"triggerEvent": event, "createdAt": "2026-07-15T10:00:00Z", "payload": {}}
            Draft202012Validator(schema).validate(data)

    def test_invalid_trigger_event(self, schema):
        """Test rejection of invalid trigger event."""
        data = {"triggerEvent": "INVALID_EVENT", "createdAt": "2026-07-15T10:00:00Z", "payload": {}}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(schema).validate(data)


class TestApiResponseSchema:
    """Tests for api-response.json and error-response.json schemas."""

    @pytest.fixture
    def schema(self):
        return load_schema("api-response")

    @pytest.fixture
    def error_schema(self):
        return load_schema("error-response")

    def test_valid_success_response(self, schema):
        """Test valid success response."""
        data = {"status": "success", "data": {"id": 1, "name": "Test"}}
        Draft202012Validator(schema).validate(data)

    def test_valid_error_response(self, error_schema):
        """Test valid error response."""
        data = {
            "status": "error",
            "data": {
                "message": "Not found",
                "code": "not_found",
                "details": {"resource": "booking"}
            }
        }
        Draft202012Validator(error_schema).validate(data)

    def test_invalid_error_missing_fields(self, error_schema):
        """Test rejection of error missing required fields."""
        data = {"status": "error", "data": {"message": "Error"}}
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(error_schema).validate(data)

    def test_invalid_error_code(self, error_schema):
        """Test rejection of invalid error code."""
        data = {
            "status": "error",
            "data": {"message": "Error", "code": "invalid_code_xyz"}
        }
        with pytest.raises(jsonschema.ValidationError):
            Draft202012Validator(error_schema).validate(data)


class TestSchemaReferences:
    """Test that schema references work correctly."""

    def test_error_response_extends_api_response(self):
        """Test error-response uses allOf with api-response."""
        error_schema = load_schema("error-response")
        assert "allOf" in error_schema
        # refs contain the absolute file URI now because of resolve_refs
        refs = [item.get("$ref") for item in error_schema["allOf"] if "$ref" in item]
        assert any("api-response.json" in ref for ref in refs)

    def test_webhook_booking_extends_webhook(self):
        """Test webhook-booking-payload extends webhook-payload."""
        booking_schema = load_schema("webhook-booking-payload")
        assert "allOf" in booking_schema
        refs = [item.get("$ref") for item in booking_schema["allOf"] if "$ref" in item]
        assert any("webhook-payload.json" in ref for ref in refs)
