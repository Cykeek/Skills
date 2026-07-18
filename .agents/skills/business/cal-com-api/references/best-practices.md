# Cal.com API v2 — Best Practices & Integration Patterns

> **Source:** Cal.com Developer Docs, Community Patterns, Production Experience
> **Last Updated:** July 2025

---

## Core Principles

### 1. Schema-First Development
- **Every request/response validated** against JSON Schema before hitting network
- **Fail fast** — invalid data never leaves your process
- **Version schemas** alongside API version

### 2. Idempotency by Default
- **Webhooks:** Track `cal-webhook-id` with 7-day TTL
- **Bookings:** Use `metadata.idempotencyKey` for safe retries
- **Event Types:** `slug` is your natural key

### 3. Observability Built-In
- Structured logging: method, endpoint, latency, status, rate-limit-remaining
- Audit logs with sanitized request/response for debugging
- Correlation IDs across async boundaries

### 4. Graceful Degradation
- **Reads cached** (event types, schedules, profile) — survive API outage
- **Writes queued** with retry — survive transient failures
- **Webhooks async** — 2xx returned immediately

---

## Authentication Patterns

### API Keys (Server-to-Server)
```python
# Environment separation
CAL_API_KEY_PROD = "cal_live_prod_..."      # Production only
CAL_API_KEY_STAGING = "cal_staging_..."     # Staging only  
CAL_API_KEY_CI = "cal_ci_..."               # CI/CD only (test prefix)

# Rotation: Quarterly via script
# Storage: AWS Secrets Manager / Vault / Azure Key Vault
```

### OAuth (User-Facing Apps)
```python
# Minimal scopes
SCOPES = ["BOOKING_READ", "BOOKING_WRITE", "EVENT_TYPE_READ"]

# PKCE for public clients (SPA, mobile)
# Auto-refresh on 401
async def get_valid_token():
    if token_expired():
        await refresh_token()
    return access_token
```

### Token Storage by Environment
| Environment | Storage |
|-------------|---------|
| Production | AWS Secrets Manager / HashiCorp Vault / Azure Key Vault |
| Staging | Same as prod (separate namespace) |
| Local Dev | `.env` (gitignored) + `direnv` |
| CI/CD | GitHub Actions Secrets / GitLab CI Variables |

---

## Request/Response Handling

### Required Headers (Every Request)
```python
DEFAULT_HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "cal-api-version": "2026-02-25",  # Pin in config
    "Content-Type": "application/json",
    "User-Agent": "my-app/1.0.0 (cal-booking-skill)"
}
```

### Validate Before Send
```python
from cal_booking_skill.validation import validate_request

request_data = {"start": "2026-07-20T14:00:00Z", ...}
validate_request("booking-request", request_data)  # Raises ValidationError
```

### Unwrap Response Envelope
```python
def parse_response(response: httpx.Response) -> dict:
    data = response.json()
    if data.get("status") == "error":
        raise CalAPIError.from_response(data["data"], response.headers)
    return data["data"]  # Unwrap {status, data} envelope
```

---

## Booking Flow Patterns

### Pattern 1: Direct Booking (Known Event Type)
```python
async def book_known_event(
    client: CalClient,
    event_type_id: int,
    start_utc: str,
    attendee: Attendee
) -> Booking:
    request = CreateBookingRequest(
        start=start_utc,
        attendee=attendee,
        eventTypeId=event_type_id,
        metadata={"idempotencyKey": f"booking_{uuid.uuid4()}"}
    )
    response = await client.create_booking(request)
    if response.data.status != "ACCEPTED":
        raise BookingNotConfirmedError(response.data)
    return response.data
```

### Pattern 2: Availability-First Booking
```python
async def book_with_availability(
    client: CalClient,
    event_type_slug: str,
    username: str,
    preferred_start: datetime,
    attendee: Attendee,
    window_days: int = 7
) -> Booking:
    # 1. Resolve event type
    event_type = await client.get_event_type_by_slug(event_type_slug, username)
    
    # 2. Check availability
    slots = await client.get_availability(
        event_type_id=event_type.id,
        start=preferred_start,
        end=preferred_start + timedelta(days=window_days),
        time_zone=attendee.timeZone
    )
    
    if not slots:
        raise NoAvailabilityError("No slots in preferred window")
    
    # 3. Book first available (or let user choose)
    return await client.create_booking(CreateBookingRequest(
        start=slots[0].start,
        attendee=attendee,
        eventTypeId=event_type.id
    ))
```

### Pattern 3: Collective/Round-Robin Team Booking
```python
async def book_team_round_robin(
    client: CalClient,
    team_slug: str,
    event_type_slug: str,
    start_utc: str,
    attendee: Attendee
) -> Booking:
    # Team event types use teamSlug + eventTypeSlug
    request = CreateBookingRequest(
        start=start_utc,
        attendee=attendee,
        eventTypeSlug=event_type_slug,
        username=team_slug  # Team slug goes in username field
    )
    return await client.create_booking(request)
```

---

## Caching Strategy

| Resource | TTL | Invalidation |
|----------|-----|--------------|
| `/me` (profile) | 5 min | On 401, or explicit refresh |
| `/event-types` | 5 min | On create/update/delete webhook |
| `/schedules` | 5 min | On webhook |
| `/teams/{id}` | 10 min | Rarely changes |
| Availability/slots | **No cache** | Real-time required |

```python
from functools import lru_cache
import time

class CachedCalClient:
    def __init__(self, client: CalClient):
        self.client = client
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes
    
    async def get_event_types(self):
        key = "event_types"
        if key in self._cache and time.time() - self._cache[key][1] < self._cache_ttl:
            return self._cache[key][0]
        
        data = await self.client.get_event_types()
        self._cache[key] = (data, time.time())
        return data
    
    def invalidate(self, key: str):
        self._cache.pop(key, None)
```

---

## Webhook Processing

### Signature Verification (Mandatory)
```python
# Use raw body — parsed JSON breaks signature!
raw_body = await request.body()
verify_signature(raw_body, headers, signing_secret)
```

### Idempotency (Two Layers)
```python
# Layer 1: Webhook ID (7-day TTL)
async def check_webhook_idempotency(webhook_id: str) -> bool:
    return await redis.set(f"webhook:{webhook_id}", "1", nx=True, ex=7*24*3600)

# Layer 2: Business key (booking UID)
async def process_booking_created(payload):
    booking_uid = payload["payload"]["uid"]
    existing = await db.bookings.find_one({"cal_uid": booking_uid})
    if existing and existing["status"] == payload["payload"]["status"]:
        return  # Already processed
    await upsert_booking(payload["payload"])
```

### Async Processing (Return 2xx < 10s)
```python
@app.post("/webhooks/cal")
async def cal_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await verify_webhook(request)
    background_tasks.add_task(process_webhook_async, payload)
    return Response(status_code=200)  # Immediate!
```

---

## Rate Limiting

### Client-Side Token Bucket
```python
class RateLimitBucket:
    def __init__(self, limit=120, window=60):
        self.limit = limit
        self.window = window
        self.tokens = limit
        self.last_refill = time.time()
        self.lock = asyncio.Lock()
    
    async def take(self, tokens=1) -> float:
        async with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            needed = tokens - self.tokens
            return needed / (self.limit / self.window)
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        if elapsed > 0:
            self.tokens = min(self.limit, self.tokens + elapsed * self.limit / self.window)
            self.last_refill = now
    
    def update_from_headers(self, limit: int, remaining: int, reset: int):
        self.limit = limit
        self.tokens = remaining
        self.last_refill = time.time()
```

### Respect Headers
```python
async def make_request(self, ...):
    wait = await self.bucket.take()
    if wait > 0:
        await asyncio.sleep(wait)
    
    response = await self.client.request(...)
    
    # Sync bucket with server
    if "X-RateLimit-Limit" in response.headers:
        self.bucket.update_from_headers(
            int(response.headers["X-RateLimit-Limit"]),
            int(response.headers["X-RateLimit-Remaining"]),
            int(response.headers["X-RateLimit-Reset"])
        )
    
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        await asyncio.sleep(retry_after)
        return await self.make_request(...)  # Retry once
    
    return response
```

---

## Timezone Handling

### Always Use IANA Timezones
```python
# ✅ Good
attendee.timeZone = "America/Los_Angeles"
attendee.timeZone = "Europe/London"
attendee.timeZone = "Asia/Tokyo"

# ❌ Bad
attendee.timeZone = "PST"      # Ambiguous
attendee.timeZone = "UTC-8"    # No DST
attendee.timeZone = "GMT-8"    # No DST
```

### UTC for API, IANA for Display
```python
# API requests: ALWAYS UTC ISO8601
start_utc = "2026-07-20T21:00:00Z"  # 2 PM PDT = 9 PM UTC

# User display: Convert to their IANA zone
from zoneinfo import ZoneInfo
user_tz = ZoneInfo("America/Los_Angeles")
display_time = datetime.fromisoformat(start_utc.replace("Z", "+00:00")).astimezone(user_tz)
# 2026-07-20 14:00:00-07:00
```

---

## Error Handling by Pattern

### Server-to-Server (API Key)
```python
try:
    return await client.create_booking(request)
except CalAPIError as e:
    if e.http_status == 401:
        alert_ops("API key invalid")  # Key rotated?
        raise ConfigError("API key invalid")
    elif e.http_status == 429:
        raise RateLimitError(e.retry_after)
    elif e.http_status == 409:
        raise SlotUnavailableError(e.details.get("alternativeSlots"))
    raise
```

### User-Facing (OAuth)
```python
async def user_action(oauth: OAuthClient, action):
    async def _try():
        tokens = await oauth.get_valid_tokens()
        client = CalClient(access_token=tokens.access_token)
        return await action(client)
    
    async def _refresh():
        await oauth.refresh_tokens()
    
    return await execute_with_retry(_try, on_401_refresh=_refresh)
```

---

## Testing Strategy

### Unit Tests: Schema Validation
```python
def test_booking_request_schema():
    valid = {"start": "2026-07-20T14:00:00Z", "attendee": {...}, "eventTypeId": 123}
    validate_request("booking-request", valid)  # No error
    
    invalid = {"start": "not-a-date", ...}
    with pytest.raises(ValidationError):
        validate_request("booking-request", invalid)
```

### Integration Tests: Mock Server
```python
@pytest.fixture
def mock_cal_api(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.cal.com/v2/bookings",
        json={"status": "success", "data": {"uid": "abc123", ...}},
        status_code=201,
        headers={"X-RateLimit-Limit": "120", "X-RateLimit-Remaining": "119"}
    )
    return httpx_mock

async def test_create_booking(mock_cal_api, client):
    booking = await client.create_booking(valid_request)
    assert booking.uid == "abc123"
```

### Contract Tests: Schema Compliance
```python
def test_booking_response_matches_schema():
    response = {"status": "success", "data": {...}}
    validate_response("api-response", response)
    validate_response("booking-response", response["data"])
```

---

## Deployment Checklist

### Pre-Deploy
- [ ] All schemas validated against test payloads
- [ ] Rate limit bucket configured for expected load
- [ ] Webhook signature verification tested
- [ ] Idempotency keys generated for all writes
- [ ] Error handling covers all documented codes
- [ ] Structured logging includes correlation IDs
- [ ] Secrets not in code (API keys, webhook secrets)

### Post-Deploy
- [ ] Smoke test: `GET /me` succeeds
- [ ] Smoke test: `POST /bookings` creates booking
- [ ] Webhook endpoint receives test event
- [ ] Rate limit headers present in responses
- [ ] Metrics: latency, error rate, 429 rate
- [ ] Alerts: 4xx > 5%, 5xx > 1%, 429 > 0.1/min

---

## Migration Guide: Platform → OAuth/API Key

| Platform Feature | OAuth/API Key Equivalent |
|-----------------|--------------------------|
| `x-cal-client-id` + `x-cal-secret-key` | `Authorization: Bearer <token>` |
| Managed users | OAuth with user consent + `offline_access` scope |
| Team-scoped access | Team-prefixed scopes (`TEAM_BOOKING_WRITE`) |
| Organization access | Org-prefixed scopes (`ORG_EVENT_TYPE_READ`) |

---

## Performance Tips

1. **Batch reads** — Use list endpoints with filters instead of N individual GETs
2. **Cache aggressively** — Event types, schedules, profile change rarely
3. **Async webhooks** — Never process synchronously
4. **Connection pooling** — Reuse HTTP client (httpx.AsyncClient)
5. **Compression** — Enable gzip: `Accept-Encoding: gzip`

---

## Security Checklist

- [ ] API keys in secret manager, never in code
- [ ] OAuth tokens encrypted at rest
- [ ] Webhook signing secret in secret manager
- [ ] HTTPS enforced for all webhook URLs
- [ ] Timestamp validation on webhooks (5 min window)
- [ ] Constant-time HMAC comparison
- [ ] Idempotency on all webhook processing
- [ ] Rate limiting on webhook endpoint
- [ ] Input validation on all user data
- [ ] Audit logging for all booking operations
- [ ] Regular key rotation (quarterly)
- [ ] Minimal OAuth scopes requested