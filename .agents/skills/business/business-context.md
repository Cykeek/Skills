---
name: business-context
description: Domain context for business skills - scheduling APIs, CRM integrations, payment processing, analytics, and business operations
---

# Business Domain Context

## Domain Overview
The **Business** domain covers skills for business operations integrations: scheduling platforms, CRM systems, payment processors, analytics, and workflow automation. Focus on API-first integrations with production-ready patterns.

## Core Capabilities

### 1. Scheduling & Calendar (Cal.com)
- **API v2**: REST endpoints for bookings, event types, schedules, webhooks
- **Authentication**: OAuth 2.0 PKCE, API keys (cal_/cal_live_), Platform (legacy)
- **Rate Limits**: 120 req/min default, up to 200 req/min on request
- **Webhooks**: Real-time events (BOOKING_CREATED, CANCELLED, RESCHEDULED, MEETING_STARTED)
- **Security**: HMAC signature verification, idempotency keys, UTC timestamps

### 2. CRM & Pipeline
- **Integrations**: HubSpot, Salesforce, Pipedrive via webhook/API
- **Data Sync**: Bidirectional contact/deal sync, custom field mapping
- **Automation**: Lead scoring, lifecycle triggers, pipeline automation

### 3. Payment & Billing
- **Providers**: Stripe, Paddle, Lemon Squeezy
- **Models**: One-time, subscription, usage-based, metered
- **Compliance**: PCI DSS, SCA, VAT/GST, revenue recognition

### 4. Analytics & Reporting
- **Event Tracking**: Custom events, funnel analysis, cohort retention
- **Dashboards**: Real-time, scheduled exports, embedded analytics
- **Attribution**: UTM, referrer, first/last touch, multi-touch models

## Skills in This Domain

| Skill | Description | Key Files |
|-------|-------------|-----------|
| `business/cal-com-api` | Cal.com API v2 integration with CLI and validation | `SKILL.md`, `scripts/cli.py`, `references/*.md` |

## Reference Standards
- **SKILL-AUTHORING-STANDARD.md**: All skills ≤500 lines, ≤10KB, kebab-case names
- **SKILL_PIPELINE.md**: 5-stage pipeline (PLAN → SCAFFOLD → AUTHOR → VALIDATE → PUBLISH)
- **Business-Specific**: OAuth 2.1, OpenAPI 3.1, webhook security (RFC 8470), PCI DSS for payments

## Integration Points
- **Engineering Domain**: Webhook handlers with `engineering/wix-support` diagnostic patterns
- **Content Domain**: Booking confirmations via `content/content-writer` email templates
- **Design Domain**: Embedded scheduling UI with `design/designer-god` component patterns
- **Productivity Domain**: Interview scheduling via `productivity/resume-doctor` career flows

## Domain Conventions
1. **Auth-First**: All API clients support multiple auth methods with clear precedence
2. **Validation Enabled**: Request/response schema validation on by default
3. **Webhook-Safe**: Signature verification mandatory; idempotency keys for all mutations
4. **UTC-Only**: All timestamps ISO 8601 UTC; no local timezone arithmetic
5. **Rate-Limit Aware**: Client-side token bucket; respect Retry-After headers
6. **Error Taxonomy**: Standardized error codes (auth, validation, rate-limit, not-found, conflict, server)

## Change Log
See `CHANGELOG.md` for domain-level changes and skill additions.