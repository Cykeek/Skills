---
name: engineering-context
description: Domain context for engineering skills - platform diagnostics, API integrations, DevOps, debugging tools, and developer productivity
---

# Engineering Domain Context

## Domain Overview
The **Engineering** domain covers skills for platform diagnostics, API integrations, DevOps workflows, debugging tools, and developer productivity. Focus on production-ready tooling with structured diagnostics and clear escalation paths.

## Core Capabilities

### 1. Platform Diagnostics (Wix)
- **Editor/Studio**: Layout debugging, responsive breakpoints, component hierarchy
- **Velo/Backend**: Code analysis, runtime debugging, log aggregation, performance profiling
- **CMS/Dynamic Pages**: Collection permissions, dataset binding, router/page config
- **DNS/Domains**: Record validation, SSL/TLS, propagation checks, redirect chains
- **Editor Comparison**: Classic vs Studio feature parity, migration checklists

### 2. API Integration Patterns
- **Authentication**: OAuth 2.0, API keys, JWT, mTLS
- **Resilience**: Circuit breaker, retry with backoff, bulkhead, timeout budgets
- **Observability**: Structured logging, distributed tracing, metrics emission
- **Validation**: JSON Schema, OpenAPI contract testing, consumer-driven contracts

### 3. DevOps & Deployment
- **CI/CD**: Pipeline templates, environment promotion, rollback strategies
- **Infrastructure**: IaC (Terraform/Pulumi), config management, secrets rotation
- **Monitoring**: SLO/SLI definitions, alerting rules, runbook automation
- **Incident Response**: Severity classification, war room procedures, postmortem templates

### 4. Developer Productivity
- **CLI Tools**: stdlib-only, JSON output, --help, exit codes 0/1/2
- **Code Generation**: OpenAPI → client, GraphQL → types, DB → models
- **Local Dev**: Docker Compose, dev containers, mock servers, hot reload
- **Debugging**: REPL integration, time-travel debugging, profile-guided optimization

## Skills in This Domain

| Skill | Description | Key Files |
|-------|-------------|-----------|
| `engineering/wix-support` | Wix platform diagnostic toolkit with structured flows | `SKILL.md`, `scripts/cli.py`, `references/*.md` |

## Reference Standards
- **SKILL-AUTHORING-STANDARD.md**: All skills ≤500 lines, ≤10KB, kebab-case names
- **SKILL_PIPELINE.md**: 5-stage pipeline (PLAN → SCAFFOLD → AUTHOR → VALIDATE → PUBLISH)
- **Engineering-Specific**: RFC 7807 (Problem Details), OpenTelemetry, SemVer, Conventional Commits

## Integration Points
- **Business Domain**: Webhook handlers for `business/cal-com-api` scheduling events
- **Design Domain**: Design token sync with `design/designer-god` design systems
- **Content Domain**: Technical docs generation with `content/content-writer`
- **Productivity Domain**: Dev environment setup with `productivity/resume-doctor` onboarding

## Domain Conventions
1. **Diagnosis-First**: Every tool starts with structured diagnosis before prescribing fixes
2. **Structured Output**: All CLI tools emit JSON; human-readable formats via flags
3. **Escalation Paths**: Clear tiered support (self-serve → community → partner → vendor)
4. **Reproducible**: Deterministic commands; same input → same output; seedable randomness
5. **Observability Built-In**: Logs, metrics, traces emitted by default; sampling configurable
6. **Security Defaults**: Least privilege, secret scanning, dependency auditing in CI

## Change Log
See `CHANGELOG.md` for domain-level changes and skill additions.