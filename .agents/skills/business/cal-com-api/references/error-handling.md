# Cal.com API v2 — Error Handling Reference

> **Source:** [Cal.com API Errors](https://cal.com/docs/api-reference/errors) | Integration Testing
> **Last Updated:** July 2025

---

## Error Response Format

All errors follow the standard envelope:

```json
{
  "status": "error",
  "data": {
    "message": "Human-readable error description",
    "code": "ERROR_CODE",
    "details": { ... }  // Optional: field-level validation, context
  }
}
```

---

## HTTP Status Codes & Retryability

| HTTP | Retryable | Description |
|------|-----------|-------------|
| 400 | ❌ | Bad Request — invalid input |
| 401 | ❌* | Unauthorized — fix auth, then retry |
| 403 | ❌ | Forbidden — permissions issue |
| 404 | ❌ | Not Found — resource doesn't exist |
| 409 | ⚠️ | Conflict — retry with different params |
| 422 | ❌ | Unprocessable — business rule violation |
| 429 | ✅ | Rate Limited — **must** respect Retry-After |
| 500 | ✅ | Server Error — retry with backoff |
| 502 | ✅ | Bad Gateway — retry with backoff |
| 503 | ✅ | Unavailable — retry with backoff |
| 504 | ✅ | Gateway Timeout — retry with backoff |

*401: Retry **after** refreshing token (OAuth) or regenerating API key

---

## Error Code Reference

### 400 Bad Request — `validation_error`
```json
{
  "status": "error",
  "data": {
    "message": "Request validation failed",
    "code": "validation_error",
    "details": {
      "start": ["Invalid ISO8601 format"],
      "attendee.timeZone": ["Invalid IANA timezone"]
    }
  }
}
```
**Action:** Fix request payload per `details`. Check schema.

### 400 Bad Request — `invalid_json`
```json
{
  "status": "error",
  "data": { "message": "Invalid JSON body", "code": "invalid_json" }
}
```
**Action:** Ensure `Content-Type: application/json` and valid JSON.

### 401 Unauthorized — `unauthorized`
```json
{
  "status": "error",
  "data": { "message": "Authentication required", "code": "unauthorized" }
}
```
**Action:** Add `Authorization: Bearer <token>` header.

### 401 Unauthorized — `invalid_token`
```json
{
  "status": "error",
  "data": { "message": "Invalid or expired token", "code": "invalid_token" }
}
```
**Action:** 
- API Key: Regenerate in dashboard
- OAuth: Use refresh token to get new access token

### 401 Unauthorized — `invalid_api_key`
```json
{
  "status": "error",
  "data": { "message": "Invalid API Key format", "code": "invalid_api_key" }
}
```
**Action:** Key must start with `cal_` (test) or `cal_live_` (live).

### 403 Forbidden — `insufficient_scope`
```json
{
  "status": "error",
  "data": { 
    "message": "Insufficient permissions", 
    "code": "insufficient_scope",
    "details": { "required": "BOOKING_WRITE", "current": ["BOOKING_READ"] }
  }
}
```
**Action:** Re-authorize with required scope.

### 403 Forbidden — `team_access_denied`
```json
{
  "status": "error",
  "data": { 
    "message": "Access denied to team", 
    "code": "team_access_denied",
    "details": { "teamId": 123, "reason": "Not a member" }
  }
}
```
**Action:** User must be team member; use team-scoped OAuth scopes.

### 404 Not Found — `not_found`
```json
{
  "status": "error",
  "data": { "message": "Booking not found", "code": "not_found" }
}
```
**Action:** Verify resource ID exists and is accessible.

### 409 Conflict — `conflict`
```json
{
  "status": "error",
  "data": { 
    "message": "Time slot no longer available", 
    "code": "conflict",
    "details": { "reason": "slot_taken", "alternativeSlots": [...] }
  }
}
```
**Action:** Offer alternative slots to user; retry with different time.

### 409 Conflict — `duplicate_webhook`
```json
{
  "status": "error",
  "data": { "message": "Webhook already exists for this URL", "code": "duplicate_webhook" }
}
```
**Action:** Use existing webhook or delete first.

### 422 Unprocessable Entity — `unprocessable_entity`
```json
{
  "status": "error",
  "data": {
    "message": "Booking cannot be created",
    "code": "unprocessable_entity",
    "details": { "reason": "outside_schedule", "scheduleId": 123 }
  }
}
```
**Action:** Check business rules (schedule, booking window, limits).

### 429 Too Many Requests — `rate_limit_exceeded`
```json
{
  "status": "error",
  "data": { 
    "message": "Rate limit exceeded", 
    "code": "rate_limit_exceeded",
    "details": { "retryAfter": 45 }
  }
}
```
**Headers:**
```
Retry-After: 45
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1721059200
```
**Action:** **Must** wait `Retry-After` seconds before retry.

### 5xx Server Errors
```json
{
  "status": "error",
  "data": { 
    "message": "Internal server error", 
    "code": "internal_error",
    "details": { "requestId": "req_abc123" }
  }
}
```
**Action:** Retry with exponential backoff. Include `requestId` in support tickets.

---

## Per-Endpoint Error Scenarios

### POST /bookings
| Scenario | HTTP | Code | Fix |
|----------|------|------|-----|
| Invalid start time format | 400 | validation_error | Use ISO8601 UTC: `2026-07-20T14:00:00Z` |
| Past start time | 422 | unprocessable_entity | Must be future |
| Slot taken | 409 | conflict | Pick different time |
| Event type not found | 404 | not_found | Verify eventTypeId/slug |
| Attendee email invalid | 400 | validation_error | Valid email format |
| Timezone invalid | 400 | validation_error | IANA tz (e.g., America/Los_Angeles) |
| Outside booking window | 422 | unprocessable_entity | Check event type periodDays |
| Double booking (same attendee) | 409 | conflict | Check existing bookings |

### POST /event-types
| Scenario | HTTP | Code | Fix |
|----------|------|------|-----|
| Slug taken | 409 | conflict | Choose unique slug |
| lengthInMinutes invalid | 400 | validation_error | 5, 15, 30, 45, 60, 90, 120... |
| Missing required fields | 400 | validation_error | title, slug, lengthInMinutes required |
| Scheduling type invalid | 400 | validation_error | PERSONAL, ROUND_ROBIN, COLLECTIVE |

### POST /webhooks
| Scenario | HTTP | Code | Fix |
|----------|------|------|-----|
| Invalid subscriberUrl | 400 | validation_error | Must be HTTPS |
| Duplicate URL | 409 | duplicate_webhook | Delete existing or update |
| Invalid trigger | 400 | validation_error | Use valid trigger constants |

### GET /event-types/{id}/slots
| Scenario | HTTP | Code | Fix |
|----------|------|------|-----|
| Missing startTime/endTime | 400 | validation_error | Both required |
| Invalid timeZone | 400 | validation_error | IANA timezone |
| startTime > endTime | 400 | validation_error | Logical order |

---

## Retry Strategy Implementation

```python
import asyncio
import random
from enum import Enum
from dataclasses import dataclass
from typing import Callable, TypeVar, Awaitable

T = TypeVar('T')

class RetryDecision(Enum):
    RETRY = "retry"
    FAIL = "fail"
    REFRESH_AUTH = "refresh_auth"

@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: float = 0.1

async def execute_with_retry(
    func: Callable[[], Awaitable[T]],
    policy: RetryPolicy = None,
    on_401_refresh: Callable[[], Awaitable[None]] = None
) -> T:
    policy = policy or RetryPolicy()
    last_exception = None
    
    for attempt in range(policy.max_attempts):
        try:
            return await func()
        except CalAPIError as e:
            last_exception = e
            decision = classify_error(e)
            
            if decision == RetryDecision.FAIL:
                raise
            elif decision == RetryDecision.REFRESH_AUTH:
                if on_401_refresh and attempt == 0:
                    await on_401_refresh()
                    continue  # Retry immediately after refresh
                raise
            elif decision == RetryDecision.RETRY:
                if attempt == policy.max_attempts - 1:
                    raise
                
                delay = min(
                    policy.base_delay * (policy.exponential_base ** attempt),
                    policy.max_delay
                )
                # Add jitter
                delay *= (1 + random.uniform(-policy.jitter, policy.jitter))
                
                # If 429, use Retry-After header
                if e.http_status == 429 and e.retry_after:
                    delay = e.retry_after
                
                await asyncio.sleep(delay)
                continue
    
    raise last_exception

def classify_error(error: CalAPIError) -> RetryDecision:
    if error.http_status == 429:
        return RetryDecision.RETRY
    if error.http_status in (500, 502, 503, 504):
        return RetryDecision.RETRY
    if error.http_status == 401:
        return RetryDecision.REFRESH_AUTH
    if error.http_status == 409 and error.code == "conflict":
        # Could retry with different params, but safer to fail
        return RetryDecision.FAIL
    return RetryDecision.FAIL
```

---

## Error Handling by Integration Pattern

### Server-to-Server (API Key)
```python
async def create_booking_safe(client: CalClient, request: BookingRequest):
    try:
        return await client.create_booking(request)
    except CalAPIError as e:
        if e.http_status == 401:
            # API key rotated? Alert ops.
            alert_ops("API key invalid", error=e)
            raise ConfigurationError("API key invalid") from e
        elif e.http_status == 429:
            # Should be handled by client retry logic
            raise RateLimitError(e.retry_after) from e
        elif e.http_status == 409:
            raise SlotUnavailableError(e.details.get("alternativeSlots")) from e
        else:
            raise
```

### User-Facing (OAuth)
```python
async def create_booking_user(oauth_client: OAuthClient, request: BookingRequest):
    async def _try():
        tokens = await oauth_client.get_valid_tokens()
        client = CalClient(access_token=tokens.access_token)
        return await client.create_booking(request)
    
    async def _refresh():
        await oauth_client.refresh_tokens()
    
    return await execute_with_retry(_try, on_401_refresh=_refresh)
```

### Webhook Processor
```python
async def process_webhook(payload: dict):
    trigger = payload["triggerEvent"]
    
    try:
        if trigger == "BOOKING_CREATED":
            await handle_created(payload["payload"])
        elif trigger == "BOOKING_CANCELLED":
            await handle_cancelled(payload["payload"])
        # ...
    except Exception as e:
        # Log but don't crash — we already returned 200 to Cal.com
        logger.error("Webhook processing failed", extra={
            "trigger": trigger,
            "booking_uid": payload["payload"].get("uid"),
            "error": str(e)
        })
        # Send to dead letter queue for manual review
        await dlq.send(payload, error=str(e))
```

---

## Monitoring & Alerting

### Key Error Metrics
| Metric | Query | Alert Threshold |
|--------|-------|-----------------|
| 4xx rate | `rate(http_errors_4xx[5m])` | > 5% of requests |
| 5xx rate | `rate(http_errors_5xx[5m])` | > 1% of requests |
| 429 rate | `rate(http_429[5m])` | > 0.1/min |
| Auth failures | `rate(http_401[5m])` | > 0/min (should be 0) |
| Webhook processing errors | `rate(webhook_processing_errors[5m])` | > 0/min |

### Structured Error Logging
```json
{
  "timestamp": "2026-07-15T14:32:10.123Z",
  "level": "ERROR",
  "service": "booking-api",
  "operation": "create_booking",
  "http_status": 409,
  "error_code": "conflict",
  "error_message": "Time slot no longer available",
  "event_type_id": 123,
  "attendee_email_hash": "sha256:abc123...",
  "request_id": "req_xyz789",
  "retry_attempt": 1,
  "stack_trace": "..."
}
```

---

## Support Escalation

When contacting Cal.com support, include:
1. **Request ID** (from `details.requestId` or response headers)
2. **Timestamp** (ISO8601)
3. **Full request/response** (sanitized — no tokens!)
4. **API Key prefix** (first 8 chars only: `cal_live_abc1...`)
5. **Reproduction steps**
6. **Expected vs actual behavior**

### Support Channels
- **Email:** `support@cal.com`
- **Dashboard:** Help → Contact Support
- **Community:** `https://github.com/calcom/cal.com/discussions`
- **Status Page:** `https://status.cal.com`