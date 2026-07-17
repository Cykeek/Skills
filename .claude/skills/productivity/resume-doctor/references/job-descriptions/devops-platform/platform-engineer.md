---
role_id: "devops-platform/platform-engineer"
canonical_title: "Platform Engineer"
aliases: ["Platform Engineer", "Internal Developer Platform Engineer", "Developer Experience Engineer", "DevEx Engineer", "Platform Infrastructure Engineer", "IDP Engineer"]
seniority_levels: ["Junior", "Mid", "Senior", "Staff", "Principal"]
related_roles: ["devops-platform/devops-engineer", "devops-platform/sre", "software-engineer/backend-engineer", "software-engineer/fullstack-engineer"]
ats_keywords:
  - "Platform Engineering"
  - "Internal Developer Platform"
  - "IDP"
  - "Developer Experience"
  - "DevEx"
  - "Self-Service"
  - "Golden Paths"
  - "Paved Roads"
  - "Backstage"
  - "Port"
  - "Cortex"
  - "Humanitec"
  - "Kubernetes"
  - "Docker"
  - "Terraform"
  - "GitOps"
  - "ArgoCD"
  - "Flux"
  - "CI/CD"
  - "GitHub Actions"
  - "GitLab CI"
  - "Go"
  - "Python"
  - "TypeScript"
  - "API Platform"
  - "Service Mesh"
  - "Istio"
  - "Cilium"
  - "Gateway API"
  - "Observability"
  - "SLO"
  - "Platform as Product"
  - "Adoption Metrics"
  - "Developer Productivity"
ats_skills_taxonomy:
  internal_developer_platform:
    - "IDP Platforms: Backstage (Software Catalog, Scaffolder, TechDocs, Scorecards), Port, Cortex, Humanitec, Cycloid"
    - "Self-Service Provisioning: Infrastructure (Terraform/Pulumi/CDK), Environments (ephemeral, preview), Databases, Secrets, Certificates"
    - "Developer Portal: Software Catalog (entities, relationships, ownership), TechDocs (mkdocs, mkdocs-material), Scorecards (maturity, security, reliability)"
    - "Scaffolding: Cookiecutter, GitHub Template, Yeoman, Backstage Scaffolder (templates, parameters, steps, publish)"
  developer_experience:
    - "Local Development: Tilt, Garden, DevSpace, Okteto, Telepresence (intercept, personal intercepts, preview URLs)"
    - "CLI Tools: Cobra (Go), Click/Typer (Python), oclif (TypeScript); auto-completion, plugins, distributed via Homebrew/Scoop"
    - "Feedback Loops: Deployment frequency, lead time, change failure rate, MTTR, developer NPS, time to first commit"
    - "Documentation: Diátaxis framework, ADR (MADR), runbooks, onboarding guides, architecture decision records"
  golden_paths:
    - "Paved Roads: Standardized workflows, approved patterns, migration guides, deprecation policy, adoption metrics"
    - "Service Templates: Language-specific (Go, Python, TypeScript, Java), framework-specific (FastAPI, Gin, NestJS, Spring Boot)"
    - "Infrastructure Modules: Terraform modules (VPC, EKS, RDS, Redis, Kafka), Helm charts, Kustomize bases"
    - "CI/CD Templates: GitHub Actions reusable workflows, GitLab CI templates, matrix builds, test stages, security scans"
  api_platform:
    - "API Gateway: Kong, Envoy, AWS API Gateway, GraphQL Federation, Rate Limiting, AuthZ/AuthN, Developer Portal"
    - "Service Mesh: Istio, Linkerd, Cilium (mTLS, Traffic Split, AuthZ, Observability, Retry/Timeout/Circuit Breaker)"
    - "Gateway API: HTTPRoute, GRPCRoute, TLSRoute, ReferenceGrant, BackendTLSPolicy, ExtensionRef"
    - "Contract Management: Protobuf, gRPC, AsyncAPI, Schema Registry (Confluent, Apicurio), Breaking Change Detection"
  platform_infrastructure:
    - "Kubernetes Platform: EKS/GKE/AKS/On-Prem, Cluster API (CAPI), ClusterClass, MachineDeployment, ClusterResourceSet"
    - "GitOps: ArgoCD/Flux (app-of-apps, multi-cluster, progressive delivery, image automation, policy-as-code)"
    - "Supply Chain: SBOM (Syft, SPDX/CycloneDX), Signing (Cosign, Sigstore), Verification (Policy Controller, Kyverno), Provenance (SLSA)"
    - "Security: Kyverno, OPA/Gatekeeper, Falco, Trivy, Cosign, Sigstore, Pod Security Standards, Network Policies"
  data_platform:
    - "Streaming: Kafka/Flink (Event Time, Watermarks, Exactly-Once, State), Redpanda, RisingWave, Materialize"
    - "Orchestration: Airflow/Dagster (Assets, Partitions, Sensors, Dynamic DAGs), Temporal (Workflows, Activities, Retries)"
    - "Transformation: dbt (Models, Tests, Snapshots, Exposures, Metrics, Contracts), SQLMesh"
    - "Lakehouse: Iceberg/Delta/Hudi (Time Travel, Branching, Reproducibility, Lineage), Unity Catalog, Polaris"
  programming_automation:
    - "Go: Standard Library, Cobra (CLI), Controller-runtime (Operators), gRPC/Connect, Testing (testify, ginkgo)"
    - "TypeScript: Node.js, Fastify/Hono, tRPC, Zod, Vitest, Biome, pnpm, Turborepo"
    - "Python: FastAPI/Click/Typer (CLI), Boto3/Pulumi SDK, Pytest, Type Hints (mypy/pyright), Poetry/UV"
    - "Infrastructure: Terraform/OpenTofu, Pulumi (TypeScript/Python/Go), AWS CDK, Crossplane (Composition, XR, Claim)"
seniority_signals:
  junior:
    - "Contributes to IDP: adds Backstage plugins, improves TechDocs, fixes scaffolder templates"
    - "Builds CI/CD pipeline templates: reusable workflows, matrix builds, test stages, security scans"
    - "Creates Terraform modules for team infrastructure: VPC, RDS, Redis, EKS node groups"
    - "Writes developer tooling: CLI tools (Go/Python/TypeScript) for common tasks (deploy, logs, secrets)"
    - "Improves local development: Tilt/Garden/DevSpace configs, Telepresence intercepts, mock services"
    - "Documents golden paths: service templates, migration guides, architecture decision records (ADRs)"
    - "Participates in platform on-call; triages developer requests; improves self-service documentation"
  mid:
    - "Owns IDP capabilities: Backstage (catalog, scaffolder, techdocs, scorecards), Port, or Cortex deployment"
    - "Builds self-service infrastructure: Terraform/Pulumi modules with policy enforcement (OPA/Kyverno)"
    - "Implements GitOps: ArgoCD/Flux (app-of-apps, multi-cluster, progressive delivery, drift detection)"
    - "Designs golden paths: service templates (Go/Python/TypeScript), CI/CD workflows, observability defaults"
    - "Develops API platform: Kong/Envoy Gateway, GraphQL Federation, rate limiting, auth, developer portal"
    - "Measures developer productivity: DORA metrics (deployment freq, lead time, CFR, MTTR), SPACE framework, adoption %"
    - "Mentors juniors; runs platform office hours; improves onboarding (time to first commit 2 weeks → 2 days)"
    - "Runs platform on-call; builds runbooks for IDP components; establishes SLOs for platform services"
  senior:
    - "Architects platform strategy: IDP selection (build vs buy), multi-year roadmap, team structure (platform vs enablement)"
    - "Defines platform standards: IaC (Terraform style guide), CI/CD (workflow library), observability baselines, security baselines"
    - "Leads platform migrations: Kubernetes version, CI/CD platform, secrets management, service mesh, IDP platform"
    - "Establishes platform-as-product: user research, feedback loops, product metrics (adoption, satisfaction, NPS)"
    - "Builds data platform: Kafka/Flink streaming, Airflow/Dagster orchestration, dbt transformation, Iceberg/Delta lakehouse"
    - "Partners with Security/Compliance: supply chain (SBOM, Cosign, SLSA), runtime (Falco/Tetragon), secrets (Vault/ESO)"
    - "Mentors Senior engineers; grows Staff engineers; defines IC career ladder; raises hiring bar"
    - "Evaluates vendor/build vs buy; influences org strategy; presents to leadership on platform ROI"
  staff:
    - "Defines 5-year platform strategy: IDP, developer experience, standardization, scale, AI-assisted development"
    - "Builds platform organization: hiring, structure (platform vs enablement vs foundations), charter, metrics"
    - "Leads high-stakes migrations: EKS 1.27→1.29, GitHub Enterprise → GitHub Actions, Vault → AWS Secrets Manager"
    - "Sets org-wide standards: IaC (Terraform), CI/CD (GitHub Actions), Observability (Grafana Cloud), Security (Kyverno)"
    - "Influences C-suite on platform investment ($50M+); presents to board on developer productivity & platform leverage"
    - "Grows Staff+ engineers; defines dual-track IC/Manager; industry speaking (KubeCon, PlatformCon, re:Invent)"
    - "Represents engineering in vendor negotiations; M&A platform due diligence; open source leadership (Backstage, CNCF)"
  principal:
    - "Company-wide platform/technology vision; long-term roadmap; competitive differentiation via platform"
    - "Industry recognition: keynotes, CNCF projects, standards bodies, open source leadership (Backstage, Argo, Envoy)"
    - "Crisis leadership: platform outages, security incidents, regulatory response, vendor failures"
    - "Builds engineering culture at scale: platform thinking, you-build-it-you-run-it, cognitive load reduction"
ats_weight_hints:
  must_have:
    - "Platform Engineering"
    - "Internal Developer Platform"
    - "IDP"
    - "Developer Experience"
    - "DevEx"
    - "Self-Service"
    - "Golden Paths"
    - "Backstage"
    - "Kubernetes"
    - "Docker"
    - "Terraform"
    - "GitOps"
    - "ArgoCD"
    - "Flux"
    - "CI/CD"
    - "GitHub Actions"
    - "Go"
    - "Python"
    - "TypeScript"
    - "API Gateway"
    - "Service Mesh"
    - "Observability"
    - "SLO"
    - "Platform as Product"
  strong_signal:
    - "Port"
    - "Cortex"
    - "Humanitec"
    - "Istio"
    - "Cilium"
    - "Gateway API"
    - "Kong"
    - "Envoy"
    - "GraphQL Federation"
    - "Tilt"
    - "Garden"
    - "DevSpace"
    - "Okteto"
    - "Telepresence"
    - "DORA Metrics"
    - "SPACE Framework"
    - "Adoption Metrics"
    - "Developer Productivity"
    - "Supply Chain Security"
    - "SBOM"
    - "Cosign"
    - "SLSA"
    - "Crossplane"
  nice_to_have:
    - "Rust"
    - "Dagster"
    - "Temporal"
    - "dbt"
    - "Iceberg"
    - "Delta Lake"
    - "Karpenter"
    - "Cluster API"
    - "eBPF"
    - "Cilium Tetragon"
    - "KubeVirt"
    - "Wasmer"
    - "Spin"
    - "Fermyon"
ats_parser_hints:
  greenhouse:
    - "platform engineering"
    - "internal developer platform"
    - "idp"
    - "developer experience"
    - "devex"
    - "self-service"
    - "golden paths"
    - "backstage"
    - "kubernetes"
    - "docker"
    - "terraform"
    - "gitops"
    - "argocd"
    - "flux"
    - "ci/cd"
    - "github actions"
    - "go"
    - "python"
    - "typescript"
    - "api gateway"
    - "service mesh"
    - "observability"
    - "slo"
    - "platform as product"
  lever:
    - "platform engineering"
    - "internal developer platform"
    - "idp"
    - "developer experience"
    - "devex"
    - "self-service"
    - "golden paths"
    - "backstage"
    - "kubernetes"
    - "docker"
    - "terraform"
    - "gitops"
    - "argocd"
    - "flux"
    - "ci/cd"
    - "github actions"
    - "go"
    - "python"
    - "typescript"
    - "api gateway"
    - "service mesh"
    - "observability"
    - "slo"
    - "platform as product"
  workday:
    - "Platform Engineering"
    - "Internal Developer Platform"
    - "Developer Experience"
    - "Self-Service"
    - "Golden Paths"
    - "Backstage"
    - "Kubernetes"
    - "Docker"
    - "Terraform"
    - "GitOps"
    - "ArgoCD"
    - "Flux"
    - "Continuous Integration"
    - "Continuous Deployment"
    - "GitHub Actions"
    - "Go"
    - "Python"
    - "TypeScript"
    - "API Gateway"
    - "Service Mesh"
    - "Observability"
    - "Service Level Objective"
    - "Platform as Product"
  icims:
    skill_clusters:
      platform_core: ["Platform Engineering", "Internal Developer Platform", "IDP", "Developer Experience", "DevEx", "Self-Service", "Golden Paths"]
      idp_tools: ["Backstage", "Port", "Cortex", "Humanitec", "Software Catalog", "Scaffolder", "TechDocs", "Scorecards"]
      kubernetes: ["Kubernetes", "EKS", "GKE", "AKS", "Helm", "Kustomize", "ArgoCD", "Flux", "Operators", "Cluster API"]
      infrastructure: ["Terraform", "Pulumi", "AWS CDK", "Crossplane", "GitOps", "Ansible", "Packer"]
      cicd: ["GitHub Actions", "GitLab CI", "Jenkins", "Argo Rollouts", "Flagger", "Buildpacks", "SBOM"]
      api_platform: ["Kong", "Envoy", "AWS API Gateway", "GraphQL Federation", "Gateway API", "Rate Limiting", "AuthZ", "Developer Portal"]
      developer_tools: ["Tilt", "Garden", "DevSpace", "Okteto", "Telepresence", "CLI Tools", "Go", "Python", "TypeScript"]
      metrics: ["DORA Metrics", "SPACE Framework", "Adoption Metrics", "Developer Productivity", "NPS", "Lead Time"]
      security: ["Supply Chain", "SBOM", "Cosign", "Sigstore", "SLSA", "Kyverno", "OPA", "Falco", "Vault", "ESO"]
  taleo:
    keywords: "Platform Engineering, Internal Developer Platform, IDP, Developer Experience, Backstage, Kubernetes, Docker, Terraform, GitOps, ArgoCD, Flux, CI/CD, GitHub Actions, Go, Python, TypeScript, API Gateway, Service Mesh, Observability, SLO, Self-Service, Golden Paths, Platform, Developer Productivity"
    boolean: "(\"Platform Engineering\" OR \"Internal Developer Platform\" OR \"IDP\") AND (\"Kubernetes\" OR \"K8s\" OR \"EKS\" OR \"GKE\") AND (\"Terraform\" OR \"Pulumi\" OR \"Crossplane\") AND (\"GitHub Actions\" OR \"GitLab CI\" OR \"ArgoCD\" OR \"Flux\") AND (\"Go\" OR \"Python\" OR \"TypeScript\") AND (\"Backstage\" OR \"Port\" OR \"Cortex\" OR \"Self-Service\")"
---
## Role Summary

> **Platform Engineer** — Builds the Internal Developer Platform (IDP) that enables product teams to ship safely and quickly. Owns the "path to production": self-service infrastructure, golden paths, CI/CD, API platform, developer tooling. Treats platform as a product: user research, feedback loops, adoption metrics. At Senior+ defines platform strategy and standards; at Staff+ builds the platform organization and sets company-wide technical direction.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### Internal Developer Platform (All Levels)
- Build and operate **Internal Developer Platform (IDP)**: **Backstage** (Software Catalog, Scaffolder, TechDocs, Scorecards), **Port**, **Cortex**, **Humanitec**
- Enable **self-service provisioning**: infrastructure (Terraform/Pulumi/CDK), environments (ephemeral, preview), databases, secrets, certificates
- Maintain **developer portal**: **software catalog** (entities, relationships, ownership), **TechDocs** (mkdocs, mkdocs-material), **scorecards** (maturity, security, reliability)
- Develop **scaffolding templates**: **Cookiecutter**, **GitHub Template**, **Yeoman**, **Backstage Scaffolder** (templates, parameters, steps, publish)

### Developer Experience & Golden Paths (All Levels)
- Optimize **local development**: **Tilt**, **Garden**, **DevSpace**, **Okteto**, **Telepresence** (intercept, personal intercepts, preview URLs)
- Build **CLI tools**: **Cobra** (Go), **Click/Typer** (Python), **oclif** (TypeScript); auto-completion, plugins, distribution (Homebrew/Scoop)
- Define **golden paths / paved roads**: standardized workflows, approved patterns, migration guides, deprecation policy, **adoption metrics**
- Create **service templates**: language-specific (Go, Python, TypeScript, Java), framework-specific (FastAPI, Gin, NestJS, Spring Boot)
- Measure **developer productivity**: **DORA metrics** (deployment frequency, lead time, change failure rate, MTTR), **SPACE framework**, **developer NPS**, **adoption %**

### CI/CD & GitOps (Mid+)
- Build **reusable CI/CD workflows**: **GitHub Actions** (composite actions, reusable workflows, matrix, OIDC, self-hosted runners), **GitLab CI**
- Implement **GitOps**: **ArgoCD/Flux** (app-of-apps, multi-cluster, progressive delivery, image automation, policy-as-code)
- Containerize applications: **Docker** (multi-stage, BuildKit, distroless, SBOM, Cosign signing, multi-arch), **Buildpacks**, **Kaniko**
- Progressive delivery: **Argo Rollouts**, **Flagger**, **Flux Image Automation** (canary, blue-green, A/B, feature flags)

### API Platform & Service Mesh (Senior+)
- Operate **API Gateway**: **Kong**, **Envoy**, **AWS API Gateway**, **GraphQL Federation**, rate limiting, AuthZ/AuthN, **developer portal**
- Manage **service mesh**: **Istio**, **Linkerd**, **Cilium** (mTLS, traffic split, AuthZ, observability, retry/timeout/circuit breaker)
- Implement **Gateway API**: HTTPRoute, GRPCRoute, TLSRoute, ReferenceGrant, BackendTLSPolicy, ExtensionRef
- Contract management: **Protobuf**, **gRPC**, **AsyncAPI**, **Schema Registry** (Confluent, Apicurio), breaking change detection

### Platform Infrastructure & Security (Senior+)
- Architect **Kubernetes platform**: EKS/GKE/AKS/On-Prem, **Cluster API** (CAPI), ClusterClass, MachineDeployment, ClusterResourceSet
- Harden **supply chain**: **SBOM** (Syft, SPDX/CycloneDX), **Signing** (Cosign, Sigstore), **Verification** (Policy Controller, Kyverno), **Provenance** (SLSA)
- Runtime **security**: **Falco**, **Tetragon** (eBPF), **Cilium** (Network Policy, L7), **KubeArmor** (AppArmor/SELinux), **Admission Control**
- **Secrets management**: **Vault**, **AWS Secrets Manager**, **1Password**, **SOPS**, **SealedSecrets**, **External Secrets Operator (ESO)**

### Data Platform & Orchestration (Staff+)
- Build **streaming platform**: **Kafka/Flink** (event time, watermarks, exactly-once, state), **Redpanda**, **RisingWave**, **Materialize**
- Orchestrate **workflows**: **Airflow/Dagster** (assets, partitions, sensors, dynamic DAGs), **Temporal** (workflows, activities, retries)
- Transform **data**: **dbt** (models, tests, snapshots, exposures, metrics, contracts), **SQLMesh**
- Lakehouse: **Iceberg/Delta/Hudi** (time travel, branching, reproducibility, lineage), **Unity Catalog**, **Polaris**

### Strategy & Leadership (Staff+)
- Define **multi-year platform strategy**: IDP, developer experience, standardization, scale, AI-assisted development
- Build **platform organization**: hiring, structure (platform vs enablement vs foundations), charter, metrics (adoption, satisfaction, lead time)
- Lead **high-stakes migrations**: Kubernetes version, CI/CD platform, secrets management, service mesh, IDP platform
- Set **org-wide standards**: IaC (Terraform), CI/CD (GitHub Actions), Observability (Grafana Cloud), Security (Kyverno)
- Influence **C-suite** on platform investment; present to **board** on developer productivity & platform leverage
- Grow **Staff+ engineers**; define **dual-track IC/Manager**; **industry speaking**; **open source leadership**

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
- **Platform Engineering**, **Internal Developer Platform**, **IDP**, **Developer Experience**, **DevEx**
- **Self-Service**, **Golden Paths**, **Paved Roads**, **Backstage** (or Port/Cortex)
- **Kubernetes**, **Docker**, **Terraform**, **GitOps**, **ArgoCD/Flux**
- **CI/CD** (GitHub Actions preferred), **Go**, **Python**, **TypeScript**
- **API Gateway** (Kong/Envoy), **Service Mesh** (Istio/Cilium/Linkerd)
- **Observability**, **SLO**, **Platform as Product**, **Developer Productivity**

### Strong Signal (Differentiators)
- **ArgoCD/Flux**, **Crossplane**, **Gateway API**, **GraphQL Federation**, **Kong/Envoy**
- **Tilt/Garden/DevSpace/Okteto/Telepresence**, **DORA Metrics**, **SPACE Framework**
- **Supply Chain Security** (SBOM, Cosign, SLSA), **Kyverno/OPA**, **Falco/Tetragon**
- **Cluster API**, **Karpenter**, **Temporal/Dagster**, **dbt/Iceberg/Delta Lake**
- **Adoption Metrics**, **Developer NPS**, **Platform as Product**, **User Research**

### Nice-to-Have (Specialization)
- **Rust**, **Dagster**, **Temporal**, **dbt**, **Iceberg**, **Delta Lake**, **Karpenter**, **Cluster API**
- **eBPF/Cilium Tetragon**, **KubeVirt**, **WebAssembly** (Wasmer, Spin, Fermyon), **Edge Compute**

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Junior (0-2 yrs)
- **Contributed** to **IDP**: **added Backstage plugins**, **improved TechDocs**, **fixed scaffolder templates**
- **Built** **CI/CD pipeline templates**: **reusable workflows**, **matrix builds**, **test stages**, **security scans**
- **Created** **Terraform modules** for **team infrastructure**: **VPC**, **RDS**, **Redis**, **EKS node groups**
- **Wrote** **developer tooling**: **CLI tools** (Go/Python/TypeScript) for **common tasks** (deploy, logs, secrets)
- **Improved** **local development**: **Tilt/Garden/DevSpace configs**, **Telepresence intercepts**, **mock services**
- **Documented** **golden paths**: **service templates**, **migration guides**, **ADRs**

### Mid (2-5 yrs)
- **Owned** **IDP capabilities**: **Backstage** (catalog, scaffolder, techdocs, scorecards), **Port**, or **Cortex deployment**
- **Built** **self-service infrastructure**: **Terraform/Pulumi modules** with **policy enforcement** (OPA/Kyverno)
- **Implemented** **GitOps**: **ArgoCD/Flux** (app-of-apps, multi-cluster, progressive delivery, drift detection)
- **Designed** **golden paths**: **service templates** (Go/Python/TypeScript), **CI/CD workflows**, **observability defaults**
- **Developed** **API platform**: **Kong/Envoy Gateway**, **GraphQL Federation**, **rate limiting**, **auth**, **developer portal**
- **Measured** **developer productivity**: **DORA metrics** (deployment freq, lead time, CFR, MTTR), **SPACE**, **adoption %**
- **Mentored** **juniors**; **ran platform office hours**; **improved onboarding** (time to first commit 2 weeks → 2 days)
- **Ran** **platform on-call**; **built runbooks** for **IDP components**; **established SLOs** for **platform services**

### Senior (5-8 yrs)
- **Architected** **platform strategy**: **IDP selection** (build vs buy), **multi-year roadmap**, **team structure** (platform vs enablement)
- **Defined** **platform standards**: **IaC** (Terraform style guide), **CI/CD** (workflow library), **observability baselines**, **security baselines**
- **Led** **platform migrations**: **Kubernetes version**, **CI/CD platform**, **secrets management**, **service mesh**, **IDP platform**
- **Established** **platform-as-product**: **user research**, **feedback loops**, **product metrics** (adoption, satisfaction, NPS)
- **Built** **data platform**: **Kafka/Flink streaming**, **Airflow/Dagster orchestration**, **dbt transformation**, **Iceberg/Delta lakehouse**
- **Partnered** with **Security/Compliance**: **supply chain** (SBOM, Cosign, SLSA), **runtime** (Falco/Tetragon), **secrets** (Vault/ESO)
- **Mentored** **Senior engineers**; **grew Staff engineers**; **defined IC career ladder**; **raised hiring bar**
- **Evaluated** **vendor/build vs buy**; **influenced org strategy**; **presented to leadership** on **platform ROI**

### Staff (8-12 yrs)
- **Defined** **5-year platform strategy**: **IDP**, **developer experience**, **standardization**, **scale**, **AI-assisted development**
- **Built** **platform organization** (30 engineers): **charter**, **metrics** (adoption, satisfaction, lead time), **enablement model**
- **Led** **high-stakes migrations**: **EKS 1.27→1.29**, **GitHub Enterprise → GitHub Actions**, **HashiCorp Vault → AWS Secrets Manager**
- **Set** **org-wide standards**: **IaC (Terraform)**, **CI/CD (GitHub Actions)**, **Observability (Grafana Cloud)**, **Security (Kyverno)**
- **Influenced** **C-suite** on **platform investment** ($100M+); **presented to board** on **developer productivity & platform leverage**
- **Grew** **Staff+ cohort** 5→20; **industry speaking** (KubeCon, PlatformCon, AWS re:Invent); **CNCF project maintainer**
- **Represented** **engineering in vendor negotiations**; **M&A platform due diligence**; **open source leadership**

### Principal (12+ yrs)
- **Company-wide platform vision**; **10-year technology roadmap**; **competitive differentiation** via **platform**
- **Industry recognition**: **CNCF Ambassador**, **KubeCon Keynote**, **Standards Bodies**, **OSS Leadership** (Backstage, Argo, Envoy)
- **Crisis leadership**: **platform outages**, **security incidents**, **regulatory response**, **vendor failures**
- **Transformed engineering culture**: **platform thinking**, **you-build-it-you-run-it**, **cognitive load reduction** at scale

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `platform engineering`, `internal developer platform`, `idp`, `developer experience`, `devex`, `self-service`, `golden paths`, `backstage`, `kubernetes`, `docker`, `terraform`, `gitops`, `argocd`, `flux`, `ci/cd`, `github actions`, `go`, `python`, `typescript`, `api gateway`, `service mesh`, `observability`, `slo`, `platform as product`
**Stemming**: `platform`→`platforms`/`platforming`, `develop`→`developer`/`development`, `automat`→`automated`/`automation`
**Fuzzy**: `idp`≈`internal developer platform`, `k8s`≈`kubernetes`, `tf`≈`terraform`, `argocd`≈`argo cd`, `devex`≈`developer experience`, `dora`≈`deployment frequency`/`lead time`/`change failure rate`/`mttr`

### Lever
**Exact**: `platform engineering`, `internal developer platform`, `idp`, `developer experience`, `devex`, `self-service`, `golden paths`, `backstage`, `kubernetes`, `docker`, `terraform`, `gitops`, `argocd`, `flux`, `ci/cd`, `github actions`, `go`, `python`, `typescript`, `api gateway`, `service mesh`, `observability`, `slo`, `platform as product`
**Normalization**: `internal developer platform`→`idp`, `backstage software catalog`→`backstage`, `github actions reusable workflows`→`github actions`, `argo cd`→`argocd`, `flux cd`→`flux`

### Workday
**Exact (title case)**: `Platform Engineering`, `Internal Developer Platform`, `Developer Experience`, `Self-Service`, `Golden Paths`, `Backstage`, `Kubernetes`, `Docker`, `Terraform`, `GitOps`, `ArgoCD`, `Flux`, `Continuous Integration`, `Continuous Deployment`, `GitHub Actions`, `Go`, `Python`, `TypeScript`, `API Gateway`, `Service Mesh`, `Observability`, `Service Level Objective`, `Platform as Product`
**Compound**: `Amazon EKS`, `Google GKE`, `Azure AKS`, `AWS API Gateway`, `Google Cloud API Gateway`, `Azure API Management`

### iCIMS
**Skill clusters**:
```
platform_core: ["Platform Engineering", "Internal Developer Platform", "IDP", "Developer Experience", "DevEx", "Self-Service", "Golden Paths"]
idp_tools: ["Backstage", "Port", "Cortex", "Humanitec", "Software Catalog", "Scaffolder", "TechDocs", "Scorecards"]
kubernetes: ["Kubernetes", "EKS", "GKE", "AKS", "Helm", "Kustomize", "ArgoCD", "Flux", "Operators", "Cluster API"]
infrastructure: ["Terraform", "Pulumi", "AWS CDK", "Crossplane", "GitOps", "Ansible", "Packer"]
cicd: ["GitHub Actions", "GitLab CI", "Jenkins", "Argo Rollouts", "Flagger", "Buildpacks", "SBOM"]
api_platform: ["Kong", "Envoy", "AWS API Gateway", "GraphQL Federation", "Gateway API", "Rate Limiting", "AuthZ", "Developer Portal"]
developer_tools: ["Tilt", "Garden", "DevSpace", "Okteto", "Telepresence", "CLI Tools", "Go", "Python", "TypeScript"]
metrics: ["DORA Metrics", "SPACE Framework", "Adoption Metrics", "Developer Productivity", "NPS", "Lead Time"]
security: ["Supply Chain", "SBOM", "Cosign", "Sigstore", "SLSA", "Kyverno", "OPA", "Falco", "Vault", "ESO"]
```
**Weighting**: platform_core (0.2) + idp_tools (0.15) + kubernetes (0.15) + infrastructure (0.1) + cicd (0.1) + api_platform (0.1) + developer_tools (0.1) + metrics (0.05) + security (0.05)

### Taleo
**Keywords**: `Platform Engineering, Internal Developer Platform, IDP, Developer Experience, Backstage, Kubernetes, Docker, Terraform, GitOps, ArgoCD, Flux, CI/CD, GitHub Actions, Go, Python, TypeScript, API Gateway, Service Mesh, Observability, SLO, Self-Service, Golden Paths, Platform, Developer Productivity`
**Boolean**: `("Platform Engineering" OR "Internal Developer Platform" OR "IDP") AND ("Kubernetes" OR "K8s" OR "EKS" OR "GKE") AND ("Terraform" OR "Pulumi" OR "Crossplane") AND ("GitHub Actions" OR "GitLab CI" OR "ArgoCD" OR "Flux") AND ("Go" OR "Python" OR "TypeScript") AND ("Backstage" OR "Port" OR "Cortex" OR "Self-Service")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: Platform Team in Scale-Up (Series B-D, 100-500 eng)
**Keywords**: `platform engineering`, `idp`, `backstage`, `developer experience`, `self-service`, `golden paths`, `argocd`, `flux`, `github actions`, `terraform`, `kubernetes`, `go`, `typescript`, `dora metrics`, `adoption`, `onboarding`, `platform as product`, `user research`, `feedback loops`
**Mirror**: Lead with **platform leverage** (teams onboarded, adoption %, lead time reduction, deployment frequency). Use `enabled`, `standardized`, `accelerated`, `measured`, `iterated`. Emphasize **product mindset**, **user research**, **feedback loops**, **platform as product**.

### Archetype 2: Enterprise Platform / Regulated (FinTech, HealthTech, Large Corp)
**Keywords**: `compliance`, `soc2`, `policy as code`, `opa`, `kyverno`, `supply chain`, `sbom`, `cosign`, `slsa`, `landing zone`, `control tower`, `multi-account`, `guardrails`, `disaster recovery`, `rto`, `rpo`, `crossplane`, `cluster api`, `centralized platform`, `shared services`, `enablement`, `governance`, `audit`, `evidence`
**Mirror**: Lead with **governance**, **compliance posture**, **risk reduction**. Use `architected`, `enforced`, `standardized`, `audited`, `certified`. Emphasize **policy as code**, **centralized control**, **audit readiness**, **shared services model**.

### Archetype 3: Big Tech / Platform Company (FAANG, Platform Vendors)
**Keywords**: `internal developer platform`, `backstage`, `port`, `cortex`, `humanitec`, `developer productivity`, `dx`, `cognitive load`, `golden paths`, `paved roads`, `scaffolding`, `templates`, `cli`, `api platform`, `kong`, `envoy`, `gateway api`, `service mesh`, `istio`, `cilium`, `platform engineering`, `enablement`, `adoption metrics`, `nps`, `lead time`, `deployment frequency`, `change failure rate`, `mttr`, `space framework`
**Mirror**: Lead with **platform scale** (engineers served, services deployed, adoption metrics). Use `built`, `enabled`, `standardized`, `accelerated`, `measured`. Emphasize **leverage**, **multiplier effect**, **developer productivity**, **cognitive load reduction**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `Platform Engineering` / `IDP` / `Developer Experience` | JD requires platform; resume says "DevOps" only | Add `Platform Engineering`, `Internal Developer Platform`, `Developer Experience`, `Self-Service`, `Golden Paths` |
| `Backstage` / `Port` / `Cortex` | JD requires IDP; missing | Add `Backstage` (Software Catalog, Scaffolder, TechDocs, Scorecards) or `Port`/`Cortex`; describe implementation |
| `GitOps` / `ArgoCD` / `Flux` | JD requires; resume has manual `kubectl apply` | Add `GitOps (ArgoCD/Flux)`, `App-of-Apps`, `Progressive Delivery`, `Image Automation`, `Drift Detection` |
| `DORA Metrics` / `SPACE Framework` / `Adoption Metrics` | Senior+ JD; missing | Add `Deployment Frequency`, `Lead Time`, `Change Failure Rate`, `MTTR`, `Developer NPS`, `Platform Adoption %` |
| `API Gateway` / `Service Mesh` / `Gateway API` | JD requires; missing | Add `Kong/Envoy/AWS API Gateway`, `Istio/Cilium/Linkerd`, `Gateway API (HTTPRoute, GRPCRoute)` |
| `Supply Chain Security` / `SBOM` / `SLSA` | Enterprise JD; missing | Add `SBOM (Syft, SPDX/CycloneDX)`, `Cosign/Sigstore Signing`, `SLSA Provenance`, `Policy Controller/Kyverno` |
| `Developer Tooling` / `CLI` / `Local Dev` | JD requires DX; missing | Add `Tilt/Garden/DevSpace/Okteto`, `Telepresence`, `CLI Tools (Cobra/Click/oclif)` |
| `Crossplane` / `Cluster API` / `Karpenter` | Staff+ JD; missing | Add `Crossplane (Composition, XR, Claim)`, `Cluster API (CAPI, ClusterClass)`, `Karpenter (NodePool, Consolidation)` |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| **GitHub: Platform Tooling / Operator / CLI** | `Open Source`, `Go`, `TypeScript`, `Python`, `Kubernetes`, `Controller-runtime`, `Community`, `Downloads` | Projects, GitHub Link |
| **Technical Blog: Platform Engineering / DevEx** | `Technical Writing`, `Platform Engineering`, `Developer Experience`, `IDP`, `Backstage`, `GitOps`, `DORA` | Writing, Portfolio Link |
| **Conference Talk (PlatformCon, KubeCon, re:Invent, QCon)** | `Public Speaking`, `Thought Leadership`, `Platform Engineering`, `Developer Experience`, `IDP`, `Platform as Product` | Speaking, Leadership |
| **CNCF Project Contribution** | `Open Source`, `CNCF`, `Kubernetes`, `Argo`, `Envoy`, `Backstage`, `Prometheus`, `Maintainer` | Projects, GitHub Link |
| **Internal Platform Adoption Case Study** | `Platform Engineering`, `Adoption Metrics`, `Developer Productivity`, `Change Management`, `DORA`, `NPS` | Experience, Projects |
| **Platform RFC / Architecture Decision Record** | `Architecture`, `Decision Making`, `Platform Strategy`, `Standards`, `Governance`, `ADR`, `MADR` | Experience, Leadership |

---

## Role-Specific ATS Optimization Notes

### Red Flags (Auto-Reject)
- **No IDP/Backstage/Platform Engineering keywords** → Just DevOps, not Platform Engineering
- **No Self-Service/Golden Paths** → No product mindset, ticket-driven ops
- **No Developer Productivity Metrics** (DORA/SPACE/Adoption) → Can't measure platform value
- **Only Infrastructure, no Developer Experience** → Missing the "platform as product" philosophy
- **No CI/CD Pipeline Templates / Reusable Workflows** → No standardization, no leverage
- **>2 pages for <8 yrs** → Format penalty
- **Tables/columns/graphics** → Parser extraction failure

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `Platform Engineering`, `Internal Developer Platform`, `IDP`, `Developer Experience`, `Backstage`, `Kubernetes`, `Terraform`, `GitOps`, `ArgoCD`, `Flux`, `GitHub Actions`, `Go`, `Python`, `TypeScript` |
| High | 1.5% | 3.0% | `Self-Service`, `Golden Paths`, `API Gateway`, `Service Mesh`, `Gateway API`, `DORA Metrics`, `SPACE Framework`, `Adoption Metrics`, `Supply Chain Security`, `SBOM`, `Crossplane` |
| Medium | 1.0% | 2.5% | `Port`, `Cortex`, `Tilt`, `Garden`, `Telepresence`, `Cluster API`, `Karpenter`, `Temporal`, `Dagster`, `dbt`, `Iceberg`, `Mentoring`, `Architecture Review` |
| Low | 0.5% | 1.5% | `Rust`, `Dagster`, `Temporal`, `KubeVirt`, `Wasmer`, `Spin`, `Fermyon`, `eBPF`, `Cilium Tetragon`, `SLSA`, `Sigstore` |

### NDA Abstraction
- **L2**: "Platform Engineering for 200+ engineers: IDP (Backstage), GitOps (ArgoCD), self-service infra (Terraform)"
- **L3**: "Reduced developer onboarding 90% (2 weeks → 2 days) and deployment lead time 80% via platform standardization"
- **L4**: "Cut onboarding 90% and lead time 80% through Internal Developer Platform and golden paths"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `devops-platform/platform-engineer`
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 10 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for applications, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (adoption/lead time/DX), Tech Lead (architecture/standards), Exec (leverage/ROI/productivity)
- [ ] Metrics validated via `metric_plausibility.py` (deployment freq, lead time, CFR, MTTR, adoption %, NPS, time to first commit, platform ROI)
- [ ] Portfolio cross-refs: GitHub/blog/talks/CNCF with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024