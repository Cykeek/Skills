# Cal.com API v2 — Authentication Patterns Reference

> **Source:** [Cal.com API Docs - Authentication](https://cal.com/docs/api-reference/authentication) | [API Reference v2](https://cal.com/docs/api-reference/v2)
> **Last Updated:** July 2025 | **API Version:** v2 (header: `cal-api-version: 2026-02-25`)

---

## Overview

Cal.com API v2 supports **three authentication methods**. All methods ultimately produce a **Bearer token** used in the `Authorization` header. Choose based on your integration type:

| Method | Best For | Token Prefix | Setup Complexity | User Consent |
|--------|----------|--------------|------------------|--------------|
| **API Key** | Server-to-server, internal tools | `cal_` (test) / `cal_live_` (prod) | Low (dashboard) | None |
| **OAuth 2.0** | User-facing apps, multi-tenant | OAuth access token | Medium (OAuth flow) | Required |
| **Platform** | Legacy enterprise (deprecated) | Managed user token | High (deprecated) | Managed users only |

> ⚠️ **Platform auth is deprecated** for new sign-ups (since Dec 15, 2025). Use OAuth or API Keys for new integrations.

---

## 1. API Key Authentication (Recommended for Server-to-Server)

### Generation
1. Go to **Settings → Security → API Keys** in Cal.com dashboard
2. Click **Generate New Key**
3. Choose **Test** (`cal_` prefix) or **Live** (`cal_live_` prefix)
4. Copy immediately — **shown only once**

### Usage
```bash
curl -X GET https://api.cal.com/v2/me \
  -H "Authorization: Bearer cal_live_abc123..." \
  -H "cal-api-version: 2026-02-25"
```

### Python
```python
from cal_booking_skill.api_client import CalClient

client = CalClient(api_key="cal_live_abc123...", api_version="2026-02-25")
# All requests automatically include Authorization + cal-api-version headers
```

### Security Notes
- Treat API keys like passwords — **never commit to git**
- Use **test keys** (`cal_`) for development/CI
- Rotate keys periodically via dashboard
- Keys inherit permissions of the generating user/team

---

## 2. OAuth 2.0 Authentication (Recommended for User-Facing Apps)

### Configuration
1. Go to **Settings → Developer → OAuth Clients**
2. Create new client → note `client_id` and `client_secret`
3. Configure **Redirect URI** (must match exactly)
4. Select **Scopes** (granular permissions):
   - `BOOKING_READ`, `BOOKING_WRITE`
   - `EVENT_TYPE_READ`, `EVENT_TYPE_WRITE`
   - `PROFILE_READ`, `PROFILE_WRITE`
   - `WEBHOOK_READ`, `WEBHOOK_WRITE`
   - `SCHEDULE_READ`, `SCHEDULE_WRITE`
   - Team/Org variants: `TEAM_BOOKING_READ`, `ORG_EVENT_TYPE_WRITE`, etc.

### Authorization Code Flow (Confidential Clients)
```bash
# Step 1: Redirect user to Cal.com
https://app.cal.com/auth/oauth2/authorize?
  client_id=YOUR_CLIENT_ID&
  redirect_uri=https://yourapp.com/callback&
  response_type=code&
  scope=BOOKING_READ+BOOKING_WRITE+EVENT_TYPE_READ&
  state=RANDOM_STRING

# Step 2: User authorizes → redirected to your callback with ?code=XYZ&state=...

# Step 3: Exchange code for tokens
curl -X POST https://api.cal.com/v2/auth/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=XYZ&redirect_uri=https://yourapp.com/callback&client_id=YOUR_CLIENT_ID&client_secret=YOUR_SECRET"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 1800,
  "refresh_token": "def50200...",
  "scope": "BOOKING_READ BOOKING_WRITE EVENT_TYPE_READ"
}
```

### PKCE Flow (Public Clients - SPAs, Mobile Apps)
```bash
# Generate code_verifier (43-128 chars, URL-safe)
code_verifier="dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"

# Derive code_challenge (SHA256, base64url)
code_challenge="E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"

# Step 1: Authorization request with PKCE
https://app.cal.com/auth/oauth2/authorize?
  client_id=YOUR_CLIENT_ID&
  redirect_uri=com.yourapp://callback&
  response_type=code&
  scope=BOOKING_READ+EVENT_TYPE_READ&
  code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&
  code_challenge_method=S256&
  state=RANDOM_STRING

# Step 3: Token exchange includes code_verifier
curl -X POST https://api.cal.com/v2/auth/oauth2/token \
  -d "grant_type=authorization_code&code=XYZ&redirect_uri=com.yourapp://callback&client_id=YOUR_CLIENT_ID&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
```

### Token Refresh
```bash
curl -X POST https://api.cal.com/v2/auth/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=def50200...&client_id=YOUR_CLIENT_ID&client_secret=YOUR_SECRET"
```
- Access tokens expire in **30 minutes**
- Refresh tokens expire in **1 year** (rotate on use)
- Store refresh tokens securely (encrypted at rest)

### Python OAuth Helper
```python
from cal_booking_skill.auth import OAuthClient

oauth = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="https://yourapp.com/callback",
    scopes=["BOOKING_READ", "BOOKING_WRITE", "EVENT_TYPE_READ"]
)

# Get authorization URL
auth_url = oauth.get_authorization_url(state="random_state")

# Exchange code for tokens
tokens = await oauth.exchange_code("authorization_code_from_callback")

# Refresh access token
new_tokens = await oauth.refresh_access_token(tokens.refresh_token)

# Use with CalClient
client = CalClient(access_token=tokens.access_token, api_version="2026-02-25")
```

---

## 3. Platform Authentication (Deprecated — Legacy Only)

> **Status:** No new sign-ups since Dec 15, 2025. Existing enterprise customers supported.

### Headers
```bash
curl -X GET https://api.cal.com/v2/me \
  -H "x-cal-client-id: YOUR_OAUTH_CLIENT_ID" \
  -H "x-cal-secret-key: YOUR_CLIENT_SECRET"
```

### Managed Users Flow
1. Create managed user via `POST /v2/managed-users`
2. Receive `access_token` (60 min) + `refresh_token` (1 year)
3. Use `access_token` as Bearer token for user-scoped operations
4. Refresh via `POST /v2/auth/oauth2/token` with `grant_type=refresh_token`

### Migration Path
| Platform Feature | OAuth/API Key Equivalent |
|-----------------|-------------------------|
| Managed users | OAuth with `offline_access` scope + user consent |
| `x-cal-client-id` | `client_id` in OAuth flow |
| Team-scoped access | Team-level OAuth scopes |

---

## Required Headers (All Methods)

| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | ✅ Yes | `Bearer <token>` (API key, OAuth access token, or managed user token) |
| `cal-api-version` | ✅ Most endpoints | Date string: `2026-02-25`, `2024-06-14`, `2024-06-11` |
| `Content-Type` | POST/PUT/PATCH | `application/json` |
| `x-cal-client-id` | Platform only | OAuth client ID |
| `x-cal-secret-key` | Platform only | Client secret |

### Version Header Strategy
- **Always include** `cal-api-version` — many endpoints **require** it
- Use **latest stable date** from [Cal.com API Changelog](https://cal.com/docs/api-reference/v2/changelog)
- Pin to specific version in production; test with latest in staging

---

## Permission Scopes Reference

| Scope | Description | Endpoints |
|-------|-------------|-----------|
| `BOOKING_READ` | Read bookings | `GET /bookings`, `GET /bookings/{id}` |
| `BOOKING_WRITE` | Create/update/cancel bookings | `POST /bookings`, `PATCH /bookings/{id}`, `DELETE /bookings/{id}` |
| `EVENT_TYPE_READ` | Read event types | `GET /event-types`, `GET /event-types/{id}` |
| `EVENT_TYPE_WRITE` | Create/update/delete event types | `POST /event-types`, `PATCH /event-types/{id}`, `DELETE /event-types/{id}` |
| `PROFILE_READ` | Read user profile | `GET /me` |
| `PROFILE_WRITE` | Update user profile | `PATCH /me` |
| `WEBHOOK_READ` | List webhooks | `GET /webhooks` |
| `WEBHOOK_WRITE` | Create/update/delete webhooks | `POST /webhooks`, `PATCH /webhooks/{id}`, `DELETE /webhooks/{id}` |
| `SCHEDULE_READ` | Read schedules | `GET /schedules` |
| `SCHEDULE_WRITE` | Create/update schedules | `POST /schedules`, `PATCH /schedules/{id}` |
| `TEAM_READ` | Read team info | `GET /teams/{id}` |
| `TEAM_WRITE` | Create teams | `POST /teams` |

### Team/Org Scopes (Prefix with `TEAM_` or `ORG_`)
- `TEAM_BOOKING_READ`, `TEAM_EVENT_TYPE_WRITE`, etc.
- `ORG_BOOKING_READ`, `ORG_EVENT_TYPE_WRITE`, etc.

---

## Common Authentication Errors

| HTTP | Error Code | Cause | Resolution |
|------|------------|-------|------------|
| 401 | `unauthorized` | Missing/invalid/expired token | Check `Authorization` header; refresh OAuth token |
| 401 | `invalid_api_key` | API key format wrong | Ensure prefix `cal_` or `cal_live_` |
| 403 | `insufficient_scope` | Token lacks required scope | Re-authorize with correct scopes |
| 403 | `team_access_denied` | Team/org scope mismatch | Use correct team/org prefixed scope |
| 429 | `rate_limit_exceeded` | Too many requests | Implement backoff; request limit increase |

---

## Best Practices Checklist

- [ ] **Use API keys** for server-to-server; **OAuth** for user-facing apps
- [ ] **Store secrets** in environment variables / secret manager (never in code)
- [ ] **Pin `cal-api-version`** in production; test latest in staging
- [ ] **Implement token refresh** for OAuth (auto-refresh on 401)
- [ ] **Request minimal scopes** — audit quarterly
- [ ] **Use test keys** (`cal_`) in CI/CD; live keys (`cal_live_`) only in prod
- [ ] **Monitor 401/403 rates** — indicates token expiry or scope issues
- [ ] **Migrate from Platform auth** if still using (deprecated Dec 2025)

---

## Quick Reference: Token Format Detection

```python
def detect_auth_type(token: str) -> str:
    """Identify authentication method from token format."""
    if token.startswith("cal_live_") or token.startswith("cal_"):
        return "api_key"
    elif token.startswith("eyJ"):  # JWT prefix
        return "oauth_or_managed"
    elif len(token) > 100:  # Opaque token
        return "oauth_or_managed"
    return "unknown"
```