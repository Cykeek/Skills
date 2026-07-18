---
role_id: "product-manager/platform-pm"
canonical_title: "Platform Product Manager"
aliases: ["Platform PM", "Internal Tools PM", "Developer Platform PM", "Infrastructure PM", "Internal Products PM", "Engineering Productivity PM"]
seniority_levels: ["Mid", "Senior", "Staff", "Principal"]
related_roles: ["product-manager/technical-pm", "devops-platform/devops-engineer", "software-engineer/backend-engineer", "engineering-manager", "data-science/data-engineer"]
ats_keywords:
  - "Platform"
  - "Developer Experience"
  - "DX"
  - "Internal Developer Platform"
  - "IDP"
  - "Backstage"
  - "Platform Engineering"
  - "Golden Paths"
  - "Paved Roads"
  - "Self-Service"
  - "API Gateway"
  - "Service Mesh"
  - "Kubernetes"
  - "CI/CD"
  - "Observability"
  - "SLI"
  - "SLO"
  - "SLA"
  - "Adoption"
  - "NPS"
  - "Time to Value"
  - "Developer Productivity"
  - "Engineering Efficiency"
  - "Internal Tools"
  - "Build vs Buy"
  - "Vendor Evaluation"
  - "FinOps"
  - "Cost Optimization"
  - "Reliability"
  - "Incident Management"
  - "On-Call"
  - "Stakeholder Management"
  - "Cross-Functional"
ats_skills_taxonomy:
  platform_strategy:
    - "Vision: Platform as Product, Internal Customers (Engineers), North Star (Developer Productivity), Investment Allocation (Platform vs Feature), Build vs Buy vs Partner"
    - "Roadmap: Now/Next/Later, Theme-based (Golden Path, DX, Reliability, Cost), Outcome-oriented (Adoption, NPS, TTV, MTTR), Dependency Mapping, Capacity Planning (Platform Team Ratio 1:10-1:20)"
    - "Prioritization: RICE/WSJF adapted for Platform (Leverage = Users × Frequency × Time Saved), Technical Debt Budget (15-20%), Strategic Bets (New Paradigms: GitOps, Service Mesh, Wasm)"
    - "Metrics: Adoption (% teams, % services), NPS (Quarterly), Time-to-Value (Idea → Prod), Deployment Frequency, Lead Time, Change Failure Rate, MTTR, Cost per Transaction, Platform Team Efficiency"
  internal_developer_platform:
    - "IDP Core: Backstage (Software Catalog, Scaffolder, TechDocs, Plugins), Port, Cortex, OpsLevel, Humanitec, Cycloid (Catalog, Self-Service Actions, Scorecards, RBAC)"
    - "Golden Paths: Paved Roads (CI/CD, Observability, Security, Deploy), Templates (Cookiecutter, Backstage Scaffolder), Standards (Linting, Testing, Versioning), Defaults (Sensible Configurations)"
    - "Self-Service: Provisioning (Infrastructure, Databases, Caches, Queues), Secrets Management (Vault, Sealed Secrets, External Secrets), Environment Management (Preview, Staging, Production)"
    - "Developer Portal: Documentation (TechDocs, MkDocs, Docusaurus), API Catalog (OpenAPI, GraphQL), Runbooks, Onboarding Flows, Search, Scorecards (Maturity, Security, Reliability)"
  ci_cd_platform:
    - "Pipeline: GitHub Actions/GitLab CI/Jenkins/Buildkite/CircleCI (Reusable Workflows, Matrix, Environments, Approval Gates, OIDC, Attestations)"
    - "GitOps: ArgoCD/Flux (Applications, AppProjects, ApplicationSets, Sync Windows, Health Checks, Rollback, Progressive Delivery)"
    - "Progressive Delivery: Argo Rollouts/Flagger (Canary, Blue/Green, A/B, Analysis, Metrics, Automated Rollback)"
    - "Supply Chain: SLSA, Sigstore/Cosign (Signing, Verification, Transparency), SBOM (Syft, SPDX), Dependency Scanning (Dependabot, Renovate, Trivy), Policy (Kyverno, OPA/Gatekeeper)"
  infrastructure_platform:
    - "Kubernetes: EKS/GKE/AKS (Cluster API, Karpenter, Cluster Autoscaler), Operators (Prometheus, Kafka, PostgreSQL, Redis, Vault), Helm/Kustomize, KEDA (Event-driven Autoscaling)"
    - "Service Mesh: Istio/Linkerd/Cilium (mTLS, Traffic Management, Authorization, Observability, Resilience, Zero Trust)"
    - "API Gateway: Kong/Apigee/AWS API Gateway/Envoy (Rate Limiting, Auth, Transformation, Analytics, Developer Portal)"
    - "Networking: CNI (Cilium, Calico, VPC-CNI), Service Discovery (CoreDNS, Consul), Ingress (NGINX, Traefik, ALB), Egress, Network Policies"
  observability_platform:
    - "Metrics: Prometheus/Thanos/Cortex/Mimir (Remote Write, Ruler, Compactor, Query Federation), OpenTelemetry (Collector, SDKs, Semantic Conventions), RED/USE Method"
    - "Logs: Loki/ELK/OpenSearch (Ingestion, Retention, Query, Alerting), Structured Logging (JSON, OpenTelemetry), Log-Based Metrics"
    - "Traces: Tempo/Jaeger/Zipkin (Sampling, Tail-based, TraceQL), OpenTelemetry Instrumentation (Auto, Manual), Service Graph"
    - "SLO/SLI: Burn Rate Alerting (Multi-window, Multi-burn-rate), Error Budgets, SLO Dashboards, Alert Routing (PagerDuty, Opsgenie, OnCall)"
    - "Profiling: Pyroscope/Parca (Continuous Profiling, eBPF, Flame Graphs, Memory/CPU/Block/Alloc), Performance Optimization"
  reliability_platform:
    - "Incident: Runbooks (Automated, Executable), Incident Commander, Blameless Postmortems, RCA (5 Whys, Fishbone), Action Item Tracking"
    - "Chaos: Chaos Mesh/Litmus/Gremlin (Experiments, Game Days, Resilience Validation), Fault Injection (Network, Pod, Time, IO)"
    - "Capacity: Forecasting (ML-based), Rightsizing (VPA, Goldilocks), Quotas, Limits, Priority Classes, Descheduler"
    - "Disaster Recovery: Backup (Velero, etcd), Restore Testing, RPO/RTO, Multi-Region, Failover Drills"
  security_platform:
    - "Policy: Kyverno/OPA/Gatekeeper (Admission Control, Validating/Mutating, Mutation, Generation), Pod Security Standards, Network Policies"
    - "Secrets: Vault (Dynamic, Transit, PKI, Database), External Secrets Operator, Sealed Secrets, CSI Driver"
    - "Compliance: SOC2/PCI-DSS/HIPAA/GDPR Evidence Collection, Audit Logs (Falco, Auditd), Drift Detection, Remediation"
    - "Supply Chain: SBOM, SLSA, Sigstore, Image Signing, Admission Verification, Provenance, Reproducible Builds"
  financing_governance:
    - "FinOps: Cost Allocation (Team, Service, Environment, Label), Showback/Chargeback, Anomaly Detection, Rightsizing, Commitments (RI, Savings Plans)"
    - "Governance: Platform Council (Architecture Review, Standards, Exceptions), RFC Process, Architecture Decision Records (ADRs), Tech Radar"
    - "Vendor: Evaluation (RFI/RFP, POC, Scoring), Contract Negotiation, Renewal Management, Exit Strategy, Multi-cloud Strategy"
    - "Team: Platform Team Topologies (Stream-aligned, Platform, Enabling, Complicated-Subsystem), Hiring, Career Ladder, On-Call Rotation"
ats_weight_hints:
  must_have:
    - "Platform"
    - "Developer Experience"
    - "Internal Developer Platform"
    - "Platform Engineering"
    - "Golden Paths"
    - "Self-Service"
    - "Kubernetes"
    - "CI/CD"
    - "Observability"
    - "SLI"
    - "SLO"
    - "Adoption"
    - "NPS"
    - "Time to Value"
    - "Developer Productivity"
    - "Stakeholder Management"
    - "Cross-Functional"
    - "Build vs Buy"
    - "FinOps"
    - "Cost Optimization"
  strong_signal:
    - "Backstage"
    - "IDP"
    - "Paved Roads"
    - "API Gateway"
    - "Service Mesh"
    - "Istio"
    - "Linkerd"
    - "ArgoCD"
    - "Flux"
    - "GitOps"
    - "Progressive Delivery"
    - "Argo Rollouts"
    - "Flagger"
    - "OpenTelemetry"
    - "Prometheus"
    - "Grafana"
    - "Loki"
    - "Tempo"
    - "Chaos Engineering"
    - "Chaos Mesh"
    - "Kyverno"
    - "OPA"
    - "Vault"
    - "External Secrets"
    - "FinOps"
    - "Showback"
    - "Chargeback"
  nice_to_have:
    - "Port"
    - "Cortex"
    - "OpsLevel"
    - "Humanitec"
    - "Cycloid"
    - "Karpenter"
    - "Cluster API"
    - "KEDA"
    - "Cilium"
    - "Envoy"
    - "Kong"
    - "Apigee"
    - "SLSA"
    - "Sigstore"
    - "Cosign"
    - "SBOM"
    - "Syft"
    - "Trivy"
    - "Dependabot"
    - "Renovate"
    - "Pyroscope"
    - "Parca"
    - "Velero"
    - "Goldilocks"
    - "VPA"
    - "Platform Council"
    - "ADR"
    - "Tech Radar"
ats_parser_hints:
  greenhouse:
    - "platform"
    - "developer experience"
    - "internal developer platform"
    - "platform engineering"
    - "golden paths"
    - "self-service"
    - "kubernetes"
    - "ci/cd"
    - "observability"
    - "sli"
    - "slo"
    - "adoption"
    - "nps"
    - "time to value"
    - "developer productivity"
    - "stakeholder management"
    - "cross-functional"
    - "build vs buy"
    - "finops"
    - "cost optimization"
  lever:
    - "platform"
    - "developer experience"
    - "internal developer platform"
    - "platform engineering"
    - "golden paths"
    - "self-service"
    - "kubernetes"
    - "ci/cd"
    - "observability"
    - "sli"
    - "slo"
    - "adoption"
    - "nps"
    - "time to value"
    - "developer productivity"
    - "stakeholder management"
    - "cross-functional"
    - "build vs buy"
    - "finops"
    - "cost optimization"
  workday:
    - "Platform"
    - "Developer Experience"
    - "Internal Developer Platform"
    - "Platform Engineering"
    - "Golden Paths"
    - "Self-Service"
    - "Kubernetes"
    - "CI/CD"
    - "Observability"
    - "SLI"
    - "SLO"
    - "Adoption"
    - "NPS"
    - "Time to Value"
    - "Developer Productivity"
    - "Stakeholder Management"
    - "Cross-Functional"
    - "Build vs Buy"
    - "FinOps"
    - "Cost Optimization"
  icims:
    skill_clusters:
      platform: ["Platform", "Developer Experience", "Internal Developer Platform", "Platform Engineering", "Golden Paths", "Paved Roads", "Self-Service", "Backstage", "IDP"]
      infrastructure: ["Kubernetes", "EKS", "GKE", "AKS", "Service Mesh", "Istio", "Linkerd", "Cilium", "API Gateway", "Kong", "Envoy", "Networking", "CNI"]
      cicd: ["CI/CD", "GitHub Actions", "GitLab CI", "ArgoCD", "Flux", "GitOps", "Progressive Delivery", "Argo Rollouts", "Flagger", "Supply Chain", "SLSA", "Sigstore"]
      observability: ["Observability", "OpenTelemetry", "Prometheus", "Grafana", "Loki", "Tempo", "SLI", "SLO", "Error Budgets", "Burn Rate", "Profiling", "Pyroscope"]
      reliability: ["Reliability", "Incident Management", "Runbooks", "Postmortems", "Chaos Engineering", "Chaos Mesh", "Capacity Planning", "Disaster Recovery", "Velero"]
      security: ["Security", "Kyverno", "OPA", "Gatekeeper", "Vault", "Secrets", "Compliance", "SOC2", "Supply Chain", "SBOM", "Image Signing"]
      governance: ["FinOps", "Cost Allocation", "Showback", "Chargeback", "Governance", "Platform Council", "RFC", "ADR", "Tech Radar", "Vendor Management"]
  taleo:
    keywords: "Platform, Developer Experience, Internal Developer Platform, Platform Engineering, Golden Paths, Self-Service, Kubernetes, CI/CD, Observability, SLI, SLO, Adoption, NPS, Time to Value, Developer Productivity, Stakeholder Management, Cross-Functional, Build vs Buy, FinOps, Cost Optimization, Backstage, ArgoCD, GitOps, OpenTelemetry, Prometheus, Grafana, Chaos Engineering, Kyverno, OPA, Vault, FinOps"
    boolean: "("Platform" OR "Developer Experience" OR "Platform Engineering") AND ("Kubernetes" OR "K8s" OR "EKS" OR "GKE") AND ("CI/CD" OR "GitOps" OR "ArgoCD" OR "Flux") AND ("Observability" OR "OpenTelemetry" OR "Prometheus" OR "Grafana") AND ("Golden Paths" OR "Self-Service" OR "Backstage" OR "IDP")"
---
## Role Summary

> **Platform Product Manager** — Treats internal developer platform as a product. Owns IDP strategy, golden paths, self-service capabilities, and platform adoption. Balances leverage (engineers served × time saved) against platform team capacity. At Staff+ defines company-wide platform strategy, governance, and financing.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### Platform Strategy & Roadmap (All Levels)
- Define **Platform as Product** strategy: **internal customers** (engineers), **North Star Metric** (Developer Productivity: Deployment Frequency × Lead Time⁻¹ × Change Failure Rate⁻¹), **investment allocation** (Platform 20% / Feature 80% → shift to 30/70)
- Build **theme-based roadmap**: **Golden Paths** (CI/CD, Observability, Security, Deploy), **DX** (Backstage, Docs, Onboarding), **Reliability** (SLO, Chaos, Incident), **Cost** (FinOps, Rightsizing), **Strategic Bets** (Wasm, GitOps, Service Mesh)
- Prioritize using **Platform RICE**: **Reach** (% engineers), **Impact** (Time Saved × Frequency), **Confidence** (Validation), **Effort** (Platform Team Weeks); **Technical Debt Budget 15-20%**; **Leverage = Reach × Impact / Effort**
- Track **Platform Metrics**: **Adoption** (% teams onboarded, % services on golden path), **NPS** (Quarterly, Target >50), **Time-to-Value** (Idea → Prod: 4hrs → 30min), **DORA** (Deployment Freq, Lead Time, CFR, MTTR), **Cost/Transaction**, **Platform Team Efficiency**

### Internal Developer Platform (IDP) (Mid+)
- Own **Backstage** (or Port/Cortex/OpsLevel/Humanitec): **Software Catalog** (Services, APIs, Resources, Systems, Domains), **Scaffolder** (Templates, Cookiecutter, Actions), **TechDocs** (MkDocs, Diagrams), **Plugins** (Kubernetes, ArgoCD, Jira, PagerDuty, GitHub, Datadog)
- Design **Golden Paths / Paved Roads**: **CI/CD Templates** (GitHub Actions Reusable Workflows), **Observability Defaults** (Dashboards, Alerts, SLIs), **Security Baselines** (Kyverno Policies, Pod Security Standards), **Deployment Patterns** (ArgoCD AppProjects, Progressive Delivery)
- Enable **Self-Service**: **Infrastructure Provisioning** (Terraform Modules, Crossplane, Backstage Actions), **Database/Cache/Queue Provisioning** (Operators, Service Binding), **Secrets Management** (Vault, External Secrets Operator), **Environment Management** (Preview, Staging, Production, Ephemeral)
- Build **Developer Portal**: **API Catalog** (OpenAPI, GraphQL), **Documentation** (TechDocs, Architecture Decision Records), **Runbooks** (Executable, Incident-Linked), **Onboarding Flows** (New Hire → First Deploy <1hr), **Scorecards** (Maturity, Security, Reliability, Cost)

### CI/CD & GitOps Platform (Mid+)
- Standardize **Pipeline Platform**: **GitHub Actions** (Reusable Workflows, Composite Actions, Matrix, Environments, OIDC, Attestations), **GitLab CI** (Templates, Includes, DAG, Needs), **Buildkite** (Pipelines, Plugins, Agents)
- Implement **GitOps**: **ArgoCD / Flux** (Applications, AppProjects, ApplicationSets, Sync Windows, Health Checks, Auto-Prune, Self-Heal, Rollback, Notifications)
- Enable **Progressive Delivery**: **Argo Rollouts / Flagger** (Canary, Blue/Green, A/B, Analysis Templates, Metrics Providers: Prometheus, Datadog, New Relic, Kayenta, Automated Rollback)
- Secure **Supply Chain**: **SLSA Level 3**, **Sigstore/Cosign** (Keyless Signing, Verification, Transparency Log), **SBOM** (Syft, SPDX, CycloneDX), **Dependency Scanning** (Dependabot, Renovate, Trivy), **Policy Enforcement** (Kyverno, OPA/Gatekeeper, Admission Control)

### Infrastructure & Kubernetes Platform (Senior+)
- Operate **Kubernetes Fleet**: **EKS/GKE/AKS** (Cluster API, Karpenter, Cluster Autoscaler), **Operators** (Prometheus, Kafka, PostgreSQL, Redis, Vault, Cert-Manager, External-DNS), **Helm/Kustomize**, **KEDA** (Event-driven Autoscaling: Kafka, RabbitMQ, HTTP, Cron)
- Manage **Service Mesh**: **Istio / Linkerd / Cilium** (mTLS, Traffic Management: Canary, Mirror, Retry, Timeout, Circuit Breaker, Fault Injection, Authorization Policies, Observability Integration)
- Provide **API Gateway**: **Kong / Apigee / AWS API Gateway / Envoy** (Rate Limiting, Auth: OAuth2/OIDC/JWT/mTLS, Transformation, Analytics, Developer Portal, GraphQL Federation)
- Design **Networking**: **CNI** (Cilium, Calico, VPC-CNI), **Service Discovery** (CoreDNS, Consul), **Ingress** (NGINX, Traefik, ALB), **Egress**, **Network Policies** (Calico, Cilium, Kube-router)

### Observability & Reliability Platform (Senior+)
- Build **Unified Observability**: **Metrics** (Prometheus/Thanos/Cortex/Mimir: Remote Write, Ruler, Compactor, Query Federation), **OpenTelemetry** (Collector, SDKs, Semantic Conventions), **RED/USE Method**
- Centralize **Logs**: **Loki / ELK / OpenSearch** (Ingestion, Retention, Query: LogQL, Alerting, Log-Based Metrics), **Structured Logging** (JSON, OpenTelemetry Logs)
- Distribute **Traces**: **Tempo / Jaeger / Zipkin** (Sampling: Head/Tail, Tail-based, TraceQL), **OpenTelemetry Instrumentation** (Auto: Java/Go/Python/Node, Manual), **Service Graph**
- Define **SLO/SLI Platform**: **Burn Rate Alerting** (Multi-window, Multi-burn-rate), **Error Budgets**, **SLO Dashboards**, **Alert Routing** (PagerDuty, Opsgenie, Grafana OnCall), **SLO-based Prioritization**
- Enable **Continuous Profiling**: **Pyroscope / Parca** (eBPF, Flame Graphs, Memory/CPU/Block/Alloc, Performance Optimization, Regression Detection)

### Reliability & Security Platform (Staff+)
- Codify **Incident Management**: **Runbooks** (Automated, Executable, Linked to Alerts), **Incident Commander Role**, **Blameless Postmortems**, **RCA** (5 Whys, Fishbone), **Action Item Tracking** (Jira/Linear/GitHub Issues, SLA)
- Practice **Chaos Engineering**: **Chaos Mesh / Litmus / Gremlin** (Experiments: Pod Kill, Network Partition, Latency, IO, Time, DNS, Kernel, Game Days, Resilience Validation, CI Integration)
- Plan **Capacity**: **Forecasting** (ML-based, Seasonal, Trend), **Rightsizing** (VPA, Goldilocks), **Quotas**, **Limits**, **Priority Classes**, **Descheduler**, **Cluster Lifecycle**
- Execute **Disaster Recovery**: **Backup** (Velero, etcd), **Restore Testing** (Quarterly, Automated), **RPO/RTO**, **Multi-Region**, **Failover Drills** (Annual, Documented)
- Enforce **Security Policy**: **Kyverno / OPA / Gatekeeper** (Admission Control: Validating/Mutating, Generation, Pod Security Standards, Network Policies, Image Verification)
- Manage **Secrets**: **Vault** (Dynamic, Transit, PKI, Database), **External Secrets Operator**, **Sealed Secrets**, **CSI Driver**, **Rotation**, **Audit**
- Ensure **Compliance**: **SOC2/PCI-DSS/HIPAA/GDPR** (Evidence Collection, Audit Logs: Falco, Auditd, Drift Detection, Automated Remediation)
- Secure **Supply Chain**: **SBOM** (Syft, SPDX, CycloneDX), **SLSA**, **Sigstore/Cosign** (Image Signing, Verification, Transparency), **Provenance**, **Reproducible Builds**

### FinOps & Governance (Staff+)
- Implement **FinOps**: **Cost Allocation** (Team, Service, Environment, Label), **Showback/Chargeback** (Kubecost, OpenCost, Cloud Provider Native), **Anomaly Detection** (ML, Threshold), **Rightsizing** (VPA, Goldilocks, Manual), **Commitments** (RI, Savings Plans, CUDs)
- Establish **Platform Governance**: **Platform Council** (Architecture Review, Standards, Exceptions), **RFC Process** (Proposal, Review, Decision, Implementation), **ADRs** (Architecture Decision Records), **Tech Radar** (Adopt, Trial, Assess, Hold)
- Manage **Vendors**: **Evaluation** (RFI/RFP, POC, Scoring: Technical, Commercial, Legal, Security), **Contract Negotiation**, **Renewal Management**, **Exit Strategy**, **Multi-cloud Strategy**
- Build **Platform Team**: **Team Topologies** (Stream-aligned, Platform, Enabling, Complicated-Subsystem), **Hiring** (Seniority Mix, Skills), **Career Ladder** (IC/Manager), **On-Call Rotation** (Follow-the-Sun, Sustainable)

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
- **Platform**, **Developer Experience**, **Internal Developer Platform**, **Platform Engineering**
- **Golden Paths**, **Self-Service**, **Kubernetes**, **CI/CD**, **Observability**
- **SLI**, **SLO**, **Adoption**, **NPS**, **Time to Value**, **Developer Productivity**
- **Stakeholder Management**, **Cross-Functional**, **Build vs Buy**, **FinOps**, **Cost Optimization**

### Strong Signal (Differentiators)
- **Backstage**, **IDP**, **Paved Roads**, **API Gateway**, **Service Mesh**, **Istio**, **Linkerd**
- **ArgoCD**, **Flux**, **GitOps**, **Progressive Delivery**, **Argo Rollouts**, **Flagger**
- **OpenTelemetry**, **Prometheus**, **Grafana**, **Loki**, **Tempo**, **Chaos Engineering**, **Chaos Mesh**
- **Kyverno**, **OPA**, **Vault**, **External Secrets**, **FinOps**, **Showback**, **Chargeback**

### Nice-to-Have (Specialization)
- **Port**, **Cortex**, **OpsLevel**, **Humanitec**, **Cycloid**, **Karpenter**, **Cluster API**, **KEDA**, **Cilium**, **Envoy**, **Kong**, **Apigee**
- **SLSA**, **Sigstore**, **Cosign**, **SBOM**, **Syft**, **Trivy**, **Dependabot**, **Renovate**, **Pyroscope**, **Parca**, **Velero**, **Goldilocks**, **VPA**
- **Platform Council**, **ADR**, **Tech Radar**

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Mid (2-5 yrs)
- **Owned** **Backstage IDP** for **200 engineers**: **Software Catalog** (500+ entities), **Scaffolder** (20 templates), **TechDocs** (100% coverage); **Adoption 85%**, **NPS 45**
- **Built** **Golden Path** for **CI/CD** (**GitHub Actions Reusable Workflows**): **15 microservices onboarded**, **Pipeline Time 45min → 12min**, **Failure Rate 12% → 3%**
- **Implemented** **GitOps** (**ArgoCD**): **50 applications**, **Sync Windows**, **Health Checks**, **Auto-Rollback**; **Deployment Frequency Daily → On-Demand**, **Lead Time 2hrs → 15min**
- **Established** **SLO Platform** (**Prometheus**, **Grafana**, **Burn Rate Alerting**): **50 SLIs**, **Error Budget Policies**, **Alert Routing**; **MTTR 4hrs → 45min**, **False Positives -80%**
- **Drove** **FinOps** (**Kubecost**, **Showback**): **Cost Allocation** (Team/Service/Env), **Rightsizing** (VPA); **Cloud Spend -15%**, **$200K/yr Saved**

### Senior (5-8 yrs)
- **Architected** **Platform Strategy** for **500 engineers**: **IDP** (Backstage), **Golden Paths** (4 domains), **GitOps** (ArgoCD), **Observability** (OpenTelemetry, Tempo, Loki), **Service Mesh** (Istio); **Adoption 80%**, **TTV 4hrs → 30min**
- **Led** **Platform Consolidation** (3→1): **Kubernetes** (EKS), **CI/CD** (GitHub Actions), **Observability** (Datadog→OpenTelemetry); **Platform Team 15→8**, **Cost -30%**, **$2M/yr Saved**
- **Built** **Self-Service Infrastructure** (**Crossplane**, **Backstage Actions**): **Database/Cache/Queue Provisioning** (<5min vs 2 days), **200+ Resources/Day**, **Zero Tickets**
- **Established** **Platform Governance**: **Platform Council**, **RFC Process** (50+/yr), **ADRs** (200+), **Tech Radar**; **Exception Rate <5%**, **Decision Velocity 2wks → 3days**
- **Managed** **Vendor Portfolio** ($5M): **Evaluation** (RFI/RFP/POC), **Negotiation** (Enterprise Discounts 25%), **Renewal** (Zero Surprise), **Exit Strategy** (2 Migrations)
- **Mentored** **3 PMs**; **Defined** **Platform PM Career Ladder**; **Hired** **10+ Platform Engineers**; **Spoke** at **PlatformCon**, **KubeCon**, **QCon**

### Staff (8-12 yrs)
- **Set** **Company-Wide Platform Direction**: **AI-Native Platform** (GPU Sharing, Model Serving, RAG), **Multi-Cloud** (AWS/GCP), **Platform Team Topologies** (4 Platform Teams, 20 Stream-aligned); **Board-Approved $50M Investment**
- **Built** **Platform Serving 2000 Engineers**: **IDP** (Backstage, 95% Adoption), **Golden Paths** (10 Domains), **GitOps** (100% Services), **SLO** (99.99% Availability), **FinOps** ($50M Budget, 95% Allocated); **NPS 65**
- **Drove** **Developer Productivity Transformation**: **SPACE Metrics** (Satisfaction, Performance, Activity, Communication, Efficiency); **Lead Time 4hrs → 20min**, **Deployment Freq Weekly → 50x/Day**, **CFR 15% → 2%**
- **Architected** **Security & Compliance Platform**: **Zero Trust** (Istio mTLS, OPA), **Supply Chain** (SLSA L3, Sigstore), **Secrets** (Vault, Dynamic), **Compliance** (SOC2 Type II, Automated Evidence); **Audit Pass Zero Findings**
- **Grew** **Platform Org** 20→100; **Dual-Track IC/Manager**; **Industry Hiring Bar**; **Keynotes** (PlatformCon, KubeCon, QCon, AWS re:Invent); **CNCF TAG App Delivery Chair**
- **Advised** **CTO/CEO** on **Platform Strategy**, **Build vs Buy** (Backstage vs Port vs Humanitec), **M&A Platform Due Diligence**, **Talent Strategy**

### Principal (12+ yrs)
- **Industry Vision**: **Platform Engineering** (Platform as Product, Team Topologies, IDP, Golden Paths), **AI-Native Platforms**, **Developer Experience**; **Keynotes**, **Book** (O'Reilly), **Papers** (ICSE, FSE, SREcon), **Standards** (CNCF, OpenGitOps)
- **Recognition**: **Fellow**, **Top Platform Leaders**, **Patents**, **Editorial Boards**, **Conference Chairs** (PlatformCon, KubeCon, SREcon, QCon)
- **Crisis Leadership**: **Platform Outage** (Global, 1hr), **Security Incident** (Supply Chain), **Regulatory Response** (SEC, GDPR), **Cost Crisis** (Cloud Bill 3x), **Talent Retention** (Platform Team)
- **Transforms Organization**: **Product-Led Platform Culture**, **Customer Obsession** (Internal), **Data-Driven Platform Decisions**, **Experimentation at Scale**, **Technical Excellence as Strategy**

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `platform`, `developer experience`, `internal developer platform`, `platform engineering`, `golden paths`, `self-service`, `kubernetes`, `ci/cd`, `observability`, `sli`, `slo`, `adoption`, `nps`, `time to value`, `developer productivity`, `stakeholder management`, `cross-functional`, `build vs buy`, `finops`, `cost optimization`

### Lever
**Exact**: `platform`, `developer experience`, `internal developer platform`, `platform engineering`, `golden paths`, `self-service`, `kubernetes`, `ci/cd`, `observability`, `sli`, `slo`, `adoption`, `nps`, `time to value`, `developer productivity`, `stakeholder management`, `cross-functional`, `build vs buy`, `finops`, `cost optimization`

### Workday
**Exact (title case)**: `Platform`, `Developer Experience`, `Internal Developer Platform`, `Platform Engineering`, `Golden Paths`, `Self-Service`, `Kubernetes`, `CI/CD`, `Observability`, `SLI`, `SLO`, `Adoption`, `NPS`, `Time to Value`, `Developer Productivity`, `Stakeholder Management`, `Cross-Functional`, `Build vs Buy`, `FinOps`, `Cost Optimization`

### iCIMS
**Skill clusters**:
```
platform: ["Platform", "Developer Experience", "Internal Developer Platform", "Platform Engineering", "Golden Paths", "Paved Roads", "Self-Service", "Backstage", "IDP"]
infrastructure: ["Kubernetes", "EKS", "GKE", "AKS", "Service Mesh", "Istio", "Linkerd", "Cilium", "API Gateway", "Kong", "Envoy", "Networking", "CNI"]
cicd: ["CI/CD", "GitHub Actions", "GitLab CI", "ArgoCD", "Flux", "GitOps", "Progressive Delivery", "Argo Rollouts", "Flagger", "Supply Chain", "SLSA", "Sigstore"]
observability: ["Observability", "OpenTelemetry", "Prometheus", "Grafana", "Loki", "Tempo", "SLI", "SLO", "Error Budgets", "Burn Rate", "Profiling", "Pyroscope"]
reliability: ["Reliability", "Incident Management", "Runbooks", "Postmortems", "Chaos Engineering", "Chaos Mesh", "Capacity Planning", "Disaster Recovery", "Velero"]
security: ["Security", "Kyverno", "OPA", "Gatekeeper", "Vault", "Secrets", "Compliance", "SOC2", "Supply Chain", "SBOM", "Image Signing"]
governance: ["FinOps", "Cost Allocation", "Showback", "Chargeback", "Governance", "Platform Council", "RFC", "ADR", "Tech Radar", "Vendor Management"]
```

### Taleo
**Keywords**: `Platform, Developer Experience, Internal Developer Platform, Platform Engineering, Golden Paths, Self-Service, Kubernetes, CI/CD, Observability, SLI, SLO, Adoption, NPS, Time to Value, Developer Productivity, Stakeholder Management, Cross-Functional, Build vs Buy, FinOps, Cost Optimization, Backstage, ArgoCD, GitOps, OpenTelemetry, Prometheus, Grafana, Chaos Engineering, Kyverno, OPA, Vault, FinOps`
**Boolean**: `("Platform" OR "Developer Experience" OR "Platform Engineering") AND ("Kubernetes" OR "K8s" OR "EKS" OR "GKE") AND ("CI/CD" OR "GitOps" OR "ArgoCD" OR "Flux") AND ("Observability" OR "OpenTelemetry" OR "Prometheus" OR "Grafana") AND ("Golden Paths" OR "Self-Service" OR "Backstage" OR "IDP")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: Internal Developer Platform PM (Scale-Ups, Enterprise)
**Keywords**: `internal developer platform`, `idp`, `backstage`, `port`, `cortex`, `opslevel`, `humanitec`, `software catalog`, `scaffolder`, `techdocs`, `self-service`, `golden paths`, `paved roads`, `developer portal`, `adoption`, `nps`, `time to first hello world`, `onboarding`, `scorecards`, `platform team`, `team topologies`
**Mirror**: Lead with **platform leverage** (engineers served, adoption, NPS, time-to-value). Use `architected`, `built`, `standardized`, `enabled`, `measured`. Emphasize **self-serve**, **golden paths**, **paved roads**, **developer productivity**, **cost efficiency**, **team topologies**.

### Archetype 2: Infrastructure / Kubernetes Platform PM (Cloud-Native, High-Scale)
**Keywords**: `kubernetes`, `eks`, `gke`, `aks`, `cluster api`, `karpenter`, `service mesh`, `istio`, `linkerd`, `cilium`, `api gateway`, `kong`, `envoy`, `apigee`, `gitops`, `argocd`, `flux`, `progressive delivery`, `argo rollouts`, `flagger`, `observability`, `opentelemetry`, `prometheus`, `grafana`, `loki`, `tempo`, `slo`, `sli`, `error budgets`, `burn rate`, `chaos engineering`, `chaos mesh`, `finops`, `kubecost`, `showback`, `chargeback`
**Mirror**: Lead with **technical depth**, **scale**, **reliability**, **cost efficiency**. Use `operated`, `optimized`, `tuned`, `standardized`, `governed`. Emphasize **multi-cluster**, **service mesh**, **GitOps**, **SLO culture**, **chaos engineering**, **FinOps**, **security posture**.

### Archetype 3: Engineering Productivity / Developer Experience PM (Product-Led, DevTools)
**Keywords**: `developer experience`, `dx`, `engineering productivity`, `developer productivity`, `space metrics`, `satisfaction`, `performance`, `activity`, `communication`, `efficiency`, `time to value`, `lead time`, `deployment frequency`, `change failure rate`, `mttr`, `dora`, `internal tools`, `cli`, `sdk`, `local development`, `dev containers`, `codespaces`, `gitpod`, `build systems`, `bazel`, `turbo`, `nx`, `test infrastructure`, `flaky tests`, `test analytics`
**Mirror**: Lead with **productivity metrics**, **developer satisfaction**, **tool adoption**, **time savings**. Use `measured`, `improved`, `built`, `instrumented`, `optimized`. Emphasize **SPACE/DORA**, **local dev experience**, **build/test speed**, **flaky test reduction**, **feedback loops**, **cognitive load reduction**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `Platform` / `Platform Engineering` / `IDP` | Platform PM JD; missing | Add `Platform as Product Strategy`, `IDP` (Backstage/Port/Cortex), `Golden Paths`, `Self-Service`, `Adoption Metrics` |
| `Backstage` / `Software Catalog` / `Scaffolder` / `TechDocs` | IDP JD; missing | Add `Backstage Implementation`, `Catalog` (500+ entities), `Scaffolder` (20+ templates), `TechDocs` (100% coverage), `Plugins` |
| `Golden Paths` / `Paved Roads` / `Self-Service` | Platform JD; missing | Add `Golden Path Design` (CI/CD, Observability, Security, Deploy), `Paved Road Adoption` (% services), `Self-Service Provisioning` |
| `ArgoCD` / `Flux` / `GitOps` / `Progressive Delivery` | GitOps JD; missing | Add `GitOps Migration` (ArgoCD/Flux), `ApplicationSets`, `Sync Windows`, `Progressive Delivery` (Argo Rollouts/Flagger), `Canary/Blue-Green` |
| `OpenTelemetry` / `Prometheus` / `Grafana` / `Loki` / `Tempo` / `SLO` / `SLI` | Observability JD; missing | Add `Unified Observability` (OTel, Prometheus, Loki, Tempo), `SLO Platform` (Burn Rate, Error Budgets), `MTTR Reduction` |
| `Kubernetes` / `EKS` / `GKE` / `Service Mesh` / `Istio` / `Linkerd` | Infra Platform JD; missing | Add `Kubernetes Fleet` (EKS/GKE, Cluster API, Karpenter), `Service Mesh` (Istio/Linkerd/Cilium), `Operators`, `Networking` |
| `FinOps` / `Cost Allocation` / `Showback` / `Chargeback` / `Rightsizing` | FinOps JD; missing | Add `FinOps Program` (Kubecost/OpenCost), `Cost Allocation` (Team/Service/Env), `Showback/Chargeback`, `Rightsizing` (VPA/Goldilocks), `Commitments` |
| `Platform Council` / `RFC` / `ADR` / `Tech Radar` / `Governance` | Governance JD; missing | Add `Platform Governance` (Council, RFC Process, ADRs, Tech Radar), `Standards`, `Exception Process`, `Decision Velocity` |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| **GitHub: Backstage Plugin / IDP Tool / Platform Operator** | `Open Source`, `TypeScript`, `React`, `Backstage`, `Kubernetes`, `Operator`, `Community`, `Downloads` | Projects, GitHub Link |
| **Technical Blog: Platform Engineering / DX / GitOps / SLO** | `Technical Writing`, `Platform Engineering`, `Developer Experience`, `GitOps`, `SLO`, `Observability`, `FinOps`, `Best Practices` | Writing, Portfolio Link |
| **Conference Talk (PlatformCon, KubeCon, QCon, SREcon, API World)** | `Public Speaking`, `Thought Leadership`, `Platform Engineering`, `Developer Experience`, `GitOps`, `Observability`, `Open Source` | Speaking, Leadership |
| **CNCF / Open Source Contribution (Backstage, Argo, Flux, OpenTelemetry, Kyverno)** | `Open Source`, `Contributor`, `Maintainer`, `CNCF`, `Graduated`, `Incubating`, `Sandbox` | Projects, GitHub Link |
| **Internal Platform Case Study (Sanitized)** | `Platform Engineering`, `Adoption Metrics`, `Developer Productivity`, `Cost Savings`, `Change Management`, `Golden Paths`, `Team Topologies` | Experience, Projects |
| **RFC / ADR / Tech Radar Portfolio (Redacted)** | `Architecture Decision Records`, `RFC Process`, `Technical Writing`, `Stakeholder Alignment`, `Risk Mitigation`, `Governance` | Experience, Projects |

---

## Role-Specific ATS Optimization Notes

### Red Flags (Auto-Reject)
- **Only "Jira/Scrum"** — no platform strategy, IDP, golden paths → Project Manager, not Platform PM
- **No Kubernetes/CI/CD/Observability** → Technical depth gap for Platform PM
- **No adoption/NPS/TTV metrics** → Can't measure platform success
- **Only feature factory language** — "delivered features" not "enabled engineers" → Output over outcomes
- **No build vs. buy / vendor evaluation** → Strategic gap
- **>2 pages for <5 yrs** → Format penalty
- **Tables/columns/graphics** → Parser extraction failure

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `Platform`, `Developer Experience`, `Internal Developer Platform`, `Platform Engineering`, `Golden Paths`, `Self-Service`, `Kubernetes`, `CI/CD`, `Observability`, `SLI`, `SLO`, `Adoption`, `NPS`, `Time to Value`, `Developer Productivity`, `Stakeholder Management`, `Cross-Functional`, `Build vs Buy`, `FinOps`, `Cost Optimization` |
| High | 1.5% | 3.0% | `Backstage`, `IDP`, `Paved Roads`, `API Gateway`, `Service Mesh`, `Istio`, `Linkerd`, `ArgoCD`, `Flux`, `GitOps`, `Progressive Delivery`, `Argo Rollouts`, `Flagger`, `OpenTelemetry`, `Prometheus`, `Grafana`, `Loki`, `Tempo`, `Chaos Engineering`, `Chaos Mesh`, `Kyverno`, `OPA`, `Vault`, `External Secrets`, `FinOps`, `Showback`, `Chargeback` |
| Medium | 1.0% | 2.5% | `Port`, `Cortex`, `OpsLevel`, `Humanitec`, `Cycloid`, `Karpenter`, `Cluster API`, `KEDA`, `Cilium`, `Envoy`, `Kong`, `Apigee`, `SLSA`, `Sigstore`, `Cosign`, `SBOM`, `Syft`, `Trivy`, `Dependabot`, `Renovate`, `Pyroscope`, `Parca`, `Velero`, `Goldilocks`, `VPA`, `Platform Council`, `ADR`, `Tech Radar` |
| Low | 0.5% | 1.5% | `Team Topologies`, `Stream-aligned`, `Enabling`, `Complicated-Subsystem`, `Cognitive Load`, `Team API`, `Internal Developer Portal`, `Developer Portal`, `Portal`, `Scorecard`, `Maturity Model`, `Wasm`, `WebAssembly`, `Spin`, `Fermyon`, `Knative`, `Serverless`, `Event-Driven` |

### NDA Abstraction
- **L2**: "Platform product for 1000+ engineers at $50B+ enterprise; Kubernetes fleet 200+ clusters"
- **L3**: "Drove IDP adoption to 95% (500+ services); cut deployment lead time 94% (4hrs→15min); saved $3M/yr via FinOps"
- **L4**: "Achieved 95% platform adoption and reduced lead time 94% across 500+ services"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `product-manager/platform-pm`
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 10 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for applications, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (strategy/execution/adoption), Tech Lead (K8s/GitOps/Observability/SLO), Exec (leverage/cost/NPS/org design)
- [ ] Metrics validated via `metric_plausibility.py` (Adoption %, NPS, TTV, Lead Time, Deploy Freq, CFR, MTTR, Cost/Transaction, Platform Team Ratio)
- [ ] Portfolio cross-refs: GitHub/blog/talks/CNCF contributions/case studies with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024