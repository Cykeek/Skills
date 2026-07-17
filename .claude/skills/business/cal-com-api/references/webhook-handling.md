# Cal.com API v2 — Webhook Handling Deep Dive

> **Source:** [Cal.com Webhooks Guide](https://cal.com/docs/webhooks) | [API Reference](https://cal.com/docs/api-reference/v2/webhooks)
> **Last Updated:** July 2025

---

## Webhook Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CAL.COM WEBHOOK FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    Booking Event    ┌──────────┐    HTTPS POST    ┌─────────┐ │
│  │  USER    │ ──────────────────▶ │ CAL.COM  │ ──────────────▶  │ YOUR    │ │
│  │  BOOKS   │                     │  QUEUES  │                  │  APP    │ │
│  └──────────┘                     └──────────┘                  └────┬────┘ │
│                                                                       │      │
│                              ┌──────────────────────────────────────┘      │
│                              ▼                                             │
│                    ┌─────────────────────┐                                 │
│                    │   VERIFICATION      │                                 │
│                    │  1. Timestamp check │                                 │
│                    │  2. HMAC-SHA256     │                                 │
│                    │  3. Idempotency     │                                 │
│                    └──────────┬──────────┘                                 │
│                               │                                            │
│                    ┌──────────┴──────────┐                                 │
│                    ▼                     ▼                                 │
│             ┌──────────┐           ┌──────────┐                            │
│             │  VALID   │           │  INVALID │                            │
│             │ Process  │           │  Reject  │                            │
│             │ Event    │           │  401     │                            │
│             └──────────┘           └──────────┘                            │
│                    │                                                    │
│                    ▼                                                    │
│             ┌──────────────────┐                                        │
│             │  RESPOND 2xx     │                                        │
│             │  WITHIN 10 SECS  │                                        │
│             └──────────────────┘                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Trigger Events Reference

### Booking Lifecycle Triggers

| Trigger | Fired When | Payload Key Fields |
|---------|------------|-------------------|
| `BOOKING_CREATED` | Booking confirmed (instant or accepted) | `uid`, `status=ACCEPTED`, `startTime`, `endTime`, `attendees`, `organizer`, `eventType` |
| `BOOKING_CANCELLED` | Attendee or host cancels | `uid`, `status=CANCELLED`, `cancelReason`, `cancelledBy` |
| `BOOKING_RESCHEDULED` | Time changed | `uid`, `rescheduledFromUid`, `rescheduledToUid`, old/new `startTime`/`endTime` |
| `BOOKING_REJECTED` | Host rejects pending booking | `uid`, `status=REJECTED`, `rejectReason` |
| `BOOKING_PAID` | Payment completed (paid events) | `uid`, `payment: {amount, currency, provider}` |

### Meeting Lifecycle Triggers

| Trigger | Fired When | Use Case |
|---------|------------|----------|
| `MEETING_STARTED` | `startTime` reached | Start recording, notify participants, update CRM status |
| `MEETING_ENDED` | `endTime` reached | Stop recording, trigger post-meeting workflow, send feedback |

### Form Trigger

| Trigger | Fired When | Use Case |
|---------|------------|----------|
| `FORM_SUBMITTED` | Booking form submitted (before confirmation) | Pre-qualification, enrichment, conditional logic |

---

## Payload Structures

### BOOKING_CREATED (Full Example)
```json
{
  "triggerEvent": "BOOKING_CREATED",
  "createdAt": "2026-07-15T14:30:00.000Z",
  "payload": {
    "uid": "abc123xyz789",
    "id": 456,
    "title": "30min Discovery Call with John Doe",
    "description": "Initial discovery call for Acme Corp",
    "startTime": "2026-07-20T17:00:00.000Z",
    "endTime": "2026-07-20T17:30:00.000Z",
    "status": "ACCEPTED",
    "attendees": [
      {
        "id": 789,
        "name": "John Doe",
        "email": "john@acme.com",
        "timeZone": "America/Los_Angeles",
        "phoneNumber": "+15551234567",
        "language": "en",
        "metadata": { "source": "website", "campaign": "summer-2026" }
      }
    ],
    "organizer": {
      "id": 1,
      "name": "Jane Smith",
      "email": "jane@cal.com",
      "timeZone": "America/New_York"
    },
    "eventType": {
      "id": 123,
      "title": "30 Minute Discovery Call",
      "slug": "discovery-call",
      "lengthInMinutes": 30,
      "schedulingType": "PERSONAL"
    },
    "location": "https://meet.google.com/abc-defg-hij",
    "metadata": {
      "utm_source": "website",
      "utm_campaign": "summer-2026",
      "idempotencyKey": "booking_req_abc123"
    },
    "cancelReason": null,
    "rescheduledFromUid": null,
    "rescheduledToUid": null
  }
}
```

### BOOKING_CANCELLED
```json
{
  "triggerEvent": "BOOKING_CANCELLED",
  "createdAt": "2026-07-18T10:15:00.000Z",
  "payload": {
    "uid": "abc123xyz789",
    "id": 456,
    "status": "CANCELLED",
    "cancelReason": "Schedule conflict",
    "cancelledBy": "ATTENDEE",  // or "HOST"
    "attendees": [{ "id": 789, "email": "john@acme.com" }],
    "eventType": { "id": 123, "title": "30 Minute Discovery Call" }
  }
}
```

### BOOKING_RESCHEDULED
```json
{
  "triggerEvent": "BOOKING_RESCHEDULED",
  "createdAt": "2026-07-18T10:15:00.000Z",
  "payload": {
    "uid": "new_uid_456",
    "id": 457,
    "status": "ACCEPTED",
    "startTime": "2026-07-21T17:00:00.000Z",
    "endTime": "2026-07-21T17:30:00.000Z",
    "rescheduledFromUid": "abc123xyz789",
    "rescheduledToUid": "new_uid_456",
    "attendees": [...],
    "eventType": { "id": 123 }
  }
}
```

### MEETING_STARTED / MEETING_ENDED
```json
{
  "triggerEvent": "MEETING_STARTED",
  "createdAt": "2026-07-20T17:00:00.000Z",
  "payload": {
    "uid": "abc123xyz789",
    "id": 456,
    "startTime": "2026-07-20T17:00:00.000Z",
    "endTime": "2026-07-20T17:30:00.000Z",
    "eventType": { "id": 123 },
    "attendees": [{ "id": 789, "email": "john@acme.com" }],
    "organizer": { "id": 1, "email": "jane@cal.com" },
    "location": "https://meet.google.com/abc-defg-hij"
  }
}
```

---

## Signature Verification (Critical)

### Algorithm
```
signature = HMAC-SHA256(
    key = webhook_signing_secret,
    message = raw_body + "." + timestamp
)
```

### Headers to Verify
| Header | Example | Purpose |
|--------|---------|---------|
| `cal-signature` | `sha256=a1b2c3d4e5f6...` | HMAC signature |
| `cal-timestamp` | `1721059200` | Unix epoch seconds (replay protection) |
| `cal-webhook-id` | `evt_abc123xyz` | Unique delivery ID (idempotency) |

### Implementation (Python)
```python
import hmac
import hashlib
import time
from fastapi import Request, HTTPException, Header

WEBHOOK_SECRET = "your_signing_secret_from_cal_dashboard"  # NOT the 'secret' field!
IDEMPOTENCY_TTL = 7 * 24 * 3600  # 7 days

async def verify_webhook(
    request: Request,
    cal_signature: str = Header(..., alias="cal-signature"),
    cal_timestamp: str = Header(..., alias="cal-timestamp"),
    cal_webhook_id: str = Header(..., alias="cal-webhook-id")
) -> dict:
    raw_body = await request.body()
    
    # 1. Timestamp check (5 min tolerance)
    try:
        timestamp = int(cal_timestamp)
    except ValueError:
        raise HTTPException(400, "Invalid timestamp")
    
    if abs(time.time() - timestamp) > 300:
        raise HTTPException(400, "Timestamp too old (replay attack?)")
    
    # 2. Signature verification
    if not cal_signature.startswith("sha256="):
        raise HTTPException(400, "Invalid signature format")
    
    expected_signature = cal_signature[7:]  # Remove "sha256="
    message = raw_body + b"." + cal_timestamp.encode()
    computed = hmac.new(
        WEBHOOK_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(computed, expected_signature):
        raise HTTPException(401, "Invalid signature")
    
    # 3. Idempotency check
    redis_key = f"webhook:{cal_webhook_id}"
    if not await redis.set(redis_key, "1", nx=True, ex=IDEMPOTENCY_TTL):
        raise HTTPException(200, "Duplicate webhook (idempotent)")
    
    return json.loads(raw_body)
```

### Implementation (Node.js)
```javascript
const crypto = require('crypto');
const REDIS_TTL = 7 * 24 * 60 * 60;

async function verifyWebhook(req, res, next) {
  const rawBody = req.rawBody; // Need raw body parser!
  const signature = req.headers['cal-signature'];
  const timestamp = req.headers['cal-timestamp'];
  const webhookId = req.headers['cal-webhook-id'];
  
  // 1. Timestamp
  const ts = parseInt(timestamp, 10);
  if (isNaN(ts) || Math.abs(Date.now()/1000 - ts) > 300) {
    return res.status(400).send('Invalid timestamp');
  }
  
  // 2. HMAC
  const expected = signature.replace('sha256=', '');
  const message = rawBody + '.' + timestamp;
  const computed = crypto
    .createHmac('sha256', process.env.CAL_WEBHOOK_SECRET)
    .update(message)
    .digest('hex');
  
  if (!crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(expected))) {
    return res.status(401).send('Invalid signature');
  }
  
  // 3. Idempotency
  const key = `webhook:${webhookId}`;
  const exists = await redis.set(key, '1', 'NX', 'EX', REDIS_TTL);
  if (!exists) {
    return res.status(200).send('Duplicate');
  }
  
  next();
}
```

### ⚠️ Critical: Raw Body Required
**You MUST access the raw request body** — parsed JSON will have different whitespace/formatting and fail verification.

| Framework | How to Get Raw Body |
|-----------|---------------------|
| FastAPI | `@app.post("/webhook")` + `Request` object → `await request.body()` |
| Express | `app.use(express.raw({type: 'application/json'}))` |
| Flask | `request.get_data()` |
| Next.js | `export const config = { api: { bodyParser: false } }` |

---

## Idempotency Strategy

### Why It Matters
- Cal.com retries failed deliveries (up to 72 hours)
- Network issues can cause duplicate deliveries
- Your processing must be **exactly-once** semantically

### Implementation Layers

```python
# Layer 1: Webhook ID deduplication (7-day TTL)
async def check_idempotency(webhook_id: str) -> bool:
    return await redis.set(f"webhook:{webhook_id}", "1", nx=True, ex=7*24*3600)

# Layer 2: Business key deduployment (booking UID)
async def process_booking_created(payload: dict):
    booking_uid = payload["payload"]["uid"]
    
    # Check if we've already processed this booking
    existing = await db.bookings.find_one({"cal_uid": booking_uid})
    if existing and existing["status"] == payload["payload"]["status"]:
        return  # Already handled
    
    # Process...
    await upsert_booking(payload["payload"])

# Layer 3: Idempotency key in metadata (for creates)
booking_request = CreateBookingRequest(
    ...
    metadata={"idempotencyKey": "your-unique-key-per-user-action"}
)
```

---

## Retry Behavior & Response Requirements

### Cal.com Retry Schedule
| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 10 seconds |
| 3 | 1 minute |
| 4 | 10 minutes |
| 5 | 1 hour |
| 6 | 6 hours |
| 7 | 24 hours |
| 8+ | Every 24 hours (up to 72 hours total) |

### Your Response Requirements
| Requirement | Detail |
|-------------|--------|
| **Response Time** | **< 10 seconds** (else marked as failed, triggers retry) |
| **Success Code** | **2xx** (200, 201, 202, 204 all work) |
| **Failure Code** | Any non-2xx → retry |
| **Timeout** | Cal.com waits ~15s then treats as failure |

### Best Practice: Async Processing
```python
@app.post("/webhooks/cal")
async def cal_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await verify_webhook(request)
    
    # IMMEDIATELY return 200
    background_tasks.add_task(process_webhook_async, payload)
    return Response(status_code=200)

async def process_webhook_async(payload: dict):
    try:
        trigger = payload["triggerEvent"]
        data = payload["payload"]
        
        if trigger == "BOOKING_CREATED":
            await handle_booking_created(data)
        elif trigger == "BOOKING_CANCELLED":
            await handle_booking_cancelled(data)
        # ... etc
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}", extra={"payload": payload})
        # Don't re-raise — we already returned 200
        # Alert via monitoring system instead
```

---

## Local Development & Testing

### ngrok / Cloudflare Tunnel
```bash
# Expose local port 8000
ngrok http 8000

# Use https URL in Cal.com webhook config
# https://abc123.ngrok.io/webhooks/cal
```

### Local Signature Testing
```python
def generate_test_signature(payload: dict, secret: str, timestamp: int = None) -> dict:
    """Generate headers for local testing."""
    if timestamp is None:
        timestamp = int(time.time())
    
    raw_body = json.dumps(payload, separators=(',', ':')).encode()
    message = raw_body + b"." + str(timestamp).encode()
    signature = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    
    return {
        "cal-signature": f"sha256={signature}",
        "cal-timestamp": str(timestamp),
        "cal-webhook-id": f"test_{timestamp}"
    }

# Test
test_payload = {"triggerEvent": "BOOKING_CREATED", "createdAt": "...", "payload": {...}}
headers = generate_test_signature(test_payload, "my_secret")
# POST to localhost with these headers
```

### Webhook Testing Checklist
- [ ] Signature verification passes
- [ ] Timestamp within 5 min
- [ ] Duplicate webhook-id returns 200 (idempotent)
- [ ] Response < 10 seconds
- [ ] Async processing doesn't block response
- [ ] All trigger types handled
- [ ] Error in processing doesn't crash webhook endpoint
- [ ] Monitoring alerts on processing failures (not delivery failures)

---

## Security Checklist

- [ ] **Signing secret** stored in secret manager (not `.env` committed)
- [ ] **HTTPS only** for subscriber URL (Cal.com enforces)
- [ ] **Timestamp validation** prevents replay attacks
- [ ] **Constant-time comparison** for HMAC
- [ ] **Idempotency** at webhook ID + business key level
- [ ] **Rate limiting** on webhook endpoint (prevent DoS)
- [ ] **Input validation** on payload before processing
- [ ] **Audit log** of all webhook events (received, verified, processed)
- [ ] **Alerting** on verification failures (potential attack)

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 on verified webhook | Using `secret` field instead of `signingSecret` | Use `signingSecret` from webhook creation response |
| "Invalid signature" | Body parsed as JSON then re-serialized | Use **raw body** |
| Duplicate processing | No idempotency check | Add Redis/webhook-id check |
| Webhook never fires | `active: false` or wrong triggers | Check webhook config in Cal.com |
| Timeout errors | Processing > 10s | Move to async/background |
| Missing events | Wrong trigger list | Verify `triggers` array includes needed events |