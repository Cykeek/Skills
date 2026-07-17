# Cal.com API v2 — Rate Limits Reference

> **Source:** [Cal.com API Rate Limits](https://cal.com/docs/api-reference/rate-limits) | Response Headers
> **Last Updated:** July 2025

---

## Rate Limit Tiers

| Tier | Requests/Minute | Burst Allowance | Typical Use Case |
|------|-----------------|-----------------|------------------|
| **Default** | 120 | ~20 | Standard API keys, OAuth tokens |
| **Elevated** | 200 | ~50 | Approved via support request |
| **Platform (Legacy)** | 120 | ~20 | Deprecated — existing enterprise only |

> **Key Point:** OAuth and API Key authentication **share the same rate limit bucket** per user/team.

---

## Rate Limit Headers

Every API response includes:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 115
X-RateLimit-Reset: 1721059200
```

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests in current window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when window resets |

### On 429 Too Many Requests
```
HTTP/1.1 429 Too Many Requests
Retry-After: 45
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1721059200
```

| Header | Description |
|--------|-------------|
| `Retry-After` | Seconds to wait before retrying (use this!) |

---

## Token Bucket Algorithm (Client-Side Implementation)

Cal.com uses a **sliding window** approximated by token bucket. Implement client-side to avoid 429s:

```python
import time
import threading
from dataclasses import dataclass, field

@dataclass
class RateLimitBucket:
    limit: int = 120
    window_seconds: int = 60
    tokens: float = field(default=120.0)
    last_refill: float = field(default_factory=time.time)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def take(self, tokens: int = 1) -> float:
        """Returns seconds to wait (0 if available)."""
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            # Need to wait for refill
            needed = tokens - self.tokens
            wait_time = needed / (self.limit / self.window_seconds)
            return wait_time
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        if elapsed > 0:
            refill_rate = self.limit / self.window_seconds
            self.tokens = min(self.limit, self.tokens + elapsed * refill_rate)
            self.last_refill = now
    
    def update_from_headers(self, limit: int, remaining: int, reset: int):
        """Sync bucket with server state from response headers."""
        with self._lock:
            self.limit = limit
            self.tokens = remaining
            self.last_refill = time.time()
            # Calculate window from reset timestamp
            self.window_seconds = max(1, reset - int(time.time()))

# Usage
bucket = RateLimitBucket()

def make_request_with_rate_limit(client, method, url, **kwargs):
    # Pre-flight check
    wait = bucket.take(1)
    if wait > 0:
        time.sleep(wait)
    
    response = client.request(method, url, **kwargs)
    
    # Update bucket from response headers
    if "X-RateLimit-Limit" in response.headers:
        bucket.update_from_headers(
            limit=int(response.headers["X-RateLimit-Limit"]),
            remaining=int(response.headers["X-RateLimit-Remaining"]),
            reset=int(response.headers["X-RateLimit-Reset"])
        )
    
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        time.sleep(retry_after)
        return make_request_with_rate_limit(client, method, url, **kwargs)
    
    return response
```

---

## Per-Endpoint Rate Limit Notes

| Endpoint Category | Typical Limit | Notes |
|-------------------|---------------|-------|
| **Bookings** (CRUD) | 120/min | Includes availability checks |
| **Event Types** (CRUD) | 120/min | List endpoints may have higher limits |
| **Schedules** | 120/min | |
| **Webhooks** (CRUD) | 120/min | Delivery retries don't count |
| **Teams/Orgs** | 120/min | |
| **Profile** (`/me`) | 120/min | |
| **Availability/Slots** | 120/min | Can be called frequently for UI |

> **Bulk Operations:** If you need to create 50+ bookings, request elevated limits or batch with delays.

---

## Best Practices

### 1. Implement Exponential Backoff
```python
def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### 2. Use `Retry-After` Header on 429
```python
if response.status_code == 429:
    retry_after = int(response.headers.get("Retry-After", 60))
    time.sleep(retry_after)
    return retry_request()
```

### 3. Batch Requests When Possible
```python
# Instead of 10 sequential GET /bookings
# Use list endpoint with filters
GET /bookings?attendeeEmail=user@example.com&startTime=2026-01-01&endTime=2026-12-31
```

### 4. Cache Read-Heavy Operations
```python
# Cache event types for 5 minutes
@lru_cache(maxsize=1, ttl=300)
def get_event_types():
    return client.get("/event-types").json()
```

### 5. Monitor Rate Limit Usage
```python
# Log when remaining < 10% of limit
if bucket.tokens < bucket.limit * 0.1:
    logger.warning(f"Rate limit low: {bucket.tokens}/{bucket.limit} remaining")
```

---

## Elevated Limits Request Process

1. Email `support@cal.com` with subject: "Rate Limit Increase Request"
2. Include:
   - Your Cal.com account email / organization
   - Current limit (120/min)
   - Requested limit (max ~200/min)
   - Use case description (e.g., "High-volume booking integration for 500+ users")
   - Estimated peak RPS
3. Review typically 1-3 business days

---

## Rate Limit by Authentication Method

| Auth Method | Bucket Scope | Notes |
|-------------|--------------|-------|
| API Key (`cal_*` / `cal_live_*`) | Per key | Each key has independent bucket |
| OAuth Access Token | Per user+client | All tokens for same user+client share bucket |
| Platform (Deprecated) | Per managed user | Managed user tokens share platform bucket |

---

## Testing Rate Limits

```bash
# Quick test - should hit limit after ~120 requests
for i in {1..130}; do
  curl -s -o /dev/null -w "%{http_code} " \
    -H "Authorization: Bearer cal_live_xxx" \
    -H "cal-api-version: 2026-02-25" \
    "https://api.cal.com/v2/me"
  echo "Remaining: $(curl -s -I ... | grep -i x-ratelimit-remaining)"
done
```

---

## Common Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| No client-side bucket | Frequent 429s, wasted retries | Implement token bucket |
| Ignoring `Retry-After` | Immediate re-429, longer backoff | Always respect `Retry-After` |
| Shared bucket across services | One service starves others | Use separate API keys per service |
| Burst > 20 at startup | Immediate 429 | Stagger startup requests |
| No caching on reads | Unnecessary API calls | Cache `/me`, `/event-types`, `/schedules` |
| Not monitoring `X-RateLimit-Remaining` | Surprise 429s | Alert when < 10% remaining |