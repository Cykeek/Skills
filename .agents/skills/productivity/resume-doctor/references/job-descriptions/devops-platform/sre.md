---
role_id: "devops-platform/sre"
canonical_title: "Site Reliability Engineer (SRE)"
aliases: ["SRE", "Site Reliability Engineer", "Production Engineer", "Reliability Engineer", "Platform Reliability Engineer"]
seniority_levels: ["Junior", "Mid", "Senior", "Staff", "Principal"]
related_roles: ["devops-platform/devops-engineer", "devops-platform/platform-engineer", "software-engineer/backend-engineer", "devops-platform/cloud-engineer"]
ats_keywords:
  - "SRE"
  - "Site Reliability Engineering"
  - "SLO"
  - "SLI"
  - "Error Budget"
  - "Incident Response"
  - "On-Call"
  - "Runbooks"
  - "Blameless Postmortems"
  - "Prometheus"
  - "Grafana"
  - "Alertmanager"
  - "PagerDuty"
  - "Opsgenie"
  - "Kubernetes"
  - "Docker"
  - "Go"
  - "Python"
  - "Bash"
  - "Linux"
  - "AWS"
  - "GCP"
  - "Terraform"
  - "CI/CD"
  - "GitOps"
  - "Observability"
  - "Distributed Tracing"
  - "Chaos Engineering"
  - "Capacity Planning"
  - "Disaster Recovery"
  - "RTO"
  - "RPO"
ats_skills_taxonomy:
  slos_error_budgets:
    - "SLO/SLI Definition: Latency (p50/p95/p99), Availability, Throughput, Correctness, Freshness"
    - "Error Budgets: Burn Rate Alerting (Multi-Window Multi-Burn-Rate), Alerting on SLO Violations"
    - "Service Level Objectives: Request-based vs Window-based, Rolling Windows, Budgeting Periods"
    - "Stakeholder Alignment: Product/Engineering agreement on SLO targets, error budget policies"
  incident_response:
    - "Incident Command System (ICS): IC, Comms, Scribe roles; severity levels (SEV-1/2/3); escalation policies"
    - "Runbooks: Executable, versioned, tested; runbook automation (RunDeck, Rundeck, custom)"
    - "Blameless Postmortems: Timeline, root cause (5 Whys), contributing factors, action items with owners/dates"
    - "Communication: Status pages (Statuspage.io, Atlassian), stakeholder updates, customer communication"
    - "On-Call: Rotation design, handoffs, sustainable practices (<2 pages/week, <1 nocturnal/week), compensation"
  observability:
    - "Metrics: Prometheus (PromQL, Recording/Alerting Rules, Federation, Thanos, Mimir, Cortex), OpenTelemetry Collector"
    - "Logs: Loki, Elasticsearch/OpenSearch, Vector/Fluent Bit/Fluentd (structured JSON, labels, sampling, retention)"
    - "Traces: Tempo, Jaeger, Zipkin (OpenTelemetry, W3C TraceContext, sampling, tail-based sampling)"
    - "Visualization: Grafana (dashboards, alerting, Loki/Tempo/Prometheus data sources, provisioning)"
    - "SLO/SLI: SLI definitions, error budgets, burn rate alerting (multi-window, multi-burn-rate)"
    - "RUM/Synthetic: Sentry, Datadog, Grafana Faro, Checkly, k6 Browser (Core Web Vitals, user journeys)"
  reliability_engineering:
    - "Chaos Engineering: Litmus, Chaos Mesh, Gremlin (pod kill, network latency, CPU stress, disk fill, clock skew)"
    - "Game Days: Planned exercises, hypothesis → experiment → learning, cross-team coordination"
    - "Capacity Planning: Demand forecasting, headroom, autoscaling (HPA/VPA/Cluster Autoscaler/Karpenter), load testing (k6/Gatling)"
    - "Disaster Recovery: RPO/RTO, backup/restore (Velero, etcd), cross-region failover, DR drills"
    - "Performance Optimization: Profiling (py-spy, pprof, eBPF), bottleneck identification, latency reduction"
  automation_tooling:
    - "Go: Standard library, Cobra (CLI), controller-runtime (operators), gRPC/Connect, testing (testify, ginkgo)"
    - "Python: FastAPI/Click/Typer (CLI), boto3/pulumi SDK, pytest, type hints (mypy/pyright), poetry/uv"
    - "Bash/Shell: POSIX, ShellCheck, shfmt, scripts (idempotent, robust, logging, error handling)"
    - "Infrastructure: Terraform/OpenTofu, Pulumi, AWS CDK, Ansible, Packer"
    - "CI/CD: GitHub Actions, GitLab CI, ArgoCD/Flux, progressive delivery (Argo Rollouts, Flagger)"
  kubernetes_internals:
    - "Control Plane: API server, controller manager, scheduler, etcd, kubelet, kube-proxy"
    - "Networking: CNI (Cilium, Calico), Service/Ingress/Gateway API, CoreDNS, Network Policies"
    - "Storage: CSI, PVC/PV, StorageClasses, snapshots, volume expansion"
    - "Security: RBAC, Pod Security Standards, OPA/Gatekeeper/Kyverno, mTLS (Istio/Cilium/Linkerd)"
    - "Operators: Operator SDK, Kubebuilder, controller-runtime (CRDs, webhooks, reconciliation)"
  cloud_platforms:
    - "AWS: EC2, ECS/EKS/Fargate, Lambda, RDS/Aurora, ElastiCache, S3, CloudFront, Route53, IAM, CloudFormation, CDK, Systems Manager"
    - "GCP: Compute Engine, GKE/Cloud Run, Cloud SQL, Memorystore, Cloud Storage, Cloud CDN, IAM, Deployment Manager, Cloud Build"
    - "Azure: VMs, AKS/Container Apps, Functions, Azure SQL, Cache for Redis, Blob Storage, Front Door, Entra ID, Bicep/ARM"
seniority_signals:
  junior:
    - "Participates in on-call rotation (shadowing); updates runbooks for common alerts"
    - "Debugs production issues: analyzes logs, metrics, traces; escalates appropriately"
    - "Writes automation scripts (Bash/Python/Go) for toil reduction: log cleanup, certificate rotation, backup verification"
    - "Maintains monitoring dashboards (Grafana); adds alerts for team services"
    - "Learns Kubernetes internals: pods, services, ingress, deployments, configmaps, secrets"
    - "Contributes to postmortems: documents timeline, identifies action items"
  mid:
    - "Owns SLO/SLI definitions for team services; implements burn-rate alerting; reviews error budgets weekly"
    - "Leads incident response for team scope: IC role, coordinates comms, drives resolution, writes postmortems"
    - "Builds observability stack: Prometheus/Grafana/Loki/Tempo; defines SLIs (latency, availability, throughput)"
    - "Implements chaos engineering experiments (Litmus/Chaos Mesh); runs monthly game days"
    - "Automates toil: self-healing systems, auto-remediation, runbook automation (RunDeck, custom operators)"
    - "Manages Kubernetes clusters: upgrades, node pools, add-ons, security hardening (PSP/OPA/Kyverno)"
    - "Optimizes cloud costs: rightsizing, spot instances, savings plans, FinOps reporting"
    - "Mentors juniors; improves on-call sustainability (pages <2/week, nocturnal <1/week)"
  senior:
    - "Architects organization-wide SLO framework: error budget policy, stakeholder alignment, cross-service dependencies"
    - "Defines reliability standards: incident management process, runbook templates, severity definitions, postmortem culture"
    - "Leads high-severity incidents (SEV-1/2): incident command, cross-team coordination, executive communication"
    - "Drives reliability improvements: chaos engineering program, game days, capacity planning, DR strategy"
    - "Partners with Security/Compliance: supply chain (SBOM, Cosign), runtime (Falco/Tetragon), secrets (Vault/ESO)"
    - "Mentors Senior engineers; grows Staff engineers; defines IC career ladder; raises hiring bar"
    - "Evaluates vendor/build vs buy; influences org strategy; presents to leadership on reliability posture"
  staff:
    - "Defines multi-year reliability strategy: SLO maturity model, platform reliability, developer experience"
    - "Builds SRE/platform team: hiring, structure (SRE vs platform enablement), charter, metrics (adoption, satisfaction)"
    - "Leads high-stakes migrations: Kubernetes version, cloud provider, observability stack, secrets management"
    - "Sets org-wide standards: observability, incident management, on-call, capacity planning, chaos engineering"
    - "Influences C-suite on infrastructure investment; presents to board on reliability risk posture"
    - "Grows Staff+ engineers; defines IC track; industry speaking/writing/open source (CNCF projects)"
    - "Represents engineering in vendor negotiations; M&A infrastructure due diligence"
  principal:
    - "Company-wide reliability/technology vision; long-term architectural roadmap for resilience"
    - "Industry recognition: keynotes, CNCF projects, standards bodies, open source leadership"
    - "Crisis leadership: major outages, security incidents, regulatory response"
    - "Builds engineering culture at scale: reliability mindset, you-build-it-you-run-it, cognitive load reduction"
ats_weight_hints:
  must_have:
    - "SRE"
    - "Site Reliability Engineering"
    - "SLO"
    - "SLI"
    - "Error Budget"
    - "Incident Response"
    - "On-Call"
    - "Runbooks"
    - "Blameless Postmortems"
    - "Prometheus"
    - "Grafana"
    - "Alertmanager"
    - "PagerDuty"
    - "Kubernetes"
    - "Docker"
    - "Go"
    - "Python"
    - "Linux"
    - "AWS"
    - "Terraform"
    - "Observability"
    - "Chaos Engineering"
  strong_signal:
    - "GCP"
    - "Bash"
    - "GitOps"
    - "ArgoCD"
    - "Flux"
    - "Distributed Tracing"
    - "OpenTelemetry"
    - "Tempo"
    - "Jaeger"
    - "Loki"
    - "Capacity Planning"
    - "Disaster Recovery"
    - "RTO"
    - "RPO"
    - "FinOps"
    - "Cost Optimization"
    - "SRE Practices"
    - "Multi-Cloud"
  nice_to_have:
    - "Rust"
    - "TypeScript"
    - "Karpenter"
    - "Cluster API"
    - "Temporal"
    - "Dagster"
    - "dbt"
    - "Iceberg"
    - "Delta Lake"
    - "SLSA"
    - "Sigstore"
    - "eBPF"
    - "Cilium Tetragon"
    - "KubeVirt"
ats_parser_hints:
  greenhouse:
    - "sre"
    - "site reliability engineering"
    - "slo"
    - "sli"
    - "error budget"
    - "incident response"
    - "on-call"
    - "runbooks"
    - "blameless postmortems"
    - "prometheus"
    - "grafana"
    - "alertmanager"
    - "pagerduty"
    - "kubernetes"
    - "docker"
    - "go"
    - "python"
    - "linux"
    - "aws"
    - "terraform"
    - "observability"
    - "chaos engineering"
  lever:
    - "sre"
    - "site reliability"
    - "slo"
    - "sli"
    - "error budget"
    - "incident response"
    - "on-call"
    - "runbooks"
    - "postmortems"
    - "prometheus"
    - "grafana"
    - "alertmanager"
    - "pagerduty"
    - "kubernetes"
    - "docker"
    - "go"
    - "python"
    - "linux"
    - "aws"
    - "terraform"
    - "observability"
    - "chaos engineering"
  workday:
    - "Site Reliability Engineering"
    - "Service Level Objective"
    - "Service Level Indicator"
    - "Error Budget"
    - "Incident Response"
    - "On-Call"
    - "Runbooks"
    - "Blameless Postmortems"
    - "Prometheus"
    - "Grafana"
    - "Alertmanager"
    - "PagerDuty"
    - "Kubernetes"
    - "Docker"
    - "Go"
    - "Python"
    - "Linux"
    - "Amazon Web Services"
    - "Terraform"
    - "Observability"
    - "Chaos Engineering"
  icims:
    skill_clusters:
      sre_core: ["SRE", "SLO", "SLI", "Error Budget", "Incident Response", "On-Call", "Runbooks", "Postmortems"]
      observability: ["Prometheus", "Grafana", "Loki", "Tempo", "OpenTelemetry", "Alertmanager", "PagerDuty"]
      kubernetes: ["Kubernetes", "EKS", "GKE", "AKS", "Helm", "Kustomize", "ArgoCD", "Flux", "Operators"]
      cloud: ["AWS", "GCP", "Azure", "Terraform", "Pulumi", "CDK", "CloudFormation"]
      automation: ["Go", "Python", "Bash", "Ansible", "Linux", "Networking", "Security"]
      reliability: ["Chaos Engineering", "Game Days", "Capacity Planning", "Disaster Recovery", "FinOps"]
  taleo:
    keywords: "SRE, Site Reliability, SLO, SLI, Kubernetes, Docker, AWS, Go, Python, Prometheus, Grafana, Incident, On-Call, Terraform, Linux, Monitoring, Alerting, Automation, Cloud, Reliability, Chaos, Engineering"
    boolean: "(\"SRE\" OR \"Site Reliability\") AND (\"Kubernetes\" OR \"K8s\" OR \"EKS\" OR \"GKE\") AND (\"Prometheus\" OR \"Grafana\" OR \"Observability\") AND (\"Go\" OR \"Python\" OR \"Bash\") AND (\"AWS\" OR \"GCP\" OR \"Azure\") AND (\"Incident Response\" OR \"On-Call\" OR \"Runbooks\")"
---
## Role Summary

> **Site Reliability Engineer (SRE)** — Applies software engineering principles to operations: defines SLOs, manages error budgets, builds automation to eliminate toil, and owns production reliability. Bridges development and operations. At Senior+ defines organizational reliability standards; at Staff+ sets company-wide SRE strategy and builds the SRE team.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### SLOs & Error Budgets (All Levels)
- Define and maintain **SLOs/SLIs** for critical services: **latency (p50/p95/p99)**, **availability**, **throughput**, **correctness**, **freshness**
- Implement **error budget policy**: **multi-window multi-burn-rate alerting**, stakeholder alignment, error budget consumption tracking
- Build **SLO dashboards** (Grafana) with **burn rate visualization**, **error budget remaining**, **SLO compliance trends**
- Partner with **Product/Engineering** on **SLO targets**; negotiate **reliability vs. velocity** trade-offs

### Incident Response & On-Call (All Levels)
- Lead **incident response** using **Incident Command System (ICS)**: **IC**, **Comms**, **Scribe** roles; **SEV-1/2/3** severity levels
- Maintain **executable runbooks**: versioned, tested, automated remediation where possible; **runbook automation** (RunDeck, custom operators)
- Conduct **blameless postmortems**: timeline reconstruction, root cause analysis (5 Whys), contributing factors, action items with owners/dates
- Design **sustainable on-call**: rotation design, handoff procedures, compensation, **pages <2/week**, **nocturnal <1/week**

### Observability Stack (Mid+)
- Build **metrics pipeline**: **Prometheus** (PromQL, recording/alerting rules, federation, Thanos/Mimir/Cortex), **OpenTelemetry Collector**
- Implement **structured logging**: **Loki**, **Elasticsearch/OpenSearch**, **Vector/Fluent Bit** (JSON, labels, sampling, retention)
- Deploy **distributed tracing**: **Tempo**, **Jaeger**, **Zipkin** (OpenTelemetry, W3C TraceContext, tail-based sampling)
- Create **Grafana dashboards**: provisioning, templating, SLO panels, business metrics, **SLI/SLO compliance views**

### Reliability Engineering (Senior+)
- Run **chaos engineering** program: **Litmus**, **Chaos Mesh**, **Gremlin** (pod kill, network latency, CPU stress, disk fill, clock skew)
- Execute **game days**: hypothesis-driven, cross-team coordination, learning-focused, action item tracking
- Perform **capacity planning**: demand forecasting, headroom calculation, **autoscaling** (HPA/VPA/Cluster Autoscaler/Karpenter), **load testing** (k6/Gatling)
- Design **disaster recovery**: **RPO/RTO**, backup/restore (Velero, etcd), cross-region failover, **DR drills**

### Automation & Tooling (All Levels)
- Develop **reliability tooling** in **Go/Python/Bash**: CLI tools (Cobra/Click/Typer), operators (controller-runtime), self-healing systems
- Build **toil elimination**: auto-remediation, certificate rotation, log cleanup, backup verification, dependency updates
- Implement **GitOps** for reliability configs: **ArgoCD/Flux**, app-of-apps, progressive delivery (Argo Rollouts/Flagger)

### Platform & Infrastructure (Mid+)
- Operate **Kubernetes** at scale: control plane upgrades, node lifecycle, CNI/CSI, Ingress/Gateway API, admission controllers
- Harden **security**: Pod Security Standards, Network Policies, **mTLS** (Istio/Cilium/Linkerd), **OPA/Gatekeeper/Kyverno**, **Falco/Tetragon**
- Manage **cloud infrastructure**: **AWS/GCP/Azure** via **Terraform/Pulumi/CDK**; multi-account, multi-region, landing zones

### Strategy & Leadership (Staff+)
- Define **multi-year SRE strategy**: SLO maturity model, platform reliability, developer experience, team structure
- Build **SRE organization**: hiring, charter (SRE vs. platform enablement), metrics (adoption, satisfaction, lead time)
- Lead **high-stakes migrations**: Kubernetes versions, cloud providers, observability stacks, secrets management
- Set **org-wide standards**: observability, incident management, on-call, capacity planning, chaos engineering
- Influence **C-suite** on reliability investment; present to **board** on risk posture

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
- **SRE**, **Site Reliability Engineering**, **SLO**, **SLI**, **Error Budget**
- **Incident Response**, **On-Call**, **Runbooks**, **Blameless Postmortems**
- **Prometheus**, **Grafana**, **Alertmanager**, **PagerDuty** (or Opsgenie)
- **Kubernetes**, **Docker**, **Linux**, **AWS** (or GCP/Azure)
- **Go**, **Python**, **Bash**, **Terraform**
- **Observability**, **Chaos Engineering**, **GitOps**

### Strong Signal (Differentiators)
- **Distributed Tracing** (Tempo/Jaeger/Zipkin), **OpenTelemetry**, **Loki**
- **ArgoCD/Flux**, **GitOps**, **Progressive Delivery** (Argo Rollouts/Flagger)
- **Capacity Planning**, **Disaster Recovery**, **RTO/RPO**, **FinOps**
- **Multi-Cloud**, **Service Mesh** (Istio/Cilium/Linkerd), **Security Hardening**
- **Kubernetes Internals** (control plane, CNI, CSI, operators)

### Nice-to-Have (Specialization)
- **Rust**, **TypeScript**, **Karpenter**, **Cluster API**, **Temporal/Dagster**
- **eBPF/Cilium Tetragon**, **KubeVirt**, **SLSA/Sigstore**, **Supply Chain Security**

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Junior (0-2 yrs)
- **Participated** in **on-call rotation** (shadowing); **updated** **runbooks** for **top 10 alerts**
- **Debugged** **production incidents**: analyzed **logs/metrics/traces**; **escalated** appropriately; **MTTR <30min** for SEV-3
- **Wrote** **Python/Go automation** for **toil reduction**: **certificate rotation**, **log cleanup**, **backup verification**
- **Maintained** **Grafana dashboards**; **added alerts** for **5+ services**; **reduced alert noise 20%**
- **Contributed** to **postmortems**: documented **timeline**, identified **3+ action items** per incident

### Mid (2-5 yrs)
- **Owned** **SLO/SLI definitions** for **10+ services**; **implemented burn-rate alerting**; **error budget reviews** weekly
- **Led** **incident response** (IC role) for **team scope**: **coordinated 5+ engineers**, **resolved SEV-2 in <1hr**, **postmortem within 48hrs**
- **Built** **observability stack**: **Prometheus/Grafana/Loki/Tempo**; **defined SLIs** (latency, availability, throughput) for **20 services**
- **Implemented** **chaos experiments** (Litmus/Chaos Mesh): **pod kill**, **network latency**, **CPU stress**; **monthly game days**
- **Automated** **toil elimination**: **self-healing** (K8s operator), **runbook automation** (RunDeck), **certificate management** (cert-manager)
- **Managed** **Kubernetes clusters** (EKS/GKE): **upgrades**, **node pools**, **add-ons**, **OPA/Kyverno policies**
- **Optimized** **cloud spend 25%** via **right-sizing**, **spot instances**, **Savings Plans**, **FinOps dashboard**
- **Mentored** **2 juniors**; **improved on-call sustainability**: **pages 5→1/week**, **nocturnal 2→0/week**

### Senior (5-8 yrs)
- **Architected** **org-wide SLO framework**: **error budget policy**, **stakeholder alignment**, **cross-service dependency mapping**
- **Defined** **reliability standards**: **incident management process**, **runbook templates**, **severity definitions**, **postmortem culture**
- **Commanded** **high-severity incidents** (SEV-1/2): **cross-team coordination**, **executive communication**, **customer updates**
- **Drove** **reliability program**: **chaos engineering** (quarterly game days), **capacity planning**, **DR strategy** (RTO <1hr, RPO <5min)
- **Partnered** with **Security** on **supply chain** (SBOM, Cosign), **runtime** (Falco/Tetragon), **secrets** (Vault/ESO)
- **Mentored** **Senior engineers**; **grew Staff engineers**; **defined IC career ladder**; **raised hiring bar**
- **Evaluated** **vendor/build vs buy**; **influenced org strategy**; **presented to leadership** on **reliability posture**

### Staff (8-12 yrs)
- **Defined** **5-year reliability strategy**: **SLO maturity model**, **platform reliability**, **developer experience**, **team structure**
- **Built** **SRE organization** (20 engineers): **charter**, **metrics** (adoption, satisfaction, lead time), **enablement model**
- **Led** **high-stakes migrations**: **EKS 1.27→1.29**, **Datadog → Grafana Cloud**, **HashiCorp Vault → AWS Secrets Manager**
- **Set** **org-wide standards**: **observability** (OpenTelemetry), **incident management** (ICS), **on-call** (sustainable), **chaos engineering**
- **Influenced** **C-suite** on **infrastructure investment** ($50M+); **presented to board** on **reliability risk posture**
- **Grew** **Staff+ cohort** 3→12; **industry speaking** (SREcon, KubeCon, AWS re:Invent); **CNCF project maintainer**

### Principal (12+ yrs)
- **Company-wide reliability vision**; **10-year technology roadmap** for **resilience**, **scale**, **cost efficiency**
- **Industry recognition**: **CNCF Ambassador**, **SREcon Keynote**, **Standards Bodies**, **OSS Leadership** (Prometheus, OpenTelemetry, Kubernetes)
- **Crisis leadership**: **major outage command**, **security incident response**, **regulatory engagement**
- **Transformed engineering culture**: **reliability mindset**, **you-build-it-you-run-it**, **cognitive load reduction** at scale

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `sre`, `site reliability engineering`, `slo`, `sli`, `error budget`, `incident response`, `on-call`, `runbooks`, `blameless postmortems`, `prometheus`, `grafana`, `alertmanager`, `pagerduty`, `kubernetes`, `docker`, `go`, `python`, `linux`, `aws`, `terraform`, `observability`, `chaos engineering`
**Stemming**: `incident`→`incidents`/`incident response`, `automat`→`automated`/`automation`, `observ`→`observability`/`observable`
**Fuzzy**: `sre`≈`site reliability`, `k8s`≈`kubernetes`, `tf`≈`terraform`, `argocd`≈`argo cd`, `slo`≈`service level objective`, `mimir`≈`thanos`≈`cortex`

### Lever
**Exact**: `sre`, `site reliability`, `slo`, `sli`, `error budget`, `incident response`, `on-call`, `runbooks`, `postmortems`, `prometheus`, `grafana`, `alertmanager`, `pagerduty`, `kubernetes`, `docker`, `go`, `python`, `linux`, `aws`, `terraform`, `observability`, `chaos engineering`
**Normalization**: `site reliability engineering`→`sre`, `prometheus operator`→`prometheus`, `kubernetes operator`→`operator pattern`, `multi window multi burn rate`→`burn rate alerting`

### Workday
**Exact (title case)**: `Site Reliability Engineering`, `Service Level Objective`, `Service Level Indicator`, `Error Budget`, `Incident Response`, `On-Call`, `Runbooks`, `Blameless Postmortems`, `Prometheus`, `Grafana`, `Alertmanager`, `PagerDuty`, `Kubernetes`, `Docker`, `Go`, `Python`, `Linux`, `Amazon Web Services`, `Terraform`, `Observability`, `Chaos Engineering`
**Compound**: `Amazon EKS`, `Google GKE`, `Azure AKS`, `AWS CloudWatch`, `Google Cloud Monitoring`, `Azure Monitor`

### iCIMS
**Skill clusters**:
```
sre_core: ["SRE", "SLO", "SLI", "Error Budget", "Incident Response", "On-Call", "Runbooks", "Postmortems"]
observability: ["Prometheus", "Grafana", "Loki", "Tempo", "OpenTelemetry", "Alertmanager", "PagerDuty"]
kubernetes: ["Kubernetes", "EKS", "GKE", "AKS", "Helm", "Kustomize", "ArgoCD", "Flux", "Operators"]
cloud: ["AWS", "GCP", "Azure", "Terraform", "Pulumi", "CDK", "CloudFormation"]
automation: ["Go", "Python", "Bash", "Ansible", "Linux", "Networking", "Security"]
reliability: ["Chaos Engineering", "Game Days", "Capacity Planning", "Disaster Recovery", "FinOps"]
```
**Weighting**: sre_core (0.25) + observability (0.2) + kubernetes (0.15) + cloud (0.15) + automation (0.15) + reliability (0.1)

### Taleo
**Keywords**: `SRE`, `Site Reliability`, `SLO`, `SLI`, `Kubernetes`, `Docker`, `AWS`, `Go`, `Python`, `Prometheus`, `Grafana`, `Incident`, `On-Call`, `Terraform`, `Linux`, `Monitoring`, `Alerting`, `Automation`, `Cloud`, `Reliability`, `Chaos`, `Engineering`
**Boolean**: `("SRE" OR "Site Reliability") AND ("Kubernetes" OR "K8s" OR "EKS" OR "GKE") AND ("Prometheus" OR "Grafana" OR "Observability") AND ("Go" OR "Python" OR "Bash") AND ("AWS" OR "GCP" OR "Azure") AND ("Incident Response" OR "On-Call" OR "Runbooks")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: SRE Team in Scale-Up / Cloud-Native Company (Series B-D, 100-500 eng)
**Keywords**: `sre`, `slo`, `error budget`, `incident response`, `on-call`, `prometheus`, `grafana`, `kubernetes`, `aws`, `terraform`, `chaos engineering`, `game days`, `toil elimination`, `automation`, `go`, `python`, `observability`, `runbooks`, `postmortems`, `capacity planning`
**Mirror**: Lead with **SLO maturity**, **incident metrics** (MTTR, MTTA, postmortem quality), **toil reduction**. Use `defined`, `implemented`, `automated`, `reduced`, `improved`. Emphasize **sustainable on-call**, **blameless culture**, **error budget governance**.

### Archetype 2: Enterprise / Regulated SRE (FinTech, HealthTech, GovCloud)
**Keywords**: `compliance`, `soc2`, `pci-dss`, `hipaa`, `fedramp`, `audit`, `evidence`, `policy as code`, `opa`, `kyverno`, `disaster recovery`, `rto`, `rpo`, `cross-region`, `backup`, `velero`, `landing zone`, `control tower`, `organizations`, `scp`, `guardrails`, `supply chain`, `sbom`, `cosign`, `slsa`, `secrets`, `vault`, `eso`
**Mirror**: Lead with **compliance posture**, **audit readiness**, **governance**. Use `architected`, `enforced`, `standardized`, `audited`, `certified`. Emphasize **risk reduction**, **policy as code**, **DR readiness**, **supply chain security**.

### Archetype 3: Platform SRE / Internal Tools (Big Tech, Platform Companies)
**Keywords**: `platform`, `internal developer platform`, `idp`, `backstage`, `developer experience`, `dx`, `self-service`, `golden paths`, `paved roads`, `scaffolding`, `templates`, `enablement`, `adoption metrics`, `nps`, `lead time`, `deployment frequency`, `change failure rate`, `mttr`, `platform engineering`, `reliability platform`, `service mesh`, `istio`, `cilium`, `gateway api`
**Mirror**: Lead with **platform leverage** (teams onboarded, adoption %, lead time reduction). Use `enabled`, `standardized`, `accelerated`, `measured`, `iterated`. Emphasize **product mindset**, **user research**, **feedback loops**, **platform as product**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `SLO` / `SLI` / `Error Budget` | JD requires SRE; resume has only "monitoring" | Add `SLO/SLI`, `Error Budgets`, `Burn-Rate Alerting`; describe stakeholder alignment |
| `Incident Response` / `Runbooks` / `Postmortems` | Senior+ JD; missing | Add `Incident Command (IC/Comms/Scribe)`, `Blameless Postmortems`, `Runbook Automation` |
| `Prometheus` / `Grafana` / `OpenTelemetry` | JD requires observability; resume has Datadog/CloudWatch only | Add `Prometheus (Mimir/Thanos)`, `Grafana`, `Loki`, `Tempo`, `OpenTelemetry Collector` |
| `Chaos Engineering` / `Game Days` | Staff+ JD; missing | Add `Litmus/Chaos Mesh/Gremlin`, `Game Days`, `Hypothesis-Driven Experiments` |
| `On-Call` / `Sustainable Practices` | JD requires; missing or "24/7" without metrics | Add `On-Call Rotation`, `Pages <2/week`, `Nocturnal <1/week`, `Handoff Procedures` |
| `Capacity Planning` / `Autoscaling` / `Load Testing` | JD requires scale; missing | Add `Demand Forecasting`, `HPA/VPA/Karpenter`, `k6/Gatling`, `Headroom Calculation` |
| `Disaster Recovery` / `RTO` / `RPO` | Enterprise JD; missing | Add `DR Strategy`, `Cross-Region Failover`, `Velero/etcd Backup`, `DR Drills` |
| `Go` / `Python` (automation) | JD requires; resume has only Bash | Add `Go (CLI, Operators)` or `Python (FastAPI, boto3, pytest)`; describe tools built |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| **GitHub: SRE Tooling / Operator / CLI** | `Open Source`, `Go`, `Python`, `Kubernetes`, `Controller-runtime`, `Community`, `Downloads` | Projects, GitHub Link |
| **Technical Blog: SRE / Reliability / Observability** | `Technical Writing`, `SRE`, `SLO`, `Incident Response`, `Chaos Engineering`, `Observability` | Writing, Portfolio Link |
| **Conference Talk (SREcon, KubeCon, Velocity, re:Invent)** | `Public Speaking`, `Thought Leadership`, `SRE`, `Reliability`, `Observability`, `Platform` | Speaking, Leadership |
| **CNCF Project Contribution** | `Open Source`, `CNCF`, `Kubernetes`, `Prometheus`, `OpenTelemetry`, `Argo`, `Envoy`, `Maintainer` | Projects, GitHub Link |
| **Internal Platform Adoption Case Study** | `Platform Engineering`, `Adoption Metrics`, `Developer Productivity`, `Change Management` | Experience, Projects |
| **Incident Postmortem (Sanitized)** | `Incident Response`, `Root Cause Analysis`, `Blameless Culture`, `Action Items`, `Reliability` | Experience, Leadership |

---

## Role-Specific ATS Optimization Notes

### Red Flags (Auto-Reject)
- **No SLO/SLI/Error Budget** → Not SRE, just ops/monitoring
- **Only Datadog/CloudWatch/New Relic** → Vendor lock-in, no open standards (Prometheus/OpenTelemetry)
- **No Incident Command/Runbooks/Postmortems** → Reactive only, no process
- **No Kubernetes** in 2024+ → Immediate filter for SRE
- **No Automation/Toil Elimination** → Manual ops, doesn't scale
- **On-Call described as "firefighting" without metrics** → Unsustainable, no improvement
- **>2 pages for <8 yrs** → Format penalty
- **Tables/columns/graphics** → Parser extraction failure

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `SRE`, `SLO`, `SLI`, `Error Budget`, `Incident Response`, `On-Call`, `Prometheus`, `Grafana`, `Kubernetes`, `Go`, `Python`, `AWS`, `Terraform` |
| High | 1.5% | 3.0% | `Runbooks`, `Postmortems`, `OpenTelemetry`, `Loki`, `Tempo`, `ArgoCD`, `Flux`, `GitOps`, `Chaos Engineering`, `Capacity Planning`, `FinOps` |
| Medium | 1.0% | 2.5% | `GCP`, `Azure`, `Service Mesh`, `Istio`, `Cilium`, `Disaster Recovery`, `RTO`, `RPO`, `Mentoring`, `Architecture Review` |
| Low | 0.5% | 1.5% | `Rust`, `TypeScript`, `Karpenter`, `Cluster API`, `eBPF`, `SLSA`, `Sigstore`, `KubeVirt` |

### NDA Abstraction
- **L2**: "SRE for multi-region Kubernetes platform (50 clusters, 10K+ nodes) on AWS/GCP"
- **L3**: "Reduced MTTR 70% and alert noise 80% via SLO-based alerting and runbook automation"
- **L4**: "Cut incident resolution time 70% and operational overhead 80% through reliability platform"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `devops-platform/sre`
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 10 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for applications, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (MTTR/SLO/incidents), Tech Lead (architecture/automation), Exec (risk/cost/reliability)
- [ ] Metrics validated via `metric_plausibility.py` (MTTR, MTTA, availability %, error budget burn rate, deployment freq, change failure rate, cost savings, pages/week)
- [ ] Portfolio cross-refs: GitHub/blog/talks/CNCF with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024