# Cal.com Booking Skill — Visual Architecture & Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                           CAL.COM BOOKING SKILL ARCHITECTURE                                   │
│                      (API-First • Schema-Validated • Rate-Limit Aware)                        │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────────────────────────┐
                              │           USER INVOCATION                 │
                              │  (CLI: create-booking | list-bookings     │
                              │   create-event-type | list-event-types   │
                              │   setup-webhook | test-auth              │
                              │   check-availability)                     │
                              └─────────────────────┬────────────────────┘
                                                    │
                                                    ▼
                              ┌──────────────────────────────────────────┐
                              │        INITIALIZATION (Implicit)          │
                              │  ┌────────────────────────────────────┐  │
                              │  │  WORKSPACE ROOT                       │  │
                              │  │  └── cal-booking-output/           │  │  ◄─── Created ONCE
                              │  │      (master folder)               │  │      on first invoke
                              │  └────────────────────────────────────┘  │
                              └─────────────────────┬────────────────────┘
                                                    │
                                                    ▼
                              ┌──────────────────────────────────────────┐
                              │        TASK SUBFOLDER CREATION            │
                              │  cal-booking-output/                     │
                              │  └── {command}_{resource}_{timestamp}/   │  ◄─── Auto-created per run
                              │      ├─ create-booking_.../              │
                              │      ├─ list-event-types_.../            │
                              │      ├─ setup-webhook_.../               │
                              │      └─ check-availability_.../          │
                              └─────────────────────┬────────────────────┘
                                                    │
                                                    ▼
        ┌─────────────────────────────────────────────────────────────────────────────────────┐
        │                              3-STAGE PIPELINE (all commands)                           │
        │                                                                                       │
        │  ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────────────┐    │
        │  │  STAGE 1     │───▶│    STAGE 2       │───▶│   STAGE 3    │───▶│   STAGE 4    │    │
        │  │  INPUT       │    │  API EXECUTION   │    │  VALIDATION  │    │  OUTPUT      │    │
        │  │  VALIDATION  │    │  (Rate-Limited)  │    │  GATES       │    │  ARTIFACTS   │    │
        │  └──────┬───────┘    └────────┬─────────┘    └──────┬───────┘    └──────┬───────┘    │
        │         │                     │                   │                   │            │
        │         ▼                     ▼                   ▼                   ▼            │
        │  ┌─────────────┐      ┌───────────────┐     ┌─────────────┐      ┌──────────────┐  │
        │  │ Schema      │      │ Cal.com API   │     │ Schema      │      │ JSON Output  │  │
        │  │ Validation  │      │ v2 Client     │     │ Validation  │      │ Markdown Sum │  │
        │  │ Rate Check  │      │ Auth: Bearer  │     │ Gate 1-6    │      │ Audit Log    │  │
        │  │ Auth Verify │      │ cal-api-ver   │     │ Retry Logic │      │ Debug Curl   │  │
        │  └─────────────┘      └───────────────┘     └─────────────┘      └──────────────┘  │
        │                                                                                       │
        └─────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
                              ┌──────────────────────────────────────────┐
                              │           BUILD & OUTPUT                  │
                              │  ┌────────────────────────────────────┐  │
                              │  │ cal-booking-output/                │  │
                              │  │ └── create-booking_acme_20260715_  │  │
                              │  │     ├─ booking-response.json       │  │ ← Raw API response
                              │  │     ├─ booking-summary.md          │  │ ← Human-readable
                              │  │     ├─ curl-command.sh             │  │ ← Reproducible request
                              │  │     ├─ validation-report.json      │  │ ← All gates PASS/FAIL
                              │  │     └─ audit-log.json              │  │ ← Rate-limit trace
                              │  └────────────────────────────────────┘  │
                              └──────────────────────────────────────────┘
                                                    │
                                                    ▼
                              ┌──────────────────────────────────────────┐
                              │           USER ACTION                     │
                              │  1. Review booking-summary.md            │
                              │  2. Re-run with curl-command.sh if needed│
                              │  3. Check validation-report.json         │
                              │  4. Debug with audit-log.json            │
                              └──────────────────────────────────────────┘
```

---

## Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              PYTHON MODULE LAYER (cal_booking_skill/)              │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌──────────────┐   ┌────────────────┐   ┌──────────────┐   ┌──────────────────┐  │
│  │ api_client   │   │ validation     │   │ output_mgr   │   │ cli              │  │
│  │ .CalClient   │   │ .validate_*    │   │ .OutputMgr   │   │ .main()          │  │
│  │ .request()   │   │ .gate_*()      │   │ .write_*()   │   │ .create_booking()│  │
│  │ .rate_limit  │   │ .SchemaEnum    │   │ .ensure_dir()│   │ .list_bookings() │  │
│  └──────┬───────┘   └───────┬────────┘   └──────┬───────┘   └────────┬─────────┘  │
│         │                   │                   │                   │            │
│         ▼                   ▼                   ▼                   ▼            │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                        CAL.COM API v2 CONTRACT                              │  │
│  │  Base: https://api.cal.com/v2                                              │  │
│  │  Auth: Bearer <cal_*|cal_live_*> | OAuth | Platform (deprecated)          │  │
│  │  Version: cal-api-version: YYYY-MM-DD (required on most endpoints)        │  │
│  │  Rate Limit: 120 req/min (base), up to 200 via support                    │  │
│  │  Envelope: { "status": "success|error", "data": {...} }                   │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## CLI Command → Pipeline Mapping

```
┌────────────────────┬────────────────────────────────────────────────────────────────┐
│ COMMAND            │ PIPELINE EXECUTED                                               │
├────────────────────┼────────────────────────────────────────────────────────────────┤
│ create-booking     │ Validate → POST /bookings → Validate Response → Output         │
│ list-bookings      │ Validate → GET /bookings → Validate Response → Output          │
│ create-event-type  │ Validate → POST /event-types → Validate Response → Output      │
│ list-event-types   │ Validate → GET /event-types → Validate Response → Output       │
│ setup-webhook      │ Validate → POST /webhooks → Validate Response → Output         │
│ test-auth          │ Validate → GET /me → Validate Response → Output                │
│ check-availability │ Validate → GET /slots (or POST /bookings/availability) → Output│
└────────────────────┴────────────────────────────────────────────────────────────────┘
```

---

## Artifact Flow (What Goes Where)

```
TASK SUBFOLDER: cal-booking-output/create-booking_acme_20260715_143510/

INPUTS (provided by user)          GENERATED ARTIFACTS                    PURPOSE
─────────────────────────          ─────────────────────                   ────────
--event-type-id=123       ──────▶  booking-response.json      ← Raw API response envelope
--start="2026-07-20T14:00Z"       booking-summary.md          ← Human-readable confirmation
--attendee-name="John"            curl-command.sh             ← Reproducible cURL for debugging
--attendee-tz="America/LA"        validation-report.json      ← All 6 gates PASS/FAIL
--api-key=cal_live_...            audit-log.json              ← Rate-limit, timing, retries
--api-version=2026-02-25          debug-request.json          ← Exact request sent
```

---

## Validation Gates (All Must Pass)

```
GATE 1  request_schema       → Request payload matches endpoint schema (booking-request, etc.)
GATE 2  auth_header          → Authorization: Bearer <token> + cal-api-version present
GATE 3  rate_limit_pre       → Pre-flight: estimated requests within 120/min budget
GATE 4  response_schema      → Response envelope {status, data} matches api-response schema
GATE 5  rate_limit_post      → Post-flight: X-RateLimit-* headers within limits
GATE 6  error_handling       → 4xx/5xx responses parsed, retry-after respected, actionable msg
```

---

## Dual Output Modes

```
┌─────────────────┬──────────────────────────────┬──────────────────────────────┐
│ PROPERTY        │ json (default)               │ markdown                     │
├─────────────────┼──────────────────────────────┼──────────────────────────────┤
│ Primary Artifact│ *.json                       │ *.md                         │
│ Machine Readable│ ✅ Full envelope             │ ❌ Summary only              │
│ Human Readable  │ ❌ Raw                       │ ✅ Formatted tables          │
│ Debug Artifacts │ curl-command.sh + audit-log  │ curl-command.sh + audit-log  │
│ CI/CD Friendly  │ ✅                           │ ⚠️ Requires parsing          │
└─────────────────┴──────────────────────────────┴──────────────────────────────┘
```

---

## First Invocation — What Happens Automatically

```
$ cal-booking create-booking --event-type-id 123 --start "2026-07-20T14:00:00Z" \
    --attendee-name "John Doe" --attendee-email "john@example.com" \
    --attendee-timezone "America/Los_Angeles" --api-key cal_live_xxx

Step 1: Check workspace root for cal-booking-output/
        └── NOT FOUND → CREATE cal-booking-output/

Step 2: Generate task folder name
        └── create-booking_acme_20260715_143510/

Step 3: Create task subfolder
        └── cal-booking-output/create-booking_acme_20260715_143510/

Step 4: Stage 1 - Validate Input
        └── Schema: booking-request.json ✓
        └── Auth header format ✓
        └── cal-api-version present ✓
        └── Rate limit pre-check ✓ (1 req estimated)

Step 5: Stage 2 - Execute API Call
        └── POST https://api.cal.com/v2/bookings
        └── Headers: Authorization, cal-api-version, Content-Type
        └── Body: validated booking request
        └── Rate limit: wait if needed (exponential backoff)

Step 6: Stage 3 - Validate Response
        └── Gate 4: {status, data} envelope ✓
        └── Gate 5: X-RateLimit-Remaining > 0 ✓
        └── Gate 6: No error, or actionable error message ✓

Step 7: Stage 4 - Write Artifacts
        └── booking-response.json (raw envelope)
        └── booking-summary.md (formatted confirmation)
        └── curl-command.sh (exact reproducible request)
        └── validation-report.json (all gates)
        └── audit-log.json (timing, retries, rate limit headers)
        └── debug-request.json (sanitized request)

Step 8: Print Summary
        └── "✅ Booking confirmed! UID: abc123"
        └── "📄 Summary: cal-booking-output/create-booking_acme_20260715_143510/booking-summary.md"
        └── "🔧 Debug: cal-booking-output/create-booking_acme_20260715_143510/curl-command.sh"
        └── "📊 Validation: ALL 6 GATES PASSED"
```

---

## Rate Limiting Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                           RATE LIMIT TOKEN BUCKET (Client-Side)                     │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     │
│  │   Request   │────▶│  Token      │────▶│  If Empty:  │────▶│  Sleep &    │     │
│  │   Queued    │     │  Bucket     │     │  Wait       │     │  Retry      │     │
│  └─────────────┘     │  (120/min)  │     │  (backoff)  │     └─────────────┘     │
│                      └──────┬──────┘     └─────────────┘           │             │
│                             │                                       │             │
│                             ▼                                       ▼             │
│                    ┌─────────────┐                         ┌─────────────┐       │
│                    │  Refill:    │                         │  On 429:    │       │
│                    │  2 tokens/s │                         │  Parse      │       │
│                    └─────────────┘                         │  Retry-After│       │
│                                                           │  Sleep      │       │
│                                                           └─────────────┘       │
│                                                                                     │
│  Headers Tracked: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset     │
│  Bucket Refill: Dynamic based on X-RateLimit-Reset timestamp                      │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow Support

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              AUTH METHOD SELECTION                                   │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                 │
│  │   API KEY       │    │     OAUTH       │    │   PLATFORM      │                 │
│  │  (Recommended)  │    │ (User-facing)   │    │ (Deprecated)    │                 │
│  ├─────────────────┤    ├─────────────────┤    ├─────────────────┤                 │
│  │ cal_ / cal_live_│    │ OAuth2 flow     │    │ x-cal-client-id │                 │
│  │ Bearer token    │    │ PKCE support    │    │ x-cal-secret-key│                 │
│  │ Server-to-server│    │ Scopes: BOOKING_│    │ Managed users   │                 │
│  │ No user consent │    │   READ/WRITE,   │    │ 60min tokens    │                 │
│  │ Instant setup   │    │   EVENT_TYPE_*  │    │ 1yr refresh     │                 │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘                 │
│           │                      │                      │                          │
│           └──────────────────────┼──────────────────────┘                          │
│                                  ▼                                                 │
│                    ┌─────────────────────────┐                                    │
│                    │   Unified Auth Header   │                                    │
│                    │   Authorization: Bearer │                                    │
│                    │   <token>               │                                    │
│                    └─────────────────────────┘                                    │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Error Handling & Retry Policy

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                           RETRY & ERROR CLASSIFICATION                               │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  RETRYABLE (exponential backoff, max 3 attempts):                                  │
│  ─────────────────────────────────────────                                         │
│  • 429 Too Many Requests → Wait Retry-After header (or 60s)                       │
│  • 500, 502, 503, 504 → 1s, 2s, 4s backoff                                        │
│  • Network timeout → 2s, 4s, 8s backoff                                            │
│                                                                                     │
│  NON-RETRYABLE (fail fast with actionable message):                                │
│  ─────────────────────────────────────────────                                     │
│  • 400 Bad Request → Validation error details in response.data                     │
│  • 401 Unauthorized → "Check API key / OAuth token expiry"                         │
│  • 403 Forbidden → "Scope missing: need BOOKING_WRITE / EVENT_TYPE_WRITE"         │
│  • 404 Not Found → "Event type / booking / webhook not found"                     │
│  • 409 Conflict → "Booking slot taken / duplicate webhook"                        │
│  • 422 Unprocessable → "Validation failed: see error details"                     │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Webhook Security & Verification

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                           WEBHOOK VERIFICATION FLOW                                  │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Cal.com → POST subscriberUrl                                                       │
│       │                                                                            │
│       ▼                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐             │
│  │  Headers:                                                        │             │
│  │  • cal-signature: sha256=<hmac>  (HMAC-SHA256 of body + secret) │             │
│  │  • cal-timestamp: <unix-epoch-seconds>                           │             │
│  │  • cal-webhook-id: <uuid>                                        │             │
│  └──────────────────────────────────────────────────────────────────┘             │
│       │                                                                            │
│       ▼                                                                            │
│  1. Verify timestamp within 5 min (replay protection)                             │
│  2. Compute HMAC-SHA256(body + "." + timestamp, webhook_secret)                   │
│  3. Constant-time compare with cal-signature                                      │
│  4. If valid → Process event (BOOKING_CREATED, BOOKING_CANCELLED, etc.)           │
│  5. Respond 2xx within 10s (else Cal.com retries with backoff)                    │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Maintenance & Versioning

| Component | Update Cadence | Source |
|-----------|----------------|--------|
| API Schemas | Per Cal.com release (check changelog) | `https://cal.com/docs/api-reference/v2` |
| Auth Patterns | Quarterly | Cal.com blog / developer changelog |
| Rate Limits | Monitor headers; adjust bucket on 429 | Response headers `X-RateLimit-*` |
| Webhook Triggers | Per release notes | Cal.com webhook docs |
| Error Codes | As discovered | Integration testing + support tickets |

**Schema Versioning:** All JSON schemas in `schemas/` include `"$schema": "https://json-schema.org/draft/2020-12/schema"` and `version` field. Increment on breaking API changes.