# Cal.com API v2 — Endpoints Reference

> **Source:** [Cal.com API Reference v2](https://cal.com/docs/api-reference/v2) | [OpenAPI Spec](https://cal.com/docs/openapi.json)
> **Last Updated:** July 2025 | **Base URL:** `https://api.cal.com/v2`
> **Auth:** All endpoints require `Authorization: Bearer <token>` + `cal-api-version` header

---

## Response Envelope (All Endpoints)

```json
{
  "status": "success" | "error",
  "data": { ... } | [ ... ] | null
}
```

**Error Response:**
```json
{
  "status": "error",
  "data": {
    "message": "Human-readable error",
    "code": "ERROR_CODE",
    "details": { ... }
  }
}
```

---

## 1. Bookings (`/v2/bookings`)

### 1.1 Create Booking
**POST** `/bookings` | Scopes: `BOOKING_WRITE`

**Headers:** `cal-api-version: 2026-02-25` (required)

**Request Body:**
```json
{
  "start": "2026-07-20T14:00:00Z",
  "attendee": {
    "name": "John Doe",
    "email": "john@example.com",
    "timeZone": "America/Los_Angeles",
    "phoneNumber": "+15551234567",
    "language": "en",
    "metadata": {}
  },
  "eventTypeId": 123,
  "responses": {
    "name": "John Doe",
    "email": "john@example.com",
    "notes": "Looking forward to our call"
  },
  "metadata": {},
  "instant": false,
  "recurrenceCount": 1,
  "seatReference": "optional-seat-ref"
}
```

**Event Specification (choose ONE):**
- `eventTypeId`: numeric ID
- **OR** `eventTypeSlug` + `username` (+ optional `organizationSlug`)

**Response (201):**
```json
{
  "status": "success",
  "data": {
    "id": 456,
    "uid": "abc123xyz",
    "title": "30min Meeting with John Doe",
    "description": "Booking description",
    "startTime": "2026-07-20T14:00:00.000Z",
    "endTime": "2026-07-20T14:30:00.000Z",
    "status": "ACCEPTED",
    "attendees": [...],
    "eventTypeId": 123,
    "organizer": { "id": 1, "name": "Host Name", "email": "host@cal.com" },
    "location": "https://meet.google.com/abc-defg-hij",
    "metadata": {},
    "createdAt": "2026-07-15T10:00:00.000Z",
    "updatedAt": "2026-07-15T10:00:00.000Z"
  }
}
```

### 1.2 Get Booking
**GET** `/bookings/{id}` | Scopes: `BOOKING_READ`

**Response:** Same as create booking `data` object

### 1.3 Update Booking
**PATCH** `/bookings/{id}` | Scopes: `BOOKING_WRITE`

**Request Body:**
```json
{
  "startTime": "2026-07-20T15:00:00Z",
  "status": "CANCELLED",
  "responses": { "notes": "Rescheduled" },
  "metadata": {}
}
```

### 1.4 Cancel Booking
**DELETE** `/bookings/{id}` | Scopes: `BOOKING_WRITE`
- Sets status to `CANCELLED`
- Triggers `BOOKING_CANCELLED` webhook

### 1.5 List Bookings
**GET** `/bookings` | Scopes: `BOOKING_READ`

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `status` | string | `PENDING`, `ACCEPTED`, `CANCELLED`, `REJECTED` |
| `startTime` | ISO8601 | Filter bookings after this time |
| `endTime` | ISO8601 | Filter bookings before this time |
| `eventTypeId` | integer | Filter by event type |
| `attendeeEmail` | string | Filter by attendee email |
| `take` | integer | Page size (default 50, max 100) |
| `skip` | integer | Offset for pagination |

**Response:**
```json
{
  "status": "success",
  "data": [ {booking}, {booking}, ... ]
}
```

---

## 2. Event Types (`/v2/event-types`)

### 2.1 Create Event Type
**POST** `/event-types` | Scopes: `EVENT_TYPE_WRITE`

**Headers:** `cal-api-version: 2024-06-14` (required)

**Request Body:**
```json
{
  "title": "30 Minute Discovery Call",
  "slug": "discovery-call",
  "lengthInMinutes": 30,
  "description": "Initial discovery call",
  "hidden": false,
  "position": 0,
  "schedulingType": "ROUND_ROBIN",
  "eventName": null,
  "eventColor": null,
  "customInputs": [],
  "successRedirectUrl": "https://example.com/thanks",
  "disableGuests": false,
  "hideCalendarNotes": false,
  "requiresConfirmation": false,
  "recurringEvent": null,
  "price": 0,
  "currency": "USD",
  "seatsPerTimeSlot": 1,
  "seatDisplayName": "Seat",
  "bookingFields": {
    "name": { "required": true },
    "email": { "required": true },
    "phone": { "required": false },
    "notes": { "required": false }
  },
  "locations": [
    { "type": "googleMeet" },
    { "type": "zoom" },
    { "type": "teams" },
    { "type": "custom", "location": "Phone call" }
  ],
  "scheduleId": null,
  "periodType": "RANGE",
  "periodStartDate": "2026-01-01",
  "periodEndDate": "2026-12-31",
  "periodDays": 30,
  "periodCountCalendarDays": false,
  "slotInterval": null,
  "minimumBookingFields: [],
  "timezone": "America/Los_Angeles",
  "metadata": {}
}
```

**Key Fields:**
- `lengthInMinutes`: Required (5, 15, 30, 45, 60, 90, 120...)
- `slug`: Required, URL-friendly, unique per user/team
- `schedulingType`: `ROUND_ROBIN`, `COLLECTIVE`, `MANAGED`
- `recurringEvent`: For recurring event types (see schema)
- `locations`: Array of location objects

**Response (201):** Event type object with `id`, `teamId`, `ownerId`, `createdAt`, `updatedAt`

### 2.2 Get Event Type
**GET** `/event-types/{id}` | Scopes: `EVENT_TYPE_READ`

### 2.3 List Event Types
**GET** `/event-types` | Scopes: `EVENT_TYPE_READ`

**Query:**
- `username` / `teamSlug` / `organizationSlug` — filter by owner
- `activeOnly` — boolean

### 2.4 Update Event Type
**PATCH** `/event-types/{id}` | Scopes: `EVENT_TYPE_WRITE`

### 2.5 Delete Event Type
**DELETE** `/event-types/{id}` | Scopes: `EVENT_TYPE_WRITE`

---

## 3. Schedules (`/v2/schedules`)

### 3.1 Create Schedule
**POST** `/schedules` | Scopes: `SCHEDULE_WRITE`

**Headers:** `cal-api-version: 2024-06-11` (required)

**Request Body:**
```json
{
  "name": "Business Hours",
  "timeZone": "America/Los_Angeles",
  "isDefault": true,
  "availability": [
    { "days": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00" }
  ],
  "dateOverrides": [
    { "date": "2026-12-25", "availability": [] },  // Christmas - closed
    { "date": "2026-07-04", "availability": [{ "startTime": "10:00", "endTime": "14:00" }] }
  ]
}
```

**Availability Format:**
- `days`: Array of integers (0=Sunday ... 6=Saturday)
- `startTime`/`endTime`: 24-hour format "HH:mm"
- `dateOverrides`: Specific date exceptions

**Response (201):** Schedule object with `id`, `userId`, `createdAt`, `updatedAt`

### 3.2 List Schedules
**GET** `/schedules` | Scopes: `SCHEDULE_READ`

### 3.3 Get/Update/Delete Schedule
**GET/PATCH/DELETE** `/schedules/{id}` | Scopes: `SCHEDULE_READ/WRITE`

---

## 4. Webhooks (`/v2/webhooks`)

### 4.1 Create Webhook
**POST** `/webhooks` | Scopes: `WEBHOOK_WRITE`

**Headers:** `cal-api-version: 2024-06-14` (required)

**Request Body:**
```json
{
  "subscriberUrl": "https://yourapp.com/webhooks/cal",
  "active": true,
  "triggers": [
    "BOOKING_CREATED",
    "BOOKING_CANCELLED",
    "BOOKING_RESCHEDULED",
    "BOOKING_REJECTED",
    "MEETING_STARTED",
    "MEETING_ENDED"
  ],
  "secret": "your-webhook-secret-for-hmac",
  "payloadTemplate": null
}
```

**Available Triggers:**
| Trigger | Description |
|---------|-------------|
| `BOOKING_CREATED` | New booking confirmed |
| `BOOKING_CANCELLED` | Booking cancelled by attendee/host |
| `BOOKING_RESCHEDULED` | Booking time changed |
| `BOOKING_REJECTED` | Host rejected pending booking |
| `BOOKING_PAID` | Payment completed (if paid bookings) |
| `MEETING_STARTED` | Meeting start time reached |
| `MEETING_ENDED` | Meeting end time reached |
| `FORM_SUBMITTED` | Booking form submitted |

**Response (201):** Webhook object with `id`, `secret` (only shown once!), `signingSecret`

### 4.2 Verify Webhook Signature (Critical)

```python
import hmac
import hashlib

def verify_webhook(payload: bytes, timestamp: str, signature: str, secret: str) -> bool:
    """
    Cal.com sends:
    - cal-signature: sha256=<hmac>
    - cal-timestamp: unix epoch seconds
    """
    # 1. Check timestamp (replay protection - 5 min window)
    import time
    if abs(time.time() - int(timestamp)) > 300:
        return False
    
    # 2. Compute expected signature
    message = f"{payload.decode()}.{timestamp}".encode()
    expected = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    
    # 3. Constant-time compare
    return hmac.compare_digest(f"sha256={expected}", signature)
```

### 4.3 List/Get/Update/Delete Webhooks
**GET** `/webhooks` | **GET/PATCH/DELETE** `/webhooks/{id}` | Scopes: `WEBHOOK_READ/WRITE`

---

## 5. Users / Profile (`/v2/me`)

### 5.1 Get Current User Profile
**GET** `/me` | Scopes: `PROFILE_READ`

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "bio": "Software Engineer",
    "locale": "en",
    "timeZone": "America/Los_Angeles",
    "organization": {
      "id": 456,
      "isPlatform": false
    }
  }
}
```

---

## 6. Teams (`/v2/teams`)

### 6.1 Create Team
**POST** `/teams` | Scopes: `TEAM_WRITE`

**Request Body:**
```json
{
  "name": "Engineering Team",
  "slug": "engineering",
  "logo": "https://example.com/logo.png",
  "brandColor": "#0066FF",
  "darkBrandColor": "#0055DD",
  "timezone": "America/Los_Angeles",
  "metadata": {}
}
```

**Response (201):** Team object with `id`, `members`, `eventTypes`, `schedules`

### 6.2 Get Team
**GET** `/teams/{id}` | Scopes: `TEAM_READ`

---

## 7. Availability / Slots (Common Patterns)

### 7.1 Get Available Slots (via Event Type)
**GET** `/event-types/{id}/slots`

**Query:**
- `startTime` (ISO8601, required)
- `endTime` (ISO8601, required)
- `timeZone` (IANA, required)
- `username` / `teamSlug` / `organizationSlug` (if not owner)

### 7.2 Check Availability for Booking
**POST** `/bookings/availability` — See [Booking Availability](https://cal.com/docs/api-reference/v2/bookings/check-availability)

---

## 8. Rate Limits & Headers

### Standard Limits
| Tier | Requests/Minute | Burst |
|------|-----------------|-------|
| Default | 120 | ~20 |
| Elevated (support) | 200 | ~50 |

### Rate Limit Headers (on every response)
```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 115
X-RateLimit-Reset: 1721059200  # Unix timestamp
Retry-After: 60  # On 429 only
```

### Client-Side Bucket Algorithm
```python
# Refill rate: limit / 60 tokens per second
# On 429: sleep Retry-After, then retry
# On response: update bucket from X-RateLimit-Remaining
```

---

## 9. Error Codes Reference

| HTTP | Code | Message | Action |
|------|------|---------|--------|
| 400 | `validation_error` | Invalid request body | Check `data.details` for field errors |
| 401 | `unauthorized` | Missing/invalid token | Refresh token or regenerate API key |
| 403 | `insufficient_scope` | Scope missing | Re-auth with required scope |
| 403 | `team_access_denied` | No access to team/org | Check team membership |
| 404 | `not_found` | Resource doesn't exist | Verify ID/slug |
| 409 | `conflict` | Slot taken, duplicate | Retry with different time |
| 422 | `unprocessable_entity` | Business rule violation | Check `data.details` |
| 429 | `rate_limit_exceeded` | Too many requests | Wait `Retry-After`, backoff |
| 500 | `internal_error` | Server error | Retry with backoff, contact support |

---

## 10. Pagination Pattern

List endpoints use cursor-based pagination:
```json
{
  "status": "success",
  "data": [...],
  "meta": {
    "nextCursor": "eyJpZCI6MTIzfQ==",
    "hasMore": true
  }
}
```

**Next request:** `?cursor=eyJpZCI6MTIzfQ==`

---

## Quick Reference: Required Headers per Endpoint

| Endpoint | cal-api-version | Auth Scopes |
|----------|-----------------|-------------|
| `POST /bookings` | `2026-02-25` | `BOOKING_WRITE` |
| `GET /bookings` | `2026-02-25` | `BOOKING_READ` |
| `POST /event-types` | `2024-06-14` | `EVENT_TYPE_WRITE` |
| `GET /event-types` | `2024-06-14` | `EVENT_TYPE_READ` |
| `POST /schedules` | `2024-06-11` | `SCHEDULE_WRITE` |
| `POST /webhooks` | `2024-06-14` | `WEBHOOK_WRITE` |
| `GET /me` | `2024-06-14` | `PROFILE_READ` |
| `POST /teams` | `2024-06-14` | `TEAM_WRITE` |