"""
Schema Validation Module
========================
JSON Schema validation for Cal.com API requests and responses.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from functools import lru_cache

import jsonschema
from jsonschema import Draft202012Validator, ValidationError as JSONSchemaValidationError


SCHEMAS_DIR = Path(__file__).parent.parent.parent / "schemas"


class ValidationError(Exception):
    """Schema validation error."""

    def __init__(self, message: str, path: str = None, schema: str = None):
        super().__init__(message)
        self.message = message
        self.path = path
        self.schema = schema


@lru_cache(maxsize=32)
def _load_schema(schema_name: str) -> Dict[str, Any]:
    """Load and cache a JSON schema."""
    schema_path = SCHEMAS_DIR / f"{schema_name}.json"
    if not schema_path.exists():
        # Try without .json extension
        schema_path = SCHEMAS_DIR / schema_name
        if not schema_path.exists():
            raise ValidationError(f"Schema not found: {schema_name}")

    with open(schema_path) as f:
        return json.load(f)


def _get_validator(schema: Dict[str, Any]) -> Draft202012Validator:
    """Create a validator for the given schema."""
    return Draft202012Validator(schema)


def validate_request(schema_name: str, data: Dict[str, Any]) -> None:
    """
    Validate request data against a schema.

    Args:
        schema_name: Name of the schema (e.g., "booking-request", "event-type-config")
        data: Data to validate

    Raises:
        ValidationError: If validation fails
    """
    try:
        schema = _load_schema(schema_name)
        validator = _get_validator(schema)
        validator.validate(data)
    except JSONSchemaValidationError as e:
        path = " -> ".join(str(p) for p in e.path) if e.path else "root"
        raise ValidationError(
            f"Request validation failed for {schema_name}: {e.message}",
            path=path,
            schema=schema_name,
        ) from e
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Schema loading failed for {schema_name}: {e}") from e


def validate_response(schema_name: str, data: Dict[str, Any]) -> None:
    """
    Validate response data against a schema.

    Args:
        schema_name: Name of the schema (e.g., "booking-response", "api-response")
        data: Response data to validate

    Raises:
        ValidationError: If validation fails
    """
    try:
        schema = _load_schema(schema_name)
        validator = _get_validator(schema)
        validator.validate(data)
    except JSONSchemaValidationError as e:
        path = " -> ".join(str(p) for p in e.path) if e.path else "root"
        raise ValidationError(
            f"Response validation failed for {schema_name}: {e.message}",
            path=path,
            schema=schema_name,
        ) from e
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Schema loading failed for {schema_name}: {e}") from e


def validate_webhook_payload(payload: Dict[str, Any]) -> None:
    """Validate webhook payload structure."""
    validate_request("webhook-payload", payload)

    # Additional event-specific validation
    trigger_event = payload.get("triggerEvent")
    if trigger_event and trigger_event.startswith("BOOKING_"):
        validate_request("webhook-booking-payload", payload)


def get_schema(schema_name: str) -> Dict[str, Any]:
    """Get a schema by name (for external use)."""
    return _load_schema(schema_name)


def list_schemas() -> list:
    """List available schema names."""
    return [f.stem for f in SCHEMAS_DIR.glob("*.json")]


# Convenience functions for common validations
def validate_booking_request(data: Dict[str, Any]) -> None:
    """Validate booking creation request."""
    validate_request("booking-request", data)


def validate_event_type_config(data: Dict[str, Any]) -> None:
    """Validate event type configuration."""
    validate_request("event-type-config", data)


def validate_availability_query(data: Dict[str, Any]) -> None:
    """Validate availability query."""
    validate_request("availability-query", data)


def validate_schedule_config(data: Dict[str, Any]) -> None:
    """Validate schedule configuration."""
    validate_request("schedule-config", data)


def validate_team_config(data: Dict[str, Any]) -> None:
    """Validate team configuration."""
    validate_request("team-config", data)


def validate_api_response(data: Dict[str, Any]) -> None:
    """Validate API response envelope."""
    validate_response("api-response", data)


def validate_error_response(data: Dict[str, Any]) -> None:
    """Validate error response."""
    validate_response("error-response", data)