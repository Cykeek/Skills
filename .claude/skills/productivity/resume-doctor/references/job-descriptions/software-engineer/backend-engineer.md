---
role_id: "software-engineer/backend-engineer"
canonical_title: "Backend Software Engineer"
aliases: ["Backend Engineer", "Server-Side Engineer", "API Engineer", "Platform Engineer"]
seniority_levels: ["Junior", "Mid", "Senior", "Staff", "Principal"]
related_roles: ["fullstack-engineer", "software-engineer", "platform-engineer", "data-engineer"]
ats_keywords:
  - "Node.js"
  - "Go"
  - "Python"
  - "PostgreSQL"
  - "Redis"
  - "Kafka"
  - "gRPC"
  - "REST API"
  - "GraphQL"
  - "Microservices"
  - "Docker"
  - "Kubernetes"
  - "AWS"
  - "GCP"
  - "Terraform"
  - "CI/CD"
  - "System Design"
  - "Distributed Systems"
  - "Database Design"
  - "Caching"
  - "Observability"
  - "Testing"
  - "Mentoring"
  - "Code Review"
ats_skills_taxonomy:
  languages_frameworks:
    - "Go 1.22+ (Standard Library, Chi, Gin, gRPC, Connect, Temporal)"
    - "Node.js 20+ (Fastify, Hono, Express, tRPC, NestJS)"
    - "Python 3.11+ (FastAPI, Litestar, Django, SQLAlchemy)"
    - "Rust (Axum, Actix, Tonic) — emerging"
    - "Java 21+ (Spring Boot, Quarkus, Vert.x) — enterprise"
  databases:
    - "PostgreSQL 15+ (Indexing, Partitioning, Read Replicas, Advisory Locks, JSONB, Citus)"
    - "Redis 7+ (Cluster, Streams, Pub/Sub, Lua Scripting, Rate Limiting)"
    - "MongoDB (Sharding, Aggregation, Change Streams)"
    - "Cassandra/ScyllaDB (Wide rows, TTL, LWT)"
    - "ClickHouse / Apache Druid (OLAP, Time-series)"
    - "Elasticsearch / OpenSearch (Full-text, Logs, Observability)"
  messaging:
    - "Apache Kafka / Redpanda (Topics, Partitions, Consumer Groups, Exactly-Once, Schema Registry)"
    - "NATS / NATS JetStream (Pub/Sub, KV, Object Store, Distributed Systems)"
    - "RabbitMQ (AMQP, Quorum Queues, Dead Letter Exchanges)"
    - "AWS SQS/SNS/EventBridge (Serverless, FIFO, DLQ)"
    - "gRPC / Connect / tRPC (Contract-first, Protobuf, Codegen)"
    - "GraphQL (Apollo, GraphQL Yoga, Pothos, Federation)"
  api_design:
    - "REST (OpenAPI 3.1, JSON Schema, Hypermedia, Versioning, Problem Details RFC 9457)"
    - "GraphQL (Schema Stitching, Federation, Dataloader, Persisted Queries)"
    - "gRPC (Protobuf, Unary/Streaming, Interceptors, Reflection)"
    - "tRPC (End-to-end types, React Query integration, Adapters)"
    - "AsyncAPI (Event-driven contracts, Message schemas)"
  infrastructure:
    - "AWS (ECS/Fargate, Lambda, RDS, ElastiCache, MSK, SQS, S3, IAM, CloudFront, Route53)"
    - "GCP (Cloud Run, Cloud SQL, Memorystore, Pub/Sub, GKE, Artifact Registry)"
    - "Azure (Container Apps, AKS, Cosmos DB, Service Bus, Key Vault)"
    - "Docker (Multi-stage, BuildKit, Distroless, SBOM, Cosign)"
    - "Kubernetes (EKS/GKE/AKS, Helm, Kustomize, Operators, CRDs, Gateway API)"
    - "Terraform / OpenTofu / Pulumi / AWS CDK (IaC, Modules, State, Drift Detection)"
    - "Service Mesh: Istio, Linkerd, Cilium (mTLS, Traffic Split, Observability)"
    - "GitOps: ArgoCD, Flux (Image Automation, Progressive Delivery)"
  observability:
    - "OpenTelemetry (Auto-instrumentation, Custom Spans, Metrics, Logs)"
    - "Prometheus / Grafana / Mimir / Thanos (Metrics, Alerting, Recording Rules)"
    - "Tempo / Jaeger / Zipkin (Distributed Tracing, TraceQL)"
    - "Loki / Elasticsearch / OpenSearch (Structured Logging, LogQL)"
    - "Sentry / Datadog / Honeycomb (Error Tracking, APM, SLOs)"
    - "PagerDuty / Opsgenie / Alertmanager (On-call, Escalation, Runbooks)"
  architecture_patterns:
    - "Microservices: DDD, Bounded Contexts, Event Sourcing, CQRS, Saga/Choreography"
    - "Modular Monolith: Clean Architecture, Vertical Slice, Feature Modules"
    - "Event-Driven: Event Carried State Transfer, Event Notification, Event Sourcing"
    - "API Gateway: Kong, Envoy, AWS API Gateway, GraphQL Federation"
    - "Caching: Write-Through, Read-Through, Write-Behind, Cache-Aside, Invalidation"
    - "Database: Expand/Contract Migrations, Dual-Write, CDC (Debezium), Sharding"
    - "Resilience: Circuit Breaker (Resilience4j, Hystrix), Bulkhead, Retry, Timeout"
  security:
    - "OAuth 2.0 / OIDC / JWT / mTLS / SPIFFE"
    - "RBAC / ABAC / ReBAC (Casbin, OPA, Google Zanzibar)"
    - "OWASP Top 10, API Security Top 10"
    - "SAST/DAST/SCA: Semgrep, Snyk, Trivy, Syft, Cosign, SBOM"
    - "Secrets: Vault, AWS Secrets Manager, 1Password, SOPS, SealedSecrets"
  practices:
    - "TDD, Property-Based Testing (fast-check, hypothesis), Contract Testing (Pact)"
    - "Code Review: Conventional Comments, Stacked PRs, Review Rotation"
    - "Trunk-Based Development, Feature Flags, Progressive Delivery"
    - "Incident Response: On-Call, Runbooks, Blameless Postmortems, Chaos Engineering"
    - "Documentation: ADRs (MADR), Runbooks, API Docs (OpenAPI), C4 Diagrams"
    - "Mentoring: Pair Programming, Code Review Coaching, Career Development"
seniority_signals:
  junior:
    - "Implements API endpoints with guidance"
    - "Writes unit and integration tests (>80% coverage)"
    - "Participates in code reviews; learns patterns"
    - "Debugs production issues with senior support"
    - "Contributes to runbooks and API documentation"
    - "Learns database modeling and query optimization"
  mid:
    - "Owns services end-to-end: design → deploy → operate"
    - "Designs database schemas, API contracts, event schemas"
    - "Implements observability (metrics, logs, traces, SLOs)"
    - "Drives technical decisions for team scope"
    - "Mentors junior engineers; improves developer experience"
    - "Optimizes query performance; designs caching strategies"
    - "Handles on-call rotation; reduces MTTR"
  senior:
    - "Architects multi-service systems; defines service boundaries"
    - "Leads cross-team initiatives: migrations, platform adoption, standardization"
    - "Defines technical standards: patterns, testing, security, observability"
    - "Drives incident command; establishes postmortem culture"
    - "Mentors mid/senior engineers; grows Staff engineers"
    - "Balances tech debt vs velocity; quantifies trade-offs"
    - "Partners with PM on roadmap; influences product strategy"
    - "Evaluates new technologies; runs RFC process"
  staff:
    - "Defines multi-year platform/infrastructure strategy"
    - "Architects shared platforms: data, auth, messaging, developer platform"
    - "Sets org-wide engineering standards; chairs architecture review board"
    - "Leads high-stakes migrations (monolith → services, cloud, database)"
    - "Grows Staff+ cohort; defines career ladders and hiring bar"
    - "Influences executive decisions; represents engineering to board/investors"
    - "Industry thought leadership: speaking, writing, open source"
  principal:
    - "Company-wide technical vision and strategy"
    - "Multi-year technology roadmap aligned with business"
    - "Industry recognition: keynotes, patents, standards bodies, OSS leadership"
    - "M&A technical due diligence; crisis leadership"
    - "Builds engineering culture at scale (1000+ engineers)"
ats_weight_hints:
  must_have:
    - "Go"
    - "Node.js"
    - "Python"
    - "PostgreSQL"
    - "Redis"
    - "Kafka"
    - "gRPC"
    - "REST API"
    - "Docker"
    - "Kubernetes"
    - "AWS"
    - "System Design"
    - "Microservices"
    - "Testing"
    - "CI/CD"
  strong_signal:
    - "GraphQL"
    - "Terraform"
    - "OpenTelemetry"
    - "Prometheus"
    - "Grafana"
    - "Temporal"
    - "Event Sourcing"
    - "CQRS"
    - "DDD"
    - "Mentoring"
    - "Architecture Review"
    - "Cost Optimization"
  nice_to_have:
    - "Rust"
    - "Java"
    - "ClickHouse"
    - "Istio"
    - "ArgoCD"
    - "OPA"
    - "Chaos Engineering"
    - "FinOps"
    - "WebAssembly"
ats_parser_hints:
  greenhouse:
    - "go"
    - "node.js"
    - "python"
    - "postgresql"
    - "redis"
    - "kafka"
    - "grpc"
    - "rest api"
    - "docker"
    - "kubernetes"
    - "aws"
    - "system design"
    - "microservices"
  lever:
    - "go"
    - "node"
    - "python"
    - "postgresql"
    - "redis"
    - "kafka"
    - "grpc"
    - "rest"
    - "docker"
    - "kubernetes"
    - "aws"
    - "system design"
  workday:
    - "Go"
    - "Node.js"
    - "Python"
    - "PostgreSQL"
    - "Redis"
    - "Apache Kafka"
    - "gRPC"
    - "RESTful APIs"
    - "Docker"
    - "Kubernetes"
    - "Amazon Web Services"
    - "System Design"
    - "Microservices"
  icims:
    skill_clusters:
      languages: ["Go", "Node.js", "Python", "Java", "Rust"]
      databases: ["PostgreSQL", "Redis", "MongoDB", "Cassandra", "MySQL"]
      messaging: ["Kafka", "RabbitMQ", "NATS", "gRPC", "GraphQL", "AWS SQS"]
      cloud: ["AWS", "ECS", "Lambda", "RDS", "EKS", "CloudFormation", "Terraform"]
      devops: ["Docker", "Kubernetes", "CI/CD", "GitHub Actions", "Prometheus", "Grafana"]
      architecture: ["System Design", "Microservices", "Event-Driven", "DDD", "CQRS", "API Design"]
---
## Role Summary

> **Backend Software Engineer** — Builds, operates, and evolves server-side systems: APIs, data layers, messaging, and infrastructure. Focuses on reliability, scalability, latency, and developer experience. At Senior+ owns significant subsystems; at Staff+ defines platform strategy.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### API & Service Development (All Levels)
- Design and implement **REST APIs** (OpenAPI 3.1, Problem Details RFC 9457), **GraphQL** (Federation, Dataloader, Persisted Queries), **gRPC** (Protobuf, Streaming, Interceptors), **tRPC** (End-to-end types)
- Build **event-driven services** with **Kafka**, **NATS**, **RabbitMQ**, **AWS EventBridge** — exactly-once semantics, schema registry (Confluent, Apicurio)
- Implement **authentication/authorization**: **OAuth 2.0**, **OIDC**, **JWT**, **mTLS**, **RBAC/ABAC/ReBAC** (Casbin, OPA, Zanzibar)
- Develop **background job processors**: **Temporal**, **BullMQ**, **Celery**, **AWS Lambda** (async, retries, dead-letter, idempotency)

### Data & Storage (All Levels)
- Design **PostgreSQL** schemas: **normalization**, **indexing** (B-tree, GIN, GiST, BRIN), **partitioning** (range, list, hash), **read replicas**, **connection pooling** (PgBouncer)
- Implement **Redis** patterns: **caching** (read-through, write-through, write-behind), **sessions**, **rate limiting** (token bucket, sliding window), **distributed locks**, **streams**
- Execute **zero-downtime migrations**: expand/contract, backfill, dual-write, CDC (Debezium)
- Optimize **query performance**: `EXPLAIN ANALYZE`, statistics, correlated subqueries → joins, materialized views

### Infrastructure & Operations (Senior+)
- Provision **cloud infrastructure** (AWS/GCP/Azure) via **Terraform**/**Pulumi**/**CDK**: compute, networking, databases, DNS, certificates
- Containerize with **Docker** (multi-stage, distroless, SBOM); orchestrate with **Kubernetes** (Helm, Kustomize, Operators, Gateway API)
- Build **CI/CD pipelines** (GitHub Actions, GitLab CI): test, build, scan, sign, deploy, verify, rollback
- Establish **observability**: **OpenTelemetry** instrumentation, **Prometheus/Grafana** metrics, **Tempo/Jaeger** tracing, **Loki** logging, **SLO/SLI** dashboards, **alerting** (PromQL, Alertmanager, PagerDuty)
- Implement **GitOps** (ArgoCD/Flux): image automation, progressive delivery (canary, blue-green), drift detection

### System Design & Architecture (Senior+)
- Design **microservices architectures**: **DDD** (bounded contexts, aggregates, domain events), **Event Sourcing**, **CQRS**, **Saga** (choreography/orchestration)
- Conduct **architecture reviews**, write **ADRs** (MADR format), threat model (STRIDE)
- Define **service contracts**: API versioning, backward compatibility, deprecation policy
- Lead **capacity planning**, **cost optimization** (right-sizing, spot, savings plans, FinOps), **disaster recovery** (RPO/RTO, backup/restore, chaos engineering)

### Technical Leadership (Staff+)
- Define **technical strategy** and **multi-year roadmap** for platform/infrastructure
- Establish **engineering standards**: code style, architecture patterns, testing strategy, security baseline
- Lead **cross-team initiatives**: platform migrations, re-architecture, developer experience
- Mentor **Senior+ engineers**; grow **Staff+ engineers**; define **career ladders** and **hiring bar**
- Represent engineering in **executive reviews**, **board presentations**, **industry conferences**

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
**Languages**: Go, Node.js, Python (at least one at expert level)
**Databases**: PostgreSQL, Redis
**Messaging**: Kafka, gRPC, REST API
**Infrastructure**: Docker, Kubernetes, AWS (or GCP/Azure)
**Architecture**: System Design, Microservices, Distributed Systems
**Practices**: Testing (unit/integration/contract), CI/CD, Git, Code Review

### Strong Signal (Differentiators)
- GraphQL, Terraform, OpenTelemetry, Prometheus, Grafana, Temporal
- Event Sourcing, CQRS, DDD, API Gateway, Service Mesh
- Mentoring, Architecture Review, Cost Optimization, Incident Command
- Database Internals: WAL, MVCC, B-tree, LSM-tree, Query Planning

### Nice-to-Have (Specialization Signals)
- Rust, Java, ClickHouse, Istio, ArgoCD, OPA, Chaos Engineering, FinOps, WebAssembly
- eBPF (Cilium), WasmEdge, Spin, Fermyon (edge compute)

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Junior (0-2 yrs)
- **Implemented** REST endpoints in **Go/Node.js** with **80%+ test coverage**
- **Wrote** PostgreSQL queries with **proper indexing** reducing latency **40%**
- **Containerized** services with **Docker**; deployed to **AWS ECS**
- **Participated** in **code reviews**; contributed to **runbooks**

### Mid (2-5 yrs)
- **Designed** **GraphQL federation schema** serving **50M+ daily queries**
- **Architected** **event-driven order processing** with **Kafka** (exactly-once, 100K events/sec)
- **Implemented** **distributed tracing** with **OpenTelemetry/Jaeger** cutting **MTTR 60%**
- **Built** **CI/CD pipelines** enabling **50+ deploys/day** with **automated rollback**
- **Led** **zero-downtime PostgreSQL migration** (expand/contract, 2TB data)
- **Mentored** 2+ engineers; improved **onboarding** from 2 weeks → 3 days

### Senior (5-8 yrs)
- **Designed** **microservices platform** (DDD, Event Sourcing, CQRS) handling **1B+ events/day**
- **Drove** **cost optimization** reducing **cloud spend 30%** via right-sizing, spot, Savings Plans
- **Established** **observability strategy** org-wide (metrics, logs, traces, SLOs); cut incident resolution **50%**
- **Led** **monolith → services migration** (6 months, zero incidents, 20 services)
- **Defined** **technical standards**: architecture patterns, testing, security, observability
- **Partnered** with **PM** on **roadmap**; influenced **product strategy** via technical insight

### Staff (8-12 yrs)
- **Defined** **5-year platform strategy** enabling **10x scale**; aligned with **$100M+ ARR** target
- **Architected** **developer platform** (CI/CD, auth, observability, feature flags) serving **200+ engineers**
- **Led** **payments re-architecture** (PCI-DSS, 99.99% availability, **$50B+ volume**)
- **Grew** **Staff+ cohort** from 3→12; designed **career ladder**; raised **hiring bar**
- **Advised** **C-suite** on **technical investments**; presented to **board** on **tech risk**

### Principal (12+ yrs)
- **Set** **company-wide technical vision**; authored **multi-year technology roadmap**
- **Industry recognition**: keynotes, patents, standards bodies (CNCF, W3C), OSS leadership
- **M&A technical due diligence** for **$1B+ acquisitions**
- **Crisis leadership**: incident command, organizational transformation
- **Built** **engineering culture** at scale (**1000+ engineers**)

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `go`, `node.js`, `python`, `postgresql`, `redis`, `kafka`, `grpc`, `rest api`, `docker`, `kubernetes`, `aws`, `system design`, `microservices`
**Stemming**: `design`→`designed`/`designing`, `implement`→`implemented`, `lead`→`led`/`leading`
**Fuzzy**: `kubernetes`≈`k8s`, `postgresql`≈`postgres`, `typescript`≈`ts`

### Lever
**Exact**: `go`, `node`, `python`, `postgresql`, `redis`, `kafka`, `grpc`, `rest`, `docker`, `kubernetes`, `aws`, `system design`
**Normalization**: `nextjs`→`next.js`, `tailwindcss`→`tailwind css`, `github actions`→`github-actions`

### Workday
**Exact (title case)**: `Go`, `Node.js`, `Python`, `PostgreSQL`, `Redis`, `Apache Kafka`, `gRPC`, `RESTful APIs`, `Docker`, `Kubernetes`, `Amazon Web Services`, `System Design`, `Microservices`
**Compound**: `AWS Lambda`, `Amazon RDS`, `AWS ECS`, `AWS EKS`, `Google Cloud Run`, `Azure AKS`

### iCIMS
**Skill clusters**:
```
languages: ["Go", "Node.js", "Python", "Java", "Rust"]
databases: ["PostgreSQL", "Redis", "MongoDB", "Cassandra", "MySQL"]
messaging: ["Kafka", "RabbitMQ", "NATS", "gRPC", "GraphQL", "AWS SQS"]
cloud: ["AWS", "ECS", "Lambda", "RDS", "EKS", "CloudFormation", "Terraform"]
devops: ["Docker", "Kubernetes", "CI/CD", "GitHub Actions", "Prometheus", "Grafana"]
architecture: ["System Design", "Microservices", "Event-Driven", "DDD", "CQRS", "API Design"]
```
**Weighting**: languages (0.2) + databases (0.2) + messaging (0.15) + cloud (0.15) + devops (0.15) + architecture (0.15)

### Taleo
**Keywords**: `Java`, `Go`, `Python`, `Node`, `SQL`, `PostgreSQL`, `AWS`, `Docker`, `Kubernetes`, `REST`, `GraphQL`, `Agile`, `Scrum`, `CI/CD`, `Git`, `Linux`
**Boolean**: `("Go" OR "Golang") AND ("Node" OR "Node.js" OR "NodeJS") AND ("PostgreSQL" OR "Postgres") AND ("AWS" OR "Amazon Web Services") AND ("Docker" OR "Kubernetes")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: High-Scale Platform Team (FinTech, Ads, Marketplace)
**Keywords**: `high throughput`, `low latency`, `distributed systems`, `consistency`, `availability`, `kafka`, `event sourcing`, `cqrs`, `dddd`, `saga`, `observability`, `slo`, `sli`, `on-call`, `incident command`
**Mirror**: Lead with **scale metrics** (req/sec, latency p99, data volume). Use `architected`, `optimized`, `designed for`. Emphasize **reliability**, **observability**, **incident response**.

### Archetype 2: Product-Focused Backend (SaaS, B2B, Consumer)
**Keywords**: `api design`, `graphql`, `rest`, `database design`, `migrations`, `feature flags`, `progressive delivery`, `developer experience`, `product collaboration`, `roadmap`, `technical debt`
**Mirror**: Lead with **API design**, **developer experience**, **product partnership**. Use `designed`, `delivered`, `collaborated`, `iterated`. Balance **velocity** with **quality**.

### Archetype 3: Infrastructure/Platform Engineering
**Keywords**: `platform`, `internal tools`, `developer productivity`, `self-service`, `kubernetes`, `operator`, `crd`, `gitops`, `argocd`, `flux`, `service mesh`, `istio`, `linkerd`, `cost optimization`, `finops`
**Mirror**: Lead with **platform impact** (engineers served, deploy frequency, MTTR). Use `built`, `enabled`, `standardized`, `automated`. Emphasize **leverage**, **multiplier effect**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `Go` / `Node.js` / `Python` | JD requires; resume has only one | Add secondary language to Skills; show in 1+ bullet |
| `PostgreSQL` / `Redis` | JD requires; resume says "SQL" | Specify `PostgreSQL 15 (Partitioning, Read Replicas)`, `Redis 7 (Cluster, Streams)` |
| `Kafka` / `gRPC` | JD requires messaging; resume has REST only | Add `Kafka (Exactly-Once, Schema Registry)`, `gRPC (Streaming, Interceptors)` |
| `Kubernetes` | JD requires; resume has Docker only | Add `Kubernetes (EKS/GKE, Helm, Kustomize, ArgoCD)`; describe cluster ops |
| `Terraform` / `Pulumi` | JD requires IaC; missing | Add `Terraform (Modules, State, Drift Detection)`; cite infra managed |
| `OpenTelemetry` / `Prometheus` | JD requires observability; missing | Add `OpenTelemetry (Auto/Manual)`, `Prometheus/Grafana (SLOs, Alerting)` |
| `System Design` | Senior+ JD; missing from resume | Add `System Design: Scalability, Reliability, DDD, Event Sourcing, CQRS` |
| `Mentoring` / `Code Review` | Senior+ JD; missing | Add `Mentored N engineers`, `Led code reviews`, `Defined standards` |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| GitHub: OSS library (Go/Node/Python) | `Open Source`, `Go`, `TypeScript`, `NPM`, `Crates.io` | Projects, GitHub Link |
| Tech Blog: System Design Deep-Dives | `System Design`, `Architecture`, `Technical Writing` | Writing, Speaking |
| Conference Talk | `Public Speaking`, `Conference`, `Knowledge Sharing` | Speaking, Leadership |
| Incident Postmortem (sanitized) | `Incident Response`, `Postmortem`, `Reliability` | Experience, Leadership |
| Performance Optimization Case Study | `Performance`, `Profiling`, `Load Testing`, `Latency` | Experience, Projects |

---

## Role-Specific ATS Optimization Notes

### Red Flags
- Only frontend skills listed → not backend
- "MongoDB" only, no PostgreSQL → relational gap
- No cloud provider → can't operate in production
- No testing keywords → quality blind spot
- "Microservices" but no Kafka/gRPC/observability → buzzword only

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `Go`, `Node.js`, `PostgreSQL`, `Redis`, `Kafka`, `Docker`, `Kubernetes`, `AWS`, `System Design` |
| High | 1.5% | 3.0% | `gRPC`, `GraphQL`, `Terraform`, `OpenTelemetry`, `Prometheus`, `Temporal`, `DDD`, `CQRS` |
| Medium | 1.0% | 2.5% | `Redis Cluster`, `Istio`, `ArgoCD`, `Mentoring`, `Architecture Review`, `Cost Optimization` |
| Low | 0.5% | 1.5% | `Rust`, `Java`, `ClickHouse`, `Chaos Engineering`, `FinOps`, `eBPF` |

### NDA Abstraction
- **L2**: "High-throughput payment platform (10M+ txn/day, 50TB+) on AWS/Kubernetes"
- **L3**: "Redesigned order pipeline cutting latency 60% and cost 40% via event-driven architecture"
- **L4**: "Cut p99 latency 60% and cloud spend 40% through architecture optimization"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `software-engineer/backend-engineer`
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 9 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for apps, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (scope/scale), Tech Lead (patterns), Exec (business impact)
- [ ] Metrics validated via `metric_plausibility.py`
- [ ] Portfolio cross-refs: GitHub/blog/talks with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024