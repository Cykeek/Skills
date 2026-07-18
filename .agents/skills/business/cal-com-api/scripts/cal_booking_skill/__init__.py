"""
Cal.com Booking Skill - Python Package
======================================
Cal.com API v2 client with schema validation, rate limiting, and CLI interface.
"""

__version__ = "2.1.0"
__author__ = "AI Workflows"

from .api_client import CalComClient, CalComError, RateLimitError, AuthError, ValidationError
from .validation import validate_request, validate_response, ValidationError as SchemaValidationError
from .output_manager import OutputManager, OutputFormat

__all__ = [
    "CalComClient",
    "CalComError",
    "RateLimitError",
    "AuthError",
    "ValidationError",
    "SchemaValidationError",
    "validate_request",
    "validate_response",
    "OutputManager",
    "OutputFormat",
]