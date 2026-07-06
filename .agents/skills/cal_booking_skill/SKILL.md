---
name: cal-com-api
description: Comprehensive skill for interacting with Cal.com API v2. Provides knowledge about authentication methods, endpoints, request/response formats, rate limits, error handling, and best practices for building scheduling integrations. Use when you need to understand how to interact with Cal.com's scheduling API or build integrations with their platform.
---

# Cal.com API v2 Knowledge Skill

This skill provides comprehensive knowledge about the Cal.com API v2 for building scheduling integrations and interacting with their scheduling platform programmatically.

## API Overview

**Base URL**: `https://api.cal.com/v2` (inferred from documentation)

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
  - `x-cal-client-id` – OAuth client ID
  - `x-cal-secret-key` – Client secret
- **Managed Users**: After creating a managed user, receive an access token (valid 60 min) and refresh token (valid 1 yr); use access token as Bearer token for schedules, event types, and certain booking queries

## Rate Limits

- **Standard Allocation**: 120 requests per minute
- **Scope**: Applies to unauthenticated requests and base API keys
- **Higher Limits**: Can be requested via support (up to ~200 req/min)
- **Shared Baseline**: OAuth and API key authentication share the same limit baseline

## Core Endpoints and Purposes

### Bookings (`/v2/bookings`)
- **Purpose**: Create, retrieve, update, cancel bookings
- **Creation Requirements**:
  - UTC start time
  - Attendee information (name, timeZone)
- **Event Specification**:
  - Specify event via `eventTypeId` OR `eventTypeSlug` + `username/teamSlug` (+`orgSlug` optional)
- **Special Features**:
  - Instant bookings (team): Set `instant:true`
  - Recurring bookings: Add `recurrenceCount`
- **Required Headers**: `cal-api-version` (e.g., `2026-02-25`)
- **Optional**: `attendee.phoneNumber` for SMS notifications (if enabled)

### Event Types (`/v2/event-types`)
- **Purpose**: Create, retrieve, update, delete event types
- **Creation Requirements**:
  - `lengthInMinutes` (number)
  - `title` (string)
  - `slug` (string)
- **Required Headers**: `cal-api-version` (e.g., `2024-06-14`) and `Authorization: Bearer <token>`
- **OAuth Scope**: Requires `EVENT_TYPE_WRITE`
- **Optional Settings**:
  - Scheduling rules (buffers, notice periods)
  - Custom booking forms
  - Location options
  - Limitations
  - Recurrence rules
  - Seat limits
  - Private notes
- **Response**: Includes `status` and `data` with created event type details

### Users / Profile (`/v2/me`)
- **Purpose**: Get authenticated user's profile
- **Authentication**: `Authorization: Bearer <token>` (API key, OAuth access token, or managed user token)
- **OAuth Scope**: Requires `PROFILE_READ`
- **Response**: Returns `status` and `data` (`MeOutput`) containing:
  - `id`, `username`, `email`, `name`, `bio`, `locale`, `timeZone`
  - `organization` object (`id`, `isPlatform` boolean)

### Schedules (`/v2/schedules`)
- **Purpose**: Create schedules for authenticated user to define availability
- **Required Parameters**:
  - `name`
  - `timeZone`
  - `isDefault` (boolean)
- **Optional**: Availability windows, date-specific overrides
- **Time Format**: 24-hour format (e.g., `"08:00, 15:00"`)
- **Required Headers**: `Authorization: Bearer <token>` and `cal-api-version` (e.g., `2024-06-11`)
- **Usage**: Defines when event types are available (default schedule or specialized schedules)

### Webhooks (`/v2/webhooks`)
- **Purpose**: Create, retrieve, update, delete webhooks
- **Required Fields**:
  - `subscriberUrl`
  - `triggers` (array of strings, e.g., `"BOOKING_CREATED"`)
  - `active` (boolean)
- **OAuth Scope**: Requires `WEBHOOK_WRITE` if applicable
- **Example Triggers**:
  - `"BOOKING_CANCELLED"`
  - `"MEETING_STARTED"`
- **Response**: Returns `status` and `data` with webhook details

### Teams (`/v2/teams`)
- **Purpose**: Create teams for collaborative scheduling
- **Required**: `name` and authorization
- **Optional**: `slug` (auto-generated if omitted)
- **Response**: Returns team details

## Availability by Customer Type

- **Teams**: Access to most endpoints except those prefixed with "Platform"
- **Organizations**: Access to all except "Platform", "Teams", and child-organization routes
- **Platform** (Deprecated): Access to endpoints starting with "Platform" plus unprefixed ones (Bookings, Event Types); ESSENTIALS plan also gets most "Orgs" routes except some attribute-related endpoints

## Request/Response Formats

- **Format**: JSON for both requests and responses
- **Headers**:
  - `Authorization`: Bearer token (API key, OAuth access token, or managed user token)
  - `cal-api-version`: Date string specifying API contract version (required on many endpoints)
  - For Platform auth: `x-cal-client-id` and `x-cal-secret-key` headers
- **Response Structure**:
  - Top-level object with `status` (string) and `data` (object/array)
  - Example: `{ "status": "success", "data": { ... } }`
  - Error responses follow similar structure with error details in `data` or separate error fields

## Error Handling Patterns

- **HTTP Status Codes**: Indicate success or failure (specific codes not detailed in fetched pages)
- **Error Response Structure**:
  - `status`: "error" or similar indicator
  - `data`: Contains error message, error code, or validation details
- **Common Error Types**:
  - Authentication errors: 401 Unauthorized for missing/invalid tokens
  - Rate limit errors: 429 Too Many Requests
  - Validation errors: 400 Bad Request with details about invalid fields

## Specific Conventions and Patterns

1. **Versioning Header**: Many endpoints require `cal-api-version` header with a specific date for contract stability
2. **Identifier Flexibility**: Events can be specified by ID (`eventTypeId`) OR by slug combination (`eventTypeSlug` + `username/teamSlug`)
3. **UTC Times**: All times in API requests/responses are expected in UTC format
4. **Bearer Token Uniformity**: Whether using API key, OAuth access token, or managed user token, Authorization header format is consistent: `Bearer <token>`
5. **Scoped OAuth**: Permissions are granular; integrations only request necessary scopes
6. **Managed Users**: Platform-like functionality via temporary access tokens (60 min) and refresh tokens (1 yr) for acting on behalf of users
7. **Team/Organization Hierarchy**: Endpoint access depends on customer's plan type (Team, Organization, Platform) with specific prefix restrictions
8. **Webhook Triggers**: Use string constants for events (e.g., `"BOOKING_CREATED"`) to subscribe to specific occurrences
9. **Schedule Flexibility**: Schedules define recurring weekly availability with optional date-specific overrides for exceptions
10. **Instant Booking**: For team event types, setting `instant:true` creates a booking immediately without attendee selection timeout

## Additional Notes

- **Platform Deprecation**: The Platform offering is deprecated for new sign-ups as of December 15, 2025; existing enterprise support continues
- **API Key Security**: API keys carry significant privileges and should be treated like passwords
- **Transport Security**: HTTPS is mandatory for all API calls
- **Use Cases**: Designed for building scheduling integrations, managing event types, and automating booking workflows

## Best Practices for Using This Skill

1. **Authentication Choice**: Use OAuth for user-facing integrations, API keys for server-to-server communication
2. **Version Management**: Always include the appropriate `cal-api-version` header for endpoints that require it
3. **Error Handling**: Implement robust error handling for 401, 429, and 400 responses
4. **Rate Limiting**: Implement retry logic with exponential backoff for 429 responses
5. **Scope Management**: Request only the OAuth scopes your integration actually needs
6. **Time Handling**: Always work with UTC times when interacting with the API
7. **Testing**: Use test mode API keys (`cal_` prefix) for development and testing
8. **Webhook Security**: Validate webhook signatures and implement retry logic for failed deliveries
9. **Pagination**: Be aware that list endpoints may be paginated (check API reference for specific endpoints)
10. **Error Details**: Always check the `data` field in error responses for specific validation or error information

## Implementation Examples (Conceptual)

When using this skill to implement Cal.com integrations:

1. **Authentication Setup**:
   - For server-to-server: Generate API key in dashboard, use as Bearer token
   - For user-facing apps: Implement OAuth flow with appropriate scopes

2. **Making Requests**:
   - Set `Authorization: Bearer <your_token>` header
   - Include `cal-api-version: YYYY-MM-DD` header when required
   - Set `Content-Type: application/json` for POST/PUT requests
   - Parse JSON responses, checking `status` field first

3. **Common Operations**:
   - **Check Availability**: Use schedules and event types to determine availability
   - **Create Booking**: Provide attendee info, event specification, and UTC start time
   - **Manage Event Types**: Create/update event types with scheduling rules and custom fields
   - **Handle Events**: Set up webhooks for booking.created, booking.cancelled, etc.

4. **Error Handling**:
   - Check HTTP status codes first
   - Parse error details from response body
   - Implement specific handling for auth (401), rate limit (429), and validation (400) errors
   - Refresh tokens when receiving 401 with expired OAuth tokens

This skill provides the foundational knowledge needed to effectively work with the Cal.com API v2 for building scheduling applications and integrations.