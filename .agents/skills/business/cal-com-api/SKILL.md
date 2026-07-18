---
name: cal-com-api
description: Comprehensive guide for working with Cal.com API v2. Covers authentication (OAuth, API keys), endpoints, rate limits, error handling, and webhooks. Use when building scheduling integrations or managing bookings programmatically with Cal.com.
---

# Cal.com API v2 Knowledge Skill

This skill provides comprehensive knowledge about the Cal.com API v2 for building scheduling integrations and interacting with their scheduling platform programmatically.

## Short-Circuit

If the user only needs a quick API test, run the CLI verification script using exact credentials before writing complex integration code:
- Check test authentication: `python .agents/skills/business/cal-com-api/scripts/cli.py --api-key <cal_key> test`
- For quick endpoint inspection without custom scripts, refer directly to `references/endpoints-reference.md`.

## Anti-Patterns

1. **Hardcoding Live API Keys**: Never embed `cal_live_` keys directly inside application source code or version control.
2. **Ignoring Version Headers**: Omitting the `cal-api-version` header on endpoints that require date-stamped contract versions (`2024-06-14`, `2026-02-25`).
3. **Polling for Bookings**: Making continual REST requests to check for new bookings instead of subscribing to real-time events via `/v2/webhooks`.
4. **Unverified Webhook Processing**: Processing incoming webhook payloads without verifying the webhook signature header against the shared secret.
5. **Non-UTC Date Arithmetic**: Passing local timezone date strings into booking or schedule endpoints instead of absolute UTC ISO strings.

## API Overview

**Base URL**: `https://api.cal.com/v2`

**Versioning**: The API uses versioned endpoints (`/v2/`). Additionally, many endpoints require a `cal-api-version` header with a specific date (e.g., `2024-06-14`, `2024-06-11`, `2026-02-25`) to specify the contract version for that request.

## Authentication Methods

Cal.com API v2 supports three authentication methods:

### 1. OAuth (Recommended for integrations)
- **Setup**: Create OAuth clients via `https://app.cal.com/settings/developer/oauth`
- **Approval Process**: New clients start in "pending" state requiring admin approval
- **Key Scopes**:
  - `BOOKING_READ/WRITE` - Manage bookings
  - `EVENT_TYPE_READ/WRITE` - Control event types
  - `PROFILE_READ/WRITE` - Access user profiles
  - Team and Organization variants for scoped access
- **Authorization Flow**:
  1. Direct users to `https://app.cal.com/auth/oauth2/authorize` with `client_id`, `redirect_uri`, `state`, and `scope`
  2. Exchange codes for tokens at `POST https://api.cal.com/v2/auth/oauth2/token`
  3. Access tokens expire after 30 minutes; use refresh token to obtain new access token
- **Client Types**:
  - Confidential clients: Use `client_secret`
  - Public clients: Use PKCE with `code_verifier`

### 2. API Key (Quick setup, best for server-to-server)
- **Generation**: Create keys in **Settings > Security** in Cal.com dashboard
- **Key Formats**:
  - Test mode secret keys: prefix `cal_`
  - Live mode secret keys: prefix `cal_live_`
- **Usage**: Include as Bearer token: `Authorization: Bearer YOUR_API_KEY`
- **Requirements**: All calls must use HTTPS; unauthenticated requests are rejected

### 3. Platform (Deprecated)
- **Status**: Legacy method for platform customers (no new sign-ups as of December 15, 2025)
- **Headers**:
  - `x-cal-client-id` - OAuth client ID
  - `x-cal-secret-key` - Client secret
- **Managed Users**: After creating a managed user, receive an access token (valid 60 min) and refresh token (valid 1 yr); use access token as Bearer token for schedules, event types, and certain booking queries

## Rate Limits

- **Standard Allocation**: 120 requests per minute
- **Scope**: Applies to unauthenticated requests and base API keys
- **Higher Limits**: Can be requested via support (up to ~200 req/min)
- **Shared Baseline**: OAuth and API key authentication share the same limit baseline

## Core Endpoints and Purposes

### Bookings (`/v2/bookings`)
- **Purpose**: Create, retrieve, update, cancel bookings
- **Creation Requirements**: UTC start time, Attendee information (`name`, `timeZone`)
- **Event Specification**: Specify event via `eventTypeId` OR `eventTypeSlug` + `username/teamSlug` (+`orgSlug` optional)
- **Special Features**: Instant bookings (`instant:true`), recurring bookings (`recurrenceCount`)
- **Required Headers**: `cal-api-version` (e.g., `2026-02-25`)

### Event Types (`/v2/event-types`)
- **Purpose**: Create, retrieve, update, delete event types
- **Creation Requirements**: `lengthInMinutes`, `title`, `slug`
- **Required Headers**: `cal-api-version` (e.g., `2024-06-14`) and `Authorization: Bearer <token>`
- **OAuth Scope**: Requires `EVENT_TYPE_WRITE`

### Users / Profile (`/v2/me`)
- **Purpose**: Get authenticated user's profile
- **Authentication**: `Authorization: Bearer <token>`
- **OAuth Scope**: Requires `PROFILE_READ`

### Schedules (`/v2/schedules`)
- **Purpose**: Create schedules for authenticated user to define availability
- **Required Parameters**: `name`, `timeZone`, `isDefault` (boolean)
- **Time Format**: 24-hour format (e.g., `"08:00, 15:00"`)
- **Required Headers**: `Authorization: Bearer <token>` and `cal-api-version` (e.g., `2024-06-11`)

### Webhooks (`/v2/webhooks`)
- **Purpose**: Create, retrieve, update, delete webhooks
- **Required Fields**: `subscriberUrl`, `triggers` (array of strings, e.g., `"BOOKING_CREATED"`), `active` (boolean)
- **Example Triggers**: `"BOOKING_CANCELLED"`, `"MEETING_STARTED"`

### Teams (`/v2/teams`)
- **Purpose**: Create teams for collaborative scheduling
- **Required**: `name` and authorization

## Request/Response Formats

- **Format**: JSON for both requests and responses
- **Headers**:
  - `Authorization`: Bearer token (`Bearer <token>`)
  - `cal-api-version`: Date string specifying API contract version
- **Response Structure**:
  - Top-level object with `status` (string) and `data` (object/array)
  - Example: `{ "status": "success", "data": { ... } }`

## Related Skills

| Skill | Description | Usage Trigger |
| :--- | :--- | :--- |
| `skills/engineering/wix-support` | Integrates developer platforms, webhooks, and backend architectures | Use when connecting Cal.com to Wix or custom webhook handlers |
| `skills/content/content-writer` | Generates professional email confirmations and calendar notifications | Use when crafting attendee notifications and booking prompts |
| `skills/design/designer-god` | Designs booking forms, scheduling flows, and UI widgets | Use when building custom front-end embeds for Cal.com |

## Reference Files

| File | Description | When to Read |
| :--- | :--- | :--- |
| `auth-patterns.md` | In-depth OAuth flows, API keys, and platform token management | When configuring complex authentication setups |
| `best-practices.md` | Production resiliency, retry strategies, and performance rules | Before deploying scheduling integrations to production |
| `endpoints-reference.md` | Full catalog of payloads, headers, methods, and response schemas | When building exact API requests for bookings or event types |
| `error-handling.md` | Error codes (400, 401, 429), validation structures, and diagnostics | When debugging failed requests or implementing error recovery |
| `rate-limits.md` | Rate limit thresholds, headers (`X-RateLimit-*`), and backoff patterns | When designing high-frequency scheduling scripts |
| `webhook-handling.md` | Signature verification, event payloads, and security verification | When setting up webhook receiver endpoints |

## Quality Loop

1. **Verify Authentication**: Execute `python scripts/cli.py --api-key <key> test` to ensure credentials and network connectivity are functional.
2. **Validate Request Structure**: Confirm payloads match requirements using schema validation (`python scripts/validation.py`).
3. **Inspect API Version**: Check that `cal-api-version` header dates match the targeted endpoints exactly.
4. **Verify Webhook Signatures**: If handling webhooks, execute `scripts/cli.py verify-webhook` against payload fixtures before deploying.
