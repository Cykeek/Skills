#!/usr/bin/env python3
"""
Wix Support Validators Module
=============================
Validates requests and responses against JSON schemas.
"""

import json
import os
from typing import Any, Dict, List, Tuple
from pathlib import Path


class SchemaValidator:
    """Validates data against JSON schemas."""

    def __init__(self, schemas_dir: str = None):
        if schemas_dir is None:
            # Default to schemas directory relative to this file (go up 3 levels: wix_support_skill -> scripts -> wix-support -> schemas)
            self.schemas_dir = Path(__file__).parent.parent.parent / "schemas"
        else:
            self.schemas_dir = Path(schemas_dir)
        self._schemas = {}

    def _load_schema(self, schema_name: str) -> Dict[str, Any]:
        """Load a schema from file."""
        if schema_name in self._schemas:
            return self._schemas[schema_name]

        schema_file = self.schemas_dir / f"{schema_name}.json"
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema not found: {schema_file}")

        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        self._schemas[schema_name] = schema
        return schema

    def validate(self, schema_name: str, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate data against a schema (basic validation without jsonschema lib)."""
        errors = []

        try:
            schema = self._load_schema(schema_name)
        except FileNotFoundError as e:
            errors.append(str(e))
            return False, errors

        # Basic validation - check required fields and types
        errors.extend(self._validate_object(schema, data, ""))

        return len(errors) == 0, errors

    def _validate_object(self, schema: Dict[str, Any], data: Any, path: str) -> List[str]:
        """Recursively validate object against schema."""
        errors = []

        # Type check
        if "type" in schema:
            expected_type = schema["type"]
            if expected_type == "object":
                if not isinstance(data, dict):
                    errors.append(f"{path}: Expected object, got {type(data).__name__}")
                    return errors
            elif expected_type == "array":
                if not isinstance(data, list):
                    errors.append(f"{path}: Expected array, got {type(data).__name__}")
                    return errors
            elif expected_type == "string":
                if not isinstance(data, str):
                    errors.append(f"{path}: Expected string, got {type(data).__name__}")
                    return errors
            elif expected_type == "boolean":
                if not isinstance(data, bool):
                    errors.append(f"{path}: Expected boolean, got {type(data).__name__}")
                    return errors
            elif expected_type == "number":
                if not isinstance(data, (int, float)):
                    errors.append(f"{path}: Expected number, got {type(data).__name__}")
                    return errors

        # Required fields
        if "required" in schema and isinstance(data, dict):
            for field in schema["required"]:
                if field not in data:
                    errors.append(f"{path}.{field}: Missing required field")

        # Properties validation
        if "properties" in schema and isinstance(data, dict):
            for prop_name, prop_schema in schema["properties"].items():
                if prop_name in data:
                    prop_errors = self._validate_object(
                        prop_schema, data[prop_name], f"{path}.{prop_name}"
                    )
                    errors.extend(prop_errors)

        # Items validation for arrays
        if "items" in schema and isinstance(data, list):
            item_schema = schema["items"]
            for i, item in enumerate(data):
                item_errors = self._validate_object(item_schema, item, f"{path}[{i}]")
                errors.extend(item_errors)

        # Enum validation
        if "enum" in schema and data not in schema["enum"]:
            errors.append(f"{path}: Value '{data}' not in allowed values: {schema['enum']}")

        return errors


# Convenience functions for CLI
def validate_request(schema_name: str, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a request against its schema."""
    validator = SchemaValidator()
    # Map CLI schema names to file names
    schema_map = {
        "diagnose-request": "diagnose-request",
        "velo-check-request": "velo-check-request",
        "cms-debug-request": "cms-debug-request",
        "dns-check-request": "dns-check-request",
    }
    return validator.validate(schema_map.get(schema_name, schema_name), data)


def validate_response(schema_name: str, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a response against its schema."""
    validator = SchemaValidator()
    # Map CLI schema names to file names
    schema_map = {
        "diagnose-response": "diagnose-response",
        "velo-check-response": "velo-check-response",
        "cms-debug-response": "cms-debug-response",
        "dns-check-response": "dns-check-response",
        "editor-comparison": "editor-comparison",
    }
    return validator.validate(schema_map.get(schema_name, schema_name), data)