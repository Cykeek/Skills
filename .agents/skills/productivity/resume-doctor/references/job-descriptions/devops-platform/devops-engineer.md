---
role_id: "devops-platform/devops-engineer"
canonical_title: "DevOps / Platform Engineer"
aliases: ["DevOps Engineer", "Platform Engineer", "Site Reliability Engineer (SRE)", "Cloud Engineer", "Infrastructure Engineer", "Release Engineer"]
seniority_levels: ["Junior", "Mid", "Senior", "Staff", "Principal"]
related_roles: ["sre", "platform-engineer", "cloud-engineer", "infrastructure-engineer", "release-engineer"]
ats_keywords:
  - "AWS"
  - "GCP"
  - "Azure"
  - "Kubernetes"
  - "Docker"
  - "Terraform"
  - "CI/CD"
  - "GitHub Actions"
  - "GitLab CI"
  - "Prometheus"
  - "Grafana"
  - "Linux"
  - "Bash"
  - "Python"
  - "Go"
  - "Helm"
  - "ArgoCD"
  - "Flux"
  - "Observability"
  - "SLO"
  - "SLI"
  - "Incident Response"
  - "On-Call"
  - "Runbooks"
  - "Chaos Engineering"
  - "Cost Optimization"
  - "FinOps"
  - "Security"
  - "Compliance"
  - "IaC"
  - "GitOps"
ats_skills_taxonomy:
  cloud_platforms:
    - "AWS: EC2, ECS/EKS/Fargate, Lambda, RDS/Aurora, ElastiCache, S3, CloudFront, Route53, IAM, Organizations, CloudFormation, CDK, Systems Manager, EventBridge, Step Functions"
    - "GCP: Compute Engine, GKE/Cloud Run, Cloud SQL, Memorystore, Cloud Storage, Cloud CDN, Cloud DNS, IAM, Deployment Manager, Cloud Build, Cloud Logging/Monitoring/Trace"
    - "Azure: VMs, AKS/Container Apps, Functions, Azure SQL, Cache for Redis, Blob Storage, Front Door, DNS, Entra ID, Bicep/ARM, DevOps, Monitor"
    - "Multi-Cloud: Terraform, Pulumi, Crossplane, Cluster API (CAPI), Anthos, Arc"
  container_orchestration:
    - "Kubernetes (EKS/GKE/AKS/On-Prem): Control Plane, Worker Nodes, CNI (Cilium, Calico), CSI, Ingress (NGINX, Traefik, Envoy/Gateway API)"
    - "Helm (Charts, Dependencies, Values, Hooks, Tests), Kustomize (Bases, Overlays, Patches, Generators)"
    - "Operators/Controllers: Operator SDK, Kubebuilder, Controller-runtime (CRDs, Webhooks, Reconciliation)"
    - "Service Mesh: Istio, Linkerd, Cilium (mTLS, Traffic Split, AuthZ, Observability)"
    - "GitOps: ArgoCD, Flux (Image Automation, Policy, Notifications, Multi-tenancy)"
    - "Security: Kyverno, OPA/Gatekeeper, Falco, Trivy, Cosign, Sigstore, Pod Security Standards, Network Policies"
  infrastructure_as_code:
    - "Terraform/OpenTofu: Modules, State (Remote, Locking, Workspaces), Providers, Data Sources, Import, Plan/Apply Automation"
    - "Pulumi: TypeScript/Python/Go/C#/.NET, Automation API, Stack References, Policy as Code (OPA)"
    - "AWS CDK: TypeScript/Python, Constructs (L1/L2/L3), Aspects, Testing (Jest), cdk-nag"
    - "Ansible: Roles, Collections, Molecule Testing, AWX/Controller, Network Automation"
    - "Packer: Builders (AMI, Docker, Azure, GCP), Provisioners (Ansible, Shell), HCP Packer"
  ci_cd:
    - "GitHub Actions: Workflows, Composite Actions, Reusable Workflows, Matrix, Environments, OIDC, Self-Hosted Runners"
    - "GitLab CI: Pipelines, DAG, Child/Parent, DAST/SAST/Container Scanning, Environments, Deploy Boards"
    - "Build: Docker (BuildKit, Buildx, Multi-platform, SBOM, Attestations), Kaniko, Buildpacks (Paketo, Google)"
    - "Test: Unit, Integration, Contract (Pact), E2E, Chaos (Litmus, Chaos Mesh), Performance (k6, Gatling)"
    - "Security: SAST (Semgrep, CodeQL, SonarQube), SCA (Snyk, Dependabot, Trivy, Grype), SBOM (Syft, SPDX, CycloneDX), Signing (Cosign, Sigstore)"
    - "Deploy: ArgoCD/Flux (GitOps), Spinnaker (Pipeline), Harness, Octopus, Custom (Helm + Kubeval/Kubeconform)"
    - "Progressive Delivery: Argo Rollouts, Flagger, Flux Image Automation (Canary, Blue-Green, A/B, Feature Flags)"
  observability:
    - "Metrics: Prometheus (PromQL, Recording/Alerting Rules, Federation, Thanos, Mimir, Cortex), OpenTelemetry Collector"
    - "Logs: Loki, Elasticsearch/OpenSearch, Vector/Fluent Bit/Fluentd (Structured JSON, Labels, Sampling, Retention)"
    - "Traces: Tempo, Jaeger, Zipkin (OpenTelemetry, W3C TraceContext, Sampling, Tail-Based)"
    - "Visualization: Grafana (Dashboards, Alerting, Loki/ Tempo/ Prometheus Data Sources, Provisioning)"
    - "SLO/SLI: SLI Definitions (Latency, Availability, Throughput, Correctness), Error Budgets, Burn Rate Alerting (Multi-Window, Multi-Burn-Rate)"
    - "Alerting: Alertmanager, PagerDuty, Opsgenie, Grafana Alerting (Routes, Inhibition, Silences, Notification Templates)"
    - "RUM/Synthetic: Sentry, Datadog, Grafana Faro, Checkly, k6 Browser (Core Web Vitals, User Journeys)"
  reliability_engineering:
    - "Incident Response: Command Structure (IC, Comms, Scribe), Runbooks, War Rooms, Blameless Postmortems (Timeline, Root Cause, Action Items)"
    - "On-Call: Rotation, Escalation, Handoff, Compensation, Sustainable Practices (Pages <2/week, Nocturnal <1/week)"
    - "Chaos Engineering: Litmus, Chaos Mesh, Gremlin (Fault Injection: Pod Kill, Network Latency, CPU Stress, Disk Fill, Clock Skew)"
    - "Game Days: Planned Exercises, Hypothesis → Experiment → Learning, Cross-Team Coordination"
    - "Capacity Planning: Demand Forecasting, Headroom, Autoscaling (HPA/VPA/Cluster Autoscaler/Karpenter), Load Testing"
    - "Disaster Recovery: RPO/RTO, Backup/Restore (Velero, etcd), Cross-Region Failover, DR Drills"
  security_compliance:
    - "Supply Chain: SBOM (Syft, SPDX/CycloneDX), Signing (Cosign, Sigstore), Verification (Policy Controller, Kyverno), Provenance (SLSA)"
    - "Runtime: Falco, Tetragon (eBPF), Cilium (Network Policy, L7), KubeArmor (AppArmor/SELinux), Admission Control"
    - "Secrets: Vault, AWS Secrets Manager, 1Password, SOPS, SealedSecrets, External Secrets Operator (ESO)"
    - "Compliance: CIS Benchmarks (kube-bench), PCI-DSS, SOC2, HIPAA, FedRAMP, NIST 800-53, Audit Automation"
    - "Identity: OIDC, IRSA/OIDC Providers, SPIFFE/SPIRE, mTLS, Certificate Rotation (cert-manager, Vault PKI)"
  platform_engineering:
    - "Internal Developer Platform (IDP): Backstage, Port, Cortex, Humanitec (Software Catalog, Self-Service, Scorecards, Tech Docs)"
    - "Developer Experience: CLI Tools, Scaffold Templates (Cookiecutter, GitHub Template), Local Dev (Tilt, Garden, DevSpace, Okteto)"
    - "Golden Paths: Paved Roads, Standardized Workflows, Approved Patterns, Migration Guides, Deprecation Policy"
    - "API Platform: Kong, Envoy, AWS API Gateway, GraphQL Federation, Rate Limiting, AuthZ/AuthN, Developer Portal"
    - "Data Platform: Kafka/Flink (Streaming), Airflow/Dagster (Orchestration), dbt (Transform), Iceberg/Delta/Hudi (Lakehouse)"
  programming_automation:
    - "Go: Standard Library, Cobra (CLI), Controller-runtime (Operators), gRPC/Connect, Testing (testify, ginkgo)"
    - "Python: FastAPI/Click/Typer (CLI), Boto3/Pulumi SDK, Pytest, Type Hints (mypy/pyright), Poetry/UV"
    - "Bash/Shell: POSIX, ShellCheck, shfmt, Scripts (Idempotent, Robust, Logging, Error Handling)"
    - "SQL: PostgreSQL (Admin, Tuning, Replication, Backup), ClickHouse (Analytics), SQLite (Embedded)"
seniority_signals:
  junior:
    - "Manages CI/CD pipelines; adds tests, fixes flaky builds"
    - "Provisions cloud resources via Terraform/Console with senior review"
    - "Debugs Kubernetes workloads: logs, events, describe, exec"
    - "Participates in on-call (shadowing); updates runbooks"
    - "Automates repetitive tasks with Bash/Python scripts"
    - "Learns cloud services, networking, security fundamentals"
  mid:
    - "Owns infrastructure modules: Terraform, Helm charts, CI/CD pipelines"
    - "Designs and implements observability: dashboards, alerts, SLOs for team services"
    - "Manages Kubernetes clusters: upgrades, node pools, add-ons, security hardening"
    - "Leads incident response for team scope; writes postmortems; improves runbooks"
    - "Implements GitOps: ArgoCD/Flux, app-of-apps, progressive delivery"
    - "Optimizes cloud costs: right-sizing, spot instances, savings plans, FinOps reporting"
    - "Mentors juniors; conducts code reviews; improves developer experience"
  senior:
    - "Architects platform infrastructure: multi-account, multi-region, landing zones, network topology"
    - "Defines infrastructure standards: modules, policies (OPA/Kyverno), testing, security baselines"
    - "Leads migrations: data center → cloud, monolith → Kubernetes, CI/CD platform switch"
    - "Establishes SLO culture: error budgets, burn rate alerting, stakeholder alignment"
    - "Drives reliability improvements: chaos engineering, game days, capacity planning"
    - "Partners with Security/Compliance: supply chain, runtime, secrets, audit readiness"
    - "Mentors Senior engineers; grows Staff engineers; defines career ladder"
    - "Evaluates vendor/build vs buy; influences org strategy; presents to leadership"
  staff:
    - "Defines multi-year platform strategy: IDP, developer experience, standardization, scale"
    - "Builds platform team: hiring, structure (platform vs. enablement), charter, metrics"
    - "Leads high-stakes migrations: Kubernetes version, cloud provider, CI/CD, secrets management"
    - "Sets org-wide standards: IaC, CI/CD, observability, security, incident management"
    - "Influences C-suite on infrastructure investment; presents to board on reliability/risk"
    - "Grows Staff+ engineers; defines IC track; industry speaking/writing/open source"
    - "Represents engineering in vendor negotiations; M&A infrastructure due diligence"
  principal:
    - "Company-wide infrastructure/technology vision; long-term architectural roadmap"
    - "Industry recognition: keynotes, CNCF projects, standards bodies, open source leadership"
    - "Crisis leadership: major outages, security incidents, regulatory response"
    - "Builds engineering culture at scale; transforms org structure and processes"
ats_weight_hints:
  must_have:
    - "AWS"
    - "Kubernetes"
    - "Docker"
    - "Terraform"
    - "CI/CD"
    - "GitHub Actions"
    - "Prometheus"
    - "Grafana"
    - "Linux"
    - "Bash"
    - "Python"
    - "GitOps"
    - "Helm"
    - "Observability"
    - "SLO"
    - "Incident Response"
    - "On-Call"
    - "Runbooks"
    - "IaC"
  strong_signal:
    - "GCP"
    - "Azure"
    - "ArgoCD"
    - "Flux"
    - "Go"
    - "Pulumi"
    - "Crossplane"
    - "Istio"
    - "Cilium"
    - "Kyverno"
    - "OPA"
    - "Vault"
    - "External Secrets Operator"
    - "Chaos Engineering"
    - "FinOps"
    - "Cost Optimization"
    - "Backstage"
    - "Developer Experience"
    - "Platform Engineering"
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
    - "aws"
    - "kubernetes"
    - "docker"
    - "terraform"
    - "ci/cd"
    - "github actions"
    - "prometheus"
    - "grafana"
    - "linux"
    - "bash"
    - "python"
    - "gitops"
    - "helm"
    - "observability"
    - "slo"
    - "incident response"
    - "on-call"
    - "runbooks"
    - "iac"
  lever:
    - "aws"
    - "kubernetes"
    - "docker"
    - "terraform"
    - "ci/cd"
    - "github actions"
    - "prometheus"
    - "grafana"
    - "linux"
    - "bash"
    - "python"
    - "gitops"
    - "helm"
    - "observability"
    - "slo"
    - "incident response"
    - "on-call"
    - "runbooks"
    - "iac"
  workday:
    - "Amazon Web Services"
    - "Kubernetes"
    - "Docker"
    - "Terraform"
    - "Continuous Integration"
    - "Continuous Deployment"
    - "GitHub Actions"
    - "Prometheus"
    - "Grafana"
    - "Linux"
    - "Bash"
    - "Python"
    - "GitOps"
    - "Helm"
    - "Observability"
    - "Service Level Objective"
    - "Incident Response"
    - "On-Call"
    - "Runbooks"
    - "Infrastructure as Code"
  icims:
    skill_clusters:
      cloud: ["AWS", "EC2", "ECS", "EKS", "Lambda", "RDS", "S3", "CloudFormation", "CDK", "IAM"]
      kubernetes: ["Kubernetes", "EKS", "GKE", "AKS", "Helm", "Kustomize", "ArgoCD", "Flux", "Operators"]
      iac: ["Terraform", "Pulumi", "AWS CDK", "Ansible", "Packer", "Crossplane", "GitOps"]
      cicd: ["GitHub Actions", "GitLab CI", "Jenkins", "Argo Rollouts", "Flagger", "Buildpacks", "SBOM"]
      observability: ["Prometheus", "Grafana", "Loki", "Tempo", "OpenTelemetry", "SLO", "Alertmanager", "PagerDuty"]
      reliability: ["Incident Response", "On-Call", "Runbooks", "Chaos Engineering", "Game Days", "Capacity Planning", "DR"]
      security: ["Vault", "Secrets", "OPA", "Kyverno", "Falco", "Cosign", "SBOM", "SLSA", "mTLS", "SPIFFE"]
      platform: ["Backstage", "Developer Experience", "Self-Service", "Golden Paths", "API Gateway", "Data Platform"]
---
## Role Summary

> **DevOps / Platform Engineer** — Builds and operates the infrastructure, pipelines, and tooling that enable product teams to ship safely and quickly. Owns the "path to production": CI/CD, Kubernetes, observability, security, developer experience. Bridges development and operations. At Senior+ designs platform architecture and standards; at Staff+ defines platform strategy and builds the platform team.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### Infrastructure & Cloud (All Levels)
- Provision and manage **cloud infrastructure** (AWS/GCP/Azure) via **Terraform/OpenTofu/Pulumi/CDK**: modules, workspaces, state locking, drift detection, policy enforcement (OPA/Kyverno)
- Operate **Kubernetes clusters** (EKS/GKE/AKS/On-Prem): control plane upgrades, node lifecycle, CNI/CSI, Ingress/Gateway API, admission controllers, cluster autoscaler (Karpenter)
- Implement **GitOps** (ArgoCD/Flux): app-of-apps, multi-cluster, progressive delivery (Argo Rollouts/Flagger), image automation, policy-as-code
- Harden **security**: Pod Security Standards, Network Policies, mTLS (Istio/Cilium/Linkerd), OPA/Gatekeeper/Kyverno, Falco/Tetragon, Cosign/Sigstore, Vault/ESO

### CI/CD & Developer Experience (All Levels)
- Build and maintain **CI/CD pipelines** (GitHub Actions/GitLab CI): reusable workflows, matrix builds, OIDC auth, self-hosted runners, caching, test parallelization
- Containerize applications: **Docker** (multi-stage, BuildKit, distroless, SBOM, Cosign signing, multi-arch), Buildpacks, Kaniko
- Enable **developer self-service**: Backstage/Port/Cortex (software catalog, scaffolder, tech docs, scorecards), CLI tools, local dev (Tilt/Garden/DevSpace)
- Define **golden paths**: standardized templates, approved patterns, migration guides, deprecation policy, adoption metrics

### Observability & Reliability (Mid+)
- Establish **observability stack**: Prometheus (Mimir/Thanos/Cortex), Loki, Tempo, Grafana, OpenTelemetry Collector (receivers, processors, exporters)
- Define and enforce **SLOs/SLIs**: latency, availability, throughput, correctness; **error budgets**, **multi-window multi-burn-rate alerting**
- Lead **incident response**: IC/Comms/Scribe roles, runbooks, blameless postmortems (timeline, root cause, action items, follow-up tracking)
- Run **chaos engineering** (Litmus/Chaos Mesh/Gremlin) and **game days**: hypothesis-driven, cross-team, learning-focused
- Plan **capacity**: demand forecasting, headroom, autoscaling (HPA/VPA/Cluster Autoscaler/Karpenter), load testing (k6/Gatling)

### Platform Strategy & Leadership (Senior+)
- Architect **landing zones**: multi-account, multi-region, network (Transit Gateway, VPC Lattice, Service Connect), identity (IAM/OIDC/IRSA), guardrails (SCP, Config Rules)
- Build **Internal Developer Platform (IDP)**: Backstage + plugins, self-service provisioning, ephemeral environments, API platform (Kong/Envoy/Gateway API)
- Drive **cost optimization (FinOps)**: rightsizing, spot/EC2 Fleet, Savings Plans, commitment management, showback/chargeback, anomaly detection
- Set **org-wide standards**: IaC style, CI/CD patterns, observability baselines, security baselines, incident management process
- Mentor **Senior+ engineers**; grow **Staff+**; define **career ladder**; raise **hiring bar**

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
- **AWS** (or GCP/Azure), **Kubernetes**, **Docker**, **Terraform**
- **CI/CD** (GitHub Actions preferred), **GitOps** (ArgoCD/Flux)
- **Prometheus**, **Grafana**, **Observability**, **SLO**, **SLI**
- **Linux**, **Bash**, **Python** (or Go), **Helm**, **IaC**
- **Incident Response**, **On-Call**, **Runbooks**

### Strong Signal (Differentiators)
- **ArgoCD/Flux**, **Go**, **Pulumi/Crossplane**, **Istio/Cilium**, **Kyverno/OPA**
- **Vault/External Secrets Operator**, **Chaos Engineering**, **FinOps**, **Cost Optimization**
- **Backstage/Developer Experience**, **Platform Engineering**, **SRE Practices**
- **Multi-Cloud**, **Disaster Recovery**, **Supply Chain Security (SLSA/Sigstore)**

### Nice-to-Have (Specialization)
- **Rust**, **TypeScript**, **Karpenter**, **Cluster API**, **Temporal/Dagster**, **dbt/Iceberg/Delta Lake**
- **eBPF/Cilium Tetragon**, **KubeVirt**, **Service Mesh (Istio/Linkerd)**, **API Gateway (Kong/Envoy)**

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Junior (0-2 yrs)
- **Automated** **CI/CD pipelines** reducing build time **40%** via caching and parallelization
- **Provisioned** **AWS resources** (EC2, RDS, S3) using **Terraform modules** with senior review
- **Debugged** **Kubernetes pods**: analyzed logs, events, resource limits; resolved **OOMKilled/CrashLoopBackOff**
- **Wrote** **Bash/Python scripts** for **toil reduction**: backup rotation, log cleanup, certificate renewal
- **Participated** in **on-call rotation** (shadowing); **updated** **runbooks** for common alerts

### Mid (2-5 yrs)
- **Owned** **Terraform modules** (VPC, EKS, RDS, IAM) used by **10+ teams**; enforced **policy-as-code** (OPA)
- **Implemented** **GitOps** (ArgoCD) for **50+ applications**; **app-of-apps**, **progressive delivery** (canary via Argo Rollouts)
- **Built** **observability stack**: Prometheus/Grafana/Loki/Tempo; **defined SLOs** for **15 services**; **burn-rate alerting**
- **Led** **incident response** for **team scope**: IC role, **postmortems** with **actionable fixes**, **MTTR reduced 50%**
- **Optimized** **cloud spend** **30%** via **right-sizing**, **spot instances**, **Savings Plans**, **FinOps dashboard**
- **Mentored** **2 juniors**; **improved** **DX**: scaffold templates, local dev environment, **self-service docs**

### Senior (5-8 yrs)
- **Architected** **multi-account AWS landing zone** (Control Tower, Organizations, SCP, Config, Security Hub) for **100+ accounts**
- **Defined** **platform standards**: **Terraform style guide**, **Helm chart template**, **CI/CD workflow library**, **security baselines**
- **Led** **Kubernetes migration** (EC2 → EKS, **200+ services**, **zero-downtime**, **6-month timeline**, **$2M cost avoidance**)
- **Established** **SLO culture**: **error budget policy**, **stakeholder reviews**, **burn-rate alerting** org-wide
- **Drove** **reliability program**: **chaos engineering** (monthly game days), **capacity planning**, **DR drills** (RTO <1hr, RPO <5min)
- **Partnered** with **Security** on **supply chain**: **SBOM**, **Cosign signing**, **Kyverno policies**, **SOC2 evidence automation**
- **Mentored** **Senior engineers**; **grew** **Staff engineers**; **defined** **IC career ladder**; **hiring bar**

### Staff (8-12 yrs)
- **Defined** **5-year platform strategy**: **IDP (Backstage)**, **golden paths**, **self-service infra**, **developer productivity metrics**
- **Built** **platform team** (15 engineers): **charter**, **metrics** (adoption, satisfaction, lead time), **enablement model**
- **Led** **high-stakes migrations**: **EKS 1.27→1.29**, **GitHub Enterprise → GitHub Actions**, **HashiCorp Vault → AWS Secrets Manager**
- **Set** **org-wide standards**: **IaC (Terraform)**, **CI/CD (GitHub Actions)**, **Observability (Grafana Cloud)**, **Security (Kyverno)**
- **Influenced** **C-suite** on **infrastructure investment** ($50M+); **presented** to **board** on **reliability risk posture**
- **Grew** **Staff+ cohort** 3→10; **industry speaking** (KubeCon, SREcon, AWS re:Invent); **CNCF project maintainer**

### Principal (12+ yrs)
- **Company-wide infrastructure vision**; **10-year technology roadmap**; **competitive differentiation** via platform
- **Industry recognition**: **CNCF Ambassador**, **KubeCon Keynote**, **Standards Bodies** (CNI, CSI, Gateway API), **OSS Leadership**
- **Crisis leadership**: **major outage command**, **security incident response**, **regulatory engagement**
- **Transformed** **engineering culture**: **platform thinking**, **you build it you run it**, **cognitive load reduction** at scale

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `aws`, `kubernetes`, `docker`, `terraform`, `ci/cd`, `github actions`, `prometheus`, `grafana`, `linux`, `bash`, `python`, `gitops`, `helm`, `observability`, `slo`, `incident response`, `on-call`, `runbooks`, `iac`
**Stemming**: `automat`→`automated`/`automating`/`automation`, `migrat`→`migrated`/`migrating`/`migration`, `optimiz`→`optimized`/`optimizing`
**Fuzzy**: `k8s`≈`kubernetes`, `tf`≈`terraform`, `gha`≈`github actions`, `argocd`≈`argo cd`, `slo`≈`service level objective`

### Lever
**Exact**: `aws`, `kubernetes`, `docker`, `terraform`, `ci/cd`, `github actions`, `prometheus`, `grafana`, `linux`, `bash`, `python`, `gitops`, `helm`, `observability`, `slo`, `incident response`, `on-call`, `runbooks`, `iac`
**Normalization**: `amazon web services`→`aws`, `google cloud platform`→`gcp`, `azure kubernetes service`→`aks`, `elastic kubernetes service`→`eks`

### Workday
**Exact (title case)**: `Amazon Web Services`, `Kubernetes`, `Docker`, `Terraform`, `Continuous Integration`, `Continuous Deployment`, `GitHub Actions`, `Prometheus`, `Grafana`, `Linux`, `Bash`, `Python`, `GitOps`, `Helm`, `Observability`, `Service Level Objective`, `Incident Response`, `On-Call`, `Runbooks`, `Infrastructure as Code`

### iCIMS
**Skill clusters**:
```
cloud: ["AWS", "EC2", "ECS", "EKS", "Lambda", "RDS", "S3", "CloudFormation", "CDK", "IAM"]
kubernetes: ["Kubernetes", "EKS", "GKE", "AKS", "Helm", "Kustomize", "ArgoCD", "Flux", "Operators"]
iac: ["Terraform", "Pulumi", "AWS CDK", "Ansible", "Packer", "Crossplane", "GitOps"]
cicd: ["GitHub Actions", "GitLab CI", "Jenkins", "Argo Rollouts", "Flagger", "Buildpacks", "SBOM"]
observability: ["Prometheus", "Grafana", "Loki", "Tempo", "OpenTelemetry", "SLO", "Alertmanager", "PagerDuty"]
reliability: ["Incident Response", "On-Call", "Runbooks", "Chaos Engineering", "Game Days", "Capacity Planning", "DR"]
security: ["Vault", "Secrets", "OPA", "Kyverno", "Falco", "Cosign", "SBOM", "SLSA", "mTLS", "SPIFFE"]
platform: ["Backstage", "Developer Experience", "Self-Service", "Golden Paths", "API Gateway", "Data Platform"]
```
**Weighting**: cloud (0.2) + kubernetes (0.2) + iac (0.15) + cicd (0.15) + observability (0.1) + reliability (0.1) + security (0.05) + platform (0.05)

### Taleo
**Keywords**: `AWS`, `Kubernetes`, `Docker`, `Terraform`, `Jenkins`, `GitLab`, `GitHub`, `CI/CD`, `Linux`, `Bash`, `Python`, `Go`, `Ansible`, `Prometheus`, `Grafana`, `Elasticsearch`, `Monitoring`, `Alerting`, `Incident`, `On-Call`, `Scripting`, `Automation`, `Cloud`, `Infrastructure`, `DevOps`, `Agile`, `Scrum`
**Boolean**: `("AWS" OR "Amazon Web Services") AND ("Kubernetes" OR "K8s" OR "EKS" OR "GKE" OR "AKS") AND ("Terraform" OR "CloudFormation" OR "Pulumi") AND ("CI/CD" OR "Continuous Integration" OR "GitHub Actions" OR "GitLab CI") AND ("Prometheus" OR "Grafana" OR "Monitoring" OR "Observability")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: Cloud-Native Startup / Scale-Up (Series B-D, 50-500 eng)
**Keywords**: `aws`, `kubernetes`, `terraform`, `github actions`, `argo cd`, `prometheus`, `grafana`, `on-call`, `incident response`, `cost optimization`, `finops`, `developer experience`, `self-service`, `golden paths`, `backstage`, `scaling`, `reliability`, `chaos engineering`, `game days`
**Mirror**: Lead with **scale metrics** (clusters, services, deploys/day, MTTR). Use `built`, `scaled`, `automated`, `optimized`. Emphasize **pragmatism**, **velocity + safety**, **developer empathy**.

### Archetype 2: Enterprise / Regulated (FinTech, HealthTech, GovCloud, Large Corp)
**Keywords**: `compliance`, `soc2`, `pci-dss`, `hipaa`, `fedramp`, `landing zone`, `control tower`, `organizations`, `scp`, `config`, `security hub`, `guardduty`, `vault`, `secrets`, `opa`, `kyverno`, `falco`, `sbom`, `cosign`, `slsa`, `supply chain`, `audit`, `evidence`, `policy as code`, `multi-account`, `multi-region`, `disaster recovery`, `rto`, `rpo`
**Mirror**: Lead with **compliance posture**, **security hardening**, **governance**. Use `architected`, `enforced`, `standardized`, `audited`, `certified`. Emphasize **risk reduction**, **audit readiness**, **policy as code**.

### Archetype 3: Platform Team / Internal Tools (Big Tech, Platform Companies)
**Keywords**: `internal developer platform`, `idp`, `backstage`, `port`, `cortex`, `humanitec`, `self-service`, `developer experience`, `dx`, `cognitive load`, `golden paths`, `paved roads`, `scaffolding`, `templates`, `cli`, `api platform`, `kong`, `envoy`, `gateway api`, `service mesh`, `istio`, `cilium`, `platform engineering`, `enablement`, `adoption metrics`, `nps`, `lead time`, `deployment frequency`, `change failure rate`, `mttr`
**Mirror**: Lead with **platform leverage** (teams onboarded, adoption %, lead time reduction). Use `enabled`, `standardized`, `accelerated`, `measured`, `iterated`. Emphasize **product mindset**, **user research**, **feedback loops**, **platform as product**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `Kubernetes` / `EKS` / `GKE` | JD requires; resume has `Docker` only | Add `Kubernetes (EKS/GKE)`, `Helm`, `Kustomize`, `ArgoCD/Flux`; describe cluster ops |
| `Terraform` / `Pulumi` / `CDK` | JD requires IaC; resume has `CloudFormation`/`Console` | Add `Terraform`/`OpenTofu`; describe modules, state, testing, policy |
| `GitOps` / `ArgoCD` / `Flux` | JD requires; resume has manual `kubectl apply` | Add `GitOps (ArgoCD/Flux)`, `App-of-Apps`, `Progressive Delivery`; cite deployment frequency |
| `Prometheus` / `Grafana` / `SLO` | JD requires observability; resume has `CloudWatch`/`Datadog` only | Add `Prometheus (Mimir/Thanos)`, `Grafana`, `Loki`, `Tempo`, `SLO/SLI`, `Burn-Rate Alerting` |
| `Incident Response` / `Runbooks` / `Postmortems` | Senior+ JD; missing | Add `Incident Command`, `Blameless Postmortems`, `Runbook Automation`, `MTTR Reduction` |
| `FinOps` / `Cost Optimization` | JD requires; missing | Add `FinOps`, `Right-Sizing`, `Spot/Savings Plans`, `Kubecost/Cloudability`, `Showback/Chargeback` |
| `Go` / `Python` (automation) | JD requires; resume has only `Bash` | Add `Go` (CLI, Operators) or `Python` (Boto3, Pulumi, FastAPI); describe tools built |
| `Backstage` / `Developer Experience` | Platform JD; missing | Add `Backstage`/`Port`/`Cortex`, `Software Catalog`, `Scaffolder`, `TechDocs`, `Scorecards` |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| **GitHub: Terraform Modules / Helm Charts** | `Open Source`, `Terraform`, `Helm`, `Module`, `Registry`, `Downloads` | Projects, GitHub Link |
| **Technical Blog: Platform Engineering** | `Technical Writing`, `Platform Engineering`, `Developer Experience`, `GitOps`, `SRE` | Writing, Portfolio Link |
| **Conference Talk (KubeCon, SREcon, re:Invent)** | `Public Speaking`, `Thought Leadership`, `Kubernetes`, `Observability`, `Platform` | Speaking, Leadership |
| **CNCF Project Contribution** | `Open Source`, `CNCF`, `Kubernetes`, `Prometheus`, `Argo`, `Envoy`, `Maintainer` | Projects, GitHub Link |
| **Internal Platform Adoption Case Study** | `Platform Engineering`, `Adoption Metrics`, `Developer Productivity`, `Change Management` | Experience, Projects |
| **Incident Postmortem (Sanitized)** | `Incident Response`, `Root Cause Analysis`, `Blameless Culture`, `Action Items`, `Reliability` | Experience, Leadership |

---

## Role-Specific ATS Optimization Notes

### Red Flags (Auto-Reject)
- **No Kubernetes** in 2024+ → immediate filter for Platform/DevOps
- **Only ClickOps / Console** → no IaC discipline
- **No CI/CD** keywords → can't automate path to production
- **No Observability / SLO** → reliability blind spot
- **No On-Call / Incident** → operations inexperience
- **Only one cloud** for Senior+ → lack of breadth (unless deep specialization stated)
- **>2 pages for <8 yrs** → format penalty
- **Tables/columns/graphics** → parser extraction failure

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `AWS`, `Kubernetes`, `Terraform`, `Docker`, `CI/CD`, `GitHub Actions`, `Prometheus`, `Grafana`, `GitOps`, `Linux`, `Bash`, `Python` |
| High | 1.5% | 3.0% | `ArgoCD`, `Flux`, `Helm`, `Go`, `Pulumi`, `Istio`, `Cilium`, `Vault`, `Kyverno`, `Chaos Engineering`, `FinOps`, `Backstage`, `SLO`, `Incident Response` |
| Medium | 1.0% | 2.5% | `GCP`, `Azure`, `Crossplane`, `Karpenter`, `External Secrets`, `OPA`, `Cosign`, `SBOM`, `Disaster Recovery`, `Capacity Planning`, `Mentoring` |
| Low | 0.5% | 1.5% | `Rust`, `TypeScript`, `Cluster API`, `Temporal`, `Dagster`, `Iceberg`, `Delta Lake`, `SLSA`, `Sigstore`, `eBPF`, `KubeVirt` |

### NDA Abstraction
- **L2**: "Multi-region Kubernetes platform (50 clusters, 10K+ nodes) on AWS/GCP"
- **L3**: "Reduced deployment lead time 80% and cloud spend 35% via GitOps and FinOps automation"
- **L4**: "Cut deployment lead time 80% and infrastructure cost 35% through platform standardization"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `devops-platform/devops-engineer` (or `sre` / `platform-engineer`)
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 10 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for applications, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (scope/scale/MTTR), Tech Lead (architecture/tools), Exec (risk/cost/reliability)
- [ ] Metrics validated via `metric_plausibility.py` (MTTR, deployment freq, change failure rate, cost savings, availability %)
- [ ] Portfolio cross-refs: GitHub/blog/talks/CNCF with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024