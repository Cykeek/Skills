---
name: business-index
description: Index of all skills in the business domain
---

# Business Domain - Skill Index

## Skills

| Skill | Version | Status | Description | Last Updated |
|-------|---------|--------|-------------|--------------|
| `business/cal-com-api` | 1.0.0 | ✅ Active | Cal.com API v2 integration for scheduling and bookings | 2026-07-17 |

## Domain Statistics
- **Total Skills**: 1
- **Total Reference Files**: 6
- **Total CLI Tools**: 1
- **Lines of Skill Code**: ~141 (SKILL.md only)

## Quick Links
- [Domain Context](business-context.md)
- [Changelog](CHANGELOG.md)
- [Skill Authoring Standard](../SKILL-AUTHORING-STANDARD.md)
- [Skill Pipeline](../SKILL_PIPELINE.md)

## Skill Details

### business/cal-com-api
**Path**: `skills/business/cal-com-api/`

**Capabilities**:
- Cal.com API v2 comprehensive coverage
- 3 auth methods: API Key, OAuth 2.0 PKCE, Platform (deprecated)
- Rate limiting: 120 req/min (token bucket)
- Core endpoints: Bookings, Event Types, Schedules, Webhooks, Teams, Users
- Schema-first validation with JSON Schema
- Webhook signature verification (HMAC-SHA256)
- Idempotency key support

**Reference Files** (6):
- `auth-patterns.md`, `endpoints-reference.md`
- `error-handling.md`, `rate-limits.md`
- `webhook-handling.md`, `best-practices.md`

**CLI**: `scripts/cal_booking_skill/cli.py`
- 20+ commands: bookings, event-types, schedules, availability, webhooks, teams, utils
- Auth: `--api-key`, `--oauth-token`, `--auth-method`, `--base-url`, `--rate-limit`
- Output: `--output json|yaml|table|text`, `--no-validate`
- Commands: `test-auth`, `create-booking`, `list-bookings`, `get-booking`, `cancel-booking`, `reschedule-booking`, `create-event-type`, `list-event-types`, `get-event-type`, `update-event-type`, `delete-event-type`, `create-schedule`, `list-schedules`, `get-schedule`, `update-schedule`, `delete-schedule`, `check-availability`, `setup-webhook`, `list-webhooks`, `get-webhook`, `update-webhook`, `delete-webhook`, `verify-webhook`
- Exit codes: 0 (success), 1 (error), 2 (auth required), 3 (validation failed), 4 (rate limited)

**Validation**: `python -m cal_booking_skill.cli --help` ✅ (now works without auth)

## Related Skills (Cross-Domain)
- `engineering/wix-support` - Webhook integration, backend architecture
- `content/content-writer` - Email confirmations, calendar notifications
- `design/designer-god` - Booking forms, scheduling flows, UI widgets
- `productivity/resume-doctor` - Interview scheduling, calendar coordination