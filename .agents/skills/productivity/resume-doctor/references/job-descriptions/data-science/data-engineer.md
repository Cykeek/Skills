---
role_id: "data-science/data-engineer"
canonical_title: "Data Engineer"
aliases: ["Data Platform Engineer", "Analytics Engineer", "ETL Engineer", "Data Pipeline Engineer", "Big Data Engineer"]
seniority_levels: ["Junior", "Mid", "Senior", "Staff", "Principal"]
related_roles: ["data-scientist", "ml-engineer", "software-engineer/backend-engineer", "devops-platform/devops-engineer", "product-manager/technical-pm"]
ats_keywords:
  - "SQL"
  - "Python"
  - "Spark"
  - "Airflow"
  - "dbt"
  - "Snowflake"
  - "BigQuery"
  - "Redshift"
  - "Databricks"
  - "Kafka"
  - "Flink"
  - "Data Lake"
  - "Data Warehouse"
  - "ETL"
  - "ELT"
  - "Data Modeling"
  - "Data Quality"
  - "Great Expectations"
  - "dbt Tests"
  - "Soda"
  - "Monte Carlo"
  - "Data Governance"
  - "Data Catalog"
  - "Lineage"
  - "CDC"
  - "Debezium"
  - "Delta Lake"
  - "Iceberg"
  - "Hudi"
  - "Kubernetes"
  - "Docker"
  - "AWS"
  - "GCP"
  - "Azure"
  - "Terraform"
  - "CI/CD"
  - "GitHub Actions"
  - "GitLab CI"
  - "Observability"
  - "Prometheus"
  - "Grafana"
ats_skills_taxonomy:
  data_processing:
    - "Batch: Spark (PySpark, Structured APIs, Delta Lake, Iceberg, Hudi), Databricks (Photon, Serverless), EMR (EKS, Serverless), Synapse"
    - "Streaming: Kafka (Connect, Streams, ksqlDB), Flink (Stateful, Event Time, Exactly-Once, Savepoints), Redpanda, RisingWave, Materialize, Bytewax"
    - "OLAP: ClickHouse, Apache Druid, StarRocks, Doris, Trino/Presto (Federated, Cost-Based Optimizer), DuckDB (Embedded, WASM)"
    - "Warehouses: Snowflake (Snowpark, Streams, Tasks, Dynamic Tables), BigQuery (BigLake, BI Engine, Materialized Views), Redshift (RA3, Serverless, Spectrum), Databricks SQL"
    - "Transformation: dbt (Core, Cloud, Macros, Packages, Tests, Contracts, Semantic Layer), SQLMesh, Dataform, SQLFluff"
  orchestration:
    - "Airflow: DAGs, TaskFlow, XCom, Dynamic Mapping, Deferrable Operators, Smart Sensors, Datasets, Timetables, Provider Ecosystem"
    - "Dagster: Assets, Partitions, Sensors, Jobs, IO Managers, Resources, Definitions, Code Locations, Dagster Cloud"
    - "Prefect: Flows, Tasks, Deployments, Work Pools, Blocks, Automations, Prefect Cloud"
    - "Temporal: Workflows, Activities, Retries, Timeouts, Durable Execution, Visibility, Replay, Update, Nexus"
    - "Modern: Dagster/Prefect/Temporal (Declarative, Type-Safe, Testable, Observability-First) vs Airflow (Mature, Ecosystem, Scale)"
  data_modeling:
    - "Dimensional: Kimball (Star/Snowflake, Conformed Dimensions, Slowly Changing Dimensions Type 0/1/2/3/4/6/7), Data Vault 2.0 (Hub/Link/Sat, PIT, Bridge)"
    - "Activity Schema: Event-based (Action, Timestamp, Actor, Attributes), Temporal Queries, Self-Join Elimination"
    - "Semantic Layer: dbt Metrics, Cube, AtScale, LookML, Tableau Semantics, Power BI DAX (Headless BI, Metrics Definition, Governance)"
    - "Contract Testing: dbt Contracts, SQLMesh, Data Contracts (Schema, SLA, Ownership, Deprecation), Great Expectations"
  data_quality_observability:
    - "Testing: Great Expectations (Expectations, Checkpoints, Data Docs, Validation Operator), dbt Tests (Generic, Singular, Packages), Soda (CL, Checks, Anomaly Detection), Elementary (dbt-native, Freshness, Schema, Distribution)"
    - "Observability: Monte Carlo (ML-powered, Lineage, Anomaly, Root Cause), Datafold (Column-level Lineage, Diff, CI), Metaplane, Validio"
    - "Freshness/SLA: dbt Freshness, Dagster Asset Observations, Airflow SLAs, Custom Alerting (Looker, Metabase, Grafana)"
    - "Anomaly Detection: Statistical (Z-score, IQR, Seasonal Decomposition), ML-based (Isolation Forest, Prophet), Threshold vs Learned"
  data_governance:
    - "Catalog: DataHub (Acryl), Amundsen, OpenMetadata, Atlan, Collibra, Alation, Purview (Metadata, Lineage, Search, Ownership, Glossary)"
    - "Lineage: Column-level (Datafold, DataHub, OpenLineage, dbt), Table-level, Cross-system (Spark→Snowflake→Looker), Impact Analysis"
    - "Privacy/Compliance: PII Detection (AWS Macie, GCP DLP, Azure Purview), Tagging, Masking, Tokenization, Encryption, GDPR/CCPA/HIPAA"
    - "Access Control: RBAC/ABAC (Snowflake/BigQuery/Redshift/Databricks), Dynamic Masking, Row-level Security, Column-level Security"
  infrastructure:
    - "Cloud: AWS (S3, Glue, Athena, Redshift, EMR, MSK, Kinesis, Lambda, Step Functions), GCP (GCS, Dataflow, BigQuery, Pub/Sub, Composer, Dataproc)"
    - "Kubernetes: Operators (Spark, Airflow, Flink, Trino), Helm, Kustomize, ArgoCD, Flux (GitOps), KEDA (Event-driven Autoscaling)"
    - "Storage Formats: Parquet (Compression, Encoding, Bloom Filters, Data Page), ORC, Avro, Arrow/Feather, Delta Lake (ACID, Time Travel, Schema Evolution, Z-Order), Iceberg (Hidden Partitioning, Partition Evolution, Merge-on-Read), Hudi (COW/MOR, Clustering)"
    - "IaC: Terraform (Modules, State, Workspaces, Providers), Pulumi (TypeScript/Python/Go), Crossplane (Kubernetes-native)"
    - "CI/CD: GitHub Actions/GitLab CI (dbt, SQLFluff, Great Expectations, Terraform), Environments, Approval Gates, Rollback"
    - "Cost: FinOps (Attribution, Anomaly, Optimization), Snowflake/BigQuery/Redshift Cost Monitoring, Query Optimization, Materialization Strategy"
  real_time_analytics:
    - "CDC: Debezium (MySQL/Postgres/MongoDB/SQL Server/Oracle), Maxwell, Striim, Qlik Replicate (Log-based, Non-intrusive)"
    - "Stream Processing: Flink SQL, ksqlDB, RisingWave, Materialize, Redpanda (WASM Transforms), Bytewax (Python)"
    - "Serving: Redis (Streams, Modules), Apache Druid, ClickHouse, StarRocks, Doris, Pinot (Low-latency, High-concurrency, Aggregations)"
    - "Event Streaming: Kafka (Topics, Partitions, Retention, Compaction, Quotas, Tiered Storage), Schema Registry (Avro/Protobuf/JSON, Compatibility)"
ats_weight_hints:
  must_have:
    - "SQL"
    - "Python"
    - "Spark"
    - "Airflow"
    - "dbt"
    - "Snowflake"
    - "BigQuery"
    - "Redshift"
    - "Databricks"
    - "Kafka"
    - "Data Lake"
    - "Data Warehouse"
    - "ETL"
    - "ELT"
    - "Data Modeling"
    - "Data Quality"
    - "Great Expectations"
    - "dbt Tests"
    - "Data Governance"
    - "Data Catalog"
    - "Lineage"
    - "Kubernetes"
    - "Docker"
    - "AWS"
    - "Terraform"
    - "CI/CD"
    - "GitHub Actions"
    - "Observability"
  strong_signal:
    - "Flink"
    - "Delta Lake"
    - "Iceberg"
    - "Hudi"
    - "Debezium"
    - "CDC"
    - "Dagster"
    - "Prefect"
    - "Temporal"
    - "ClickHouse"
    - "Druid"
    - "DataHub"
    - "OpenMetadata"
    - "Monte Carlo"
    - "Datafold"
    - "Soda"
    - "Elementary"
    - "dbt Contracts"
    - "SQLMesh"
    - "GCP"
    - "Azure"
    - "GitLab CI"
    - "ArgoCD"
    - "FinOps"
  nice_to_have:
    - "Redpanda"
    - "RisingWave"
    - "Materialize"
    - "Bytewax"
    - "Trino"
    - "Presto"
    - "DuckDB"
    - "StarRocks"
    - "Doris"
    - "Pinot"
    - "Polars"
    - "Dask"
    - "Ray"
    - "dbt Semantic Layer"
    - "Cube"
    - "AtScale"
    - "LookML"
    - "OpenLineage"
    - "Pulumi"
    - "Crossplane"
    - "KEDA"
    - "Data Contracts"
ats_parser_hints:
  greenhouse:
    - "sql"
    - "python"
    - "spark"
    - "airflow"
    - "dbt"
    - "snowflake"
    - "bigquery"
    - "redshift"
    - "databricks"
    - "kafka"
    - "data lake"
    - "data warehouse"
    - "etl"
    - "elt"
    - "data modeling"
    - "data quality"
    - "great expectations"
    - "dbt tests"
    - "data governance"
    - "data catalog"
    - "lineage"
    - "kubernetes"
    - "docker"
    - "aws"
    - "terraform"
    - "ci/cd"
    - "github actions"
    - "observability"
  lever:
    - "sql"
    - "python"
    - "spark"
    - "airflow"
    - "dbt"
    - "snowflake"
    - "bigquery"
    - "redshift"
    - "databricks"
    - "kafka"
    - "data lake"
    - "data warehouse"
    - "etl"
    - "elt"
    - "data modeling"
    - "data quality"
    - "great expectations"
    - "dbt tests"
    - "data governance"
    - "data catalog"
    - "lineage"
    - "kubernetes"
    - "docker"
    - "aws"
    - "terraform"
    - "ci/cd"
    - "github actions"
    - "observability"
  workday:
    - "SQL"
    - "Python"
    - "Apache Spark"
    - "Apache Airflow"
    - "dbt"
    - "Snowflake"
    - "BigQuery"
    - "Redshift"
    - "Databricks"
    - "Apache Kafka"
    - "Data Lake"
    - "Data Warehouse"
    - "ETL"
    - "ELT"
    - "Data Modeling"
    - "Data Quality"
    - "Great Expectations"
    - "dbt Tests"
    - "Data Governance"
    - "Data Catalog"
    - "Lineage"
    - "Kubernetes"
    - "Docker"
    - "Amazon Web Services"
    - "Terraform"
    - "Continuous Integration"
    - "GitHub Actions"
    - "Observability"
  icims:
    skill_clusters:
      processing: ["SQL", "Python", "Spark", "Flink", "Kafka", "Databricks", "EMR", "Dataflow"]
      warehousing: ["Snowflake", "BigQuery", "Redshift", "Databricks SQL", "ClickHouse", "Druid", "Trino", "Iceberg", "Delta Lake", "Hudi"]
      orchestration: ["Airflow", "Dagster", "Prefect", "Temporal", "dbt", "SQLMesh"]
      modeling: ["Data Modeling", "Kimball", "Data Vault", "Activity Schema", "Semantic Layer", "dbt Metrics", "Cube"]
      quality: ["Great Expectations", "dbt Tests", "Soda", "Elementary", "Monte Carlo", "Datafold", "Data Contracts"]
      governance: ["DataHub", "OpenMetadata", "Amundsen", "Atlan", "Collibra", "Lineage", "PII", "GDPR", "RBAC"]
      infra: ["AWS", "GCP", "Azure", "Kubernetes", "Docker", "Terraform", "Pulumi", "ArgoCD", "GitHub Actions", "FinOps"]
  taleo:
    keywords: "SQL, Python, Spark, Airflow, dbt, Snowflake, BigQuery, Redshift, Databricks, Kafka, Data Lake, Data Warehouse, ETL, ELT, Data Modeling, Data Quality, Great Expectations, Kubernetes, Docker, AWS, Cloud, Terraform, CI/CD, GitHub, GitLab, Monitoring, Observability, Data Governance, Lineage, Catalog, Agile, Scrum"
    boolean: "("SQL" OR "Python" OR "Spark") AND ("Airflow" OR "Dagster" OR "Prefect" OR "Temporal" OR "dbt") AND ("Snowflake" OR "BigQuery" OR "Redshift" OR "Databricks") AND ("Kafka" OR "Flink" OR "CDC" OR "Debezium") AND ("AWS" OR "GCP" OR "Azure")"
---
## Role Summary

> **Data Engineer** — Builds reliable, scalable data platforms. Owns ingestion → transformation → serving → governance. Expert in batch/stream processing, warehousing, orchestration, data quality, and governance. At Senior+ architects data platform; at Staff+ defines company-wide data strategy and governance.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### Data Platform & Ingestion (All Levels)
- Build **data ingestion pipelines**: **batch** (S3/GCS → **Spark/Databricks** → **Delta Lake/Iceberg/Hudi**), **streaming** (**Kafka/Flink/Redpanda/RisingWave** → **ClickHouse/Druid/Pinot**), **CDC** (**Debezium/Maxwell** → **Kafka** → **Warehouse**)
- Operate **cloud data platforms**: **AWS** (S3, Glue, Athena, Redshift, EMR, MSK, Kinesis), **GCP** (GCS, Dataflow, BigQuery, Pub/Sub, Composer), **Azure** (ADLS, Synapse, Fabric, Event Hubs)
- Implement **infrastructure as code**: **Terraform/Pulumi** (modules, workspaces, state management), **GitOps** (ArgoCD/Flux), **Kubernetes operators** (Spark, Airflow, Flink, Trino)
- Establish **CI/CD for data**: **GitHub Actions/GitLab CI** (dbt, SQLFluff, Great Expectations, Terraform), **environments**, **approval gates**, **automated rollback**

### Transformation & Modeling (Mid+)
- Develop **dbt projects**: **models** (staging, intermediate, marts), **tests** (generic, singular, packages), **contracts** (schema, SLA, deprecation), **packages**, **macros**, **semantic layer** (metrics, Cube/AtScale)
- Design **data models**: **Kimball** (star/snowflake, SCD Type 0-7), **Data Vault 2.0** (Hub/Link/Sat, PIT, Bridge), **Activity Schema** (event-based, temporal queries)
- Optimize **warehouse performance**: **Snowflake** (clustering, search optimization, materialized views, Snowpark), **BigQuery** (partitioning, clustering, BI Engine, slots), **Redshift** (RA3, dist/sort keys, Spectrum)
- Implement **data contracts**: **dbt Contracts/SQLMesh** (schema enforcement, SLA, ownership, breaking change detection, CI gates)

### Data Quality & Observability (Mid+)
- Establish **data testing**: **Great Expectations** (expectations, checkpoints, data docs), **dbt Tests**, **Soda** (SodaCL, anomaly detection), **Elementary** (dbt-native, freshness, schema, distribution)
- Implement **data observability**: **Monte Carlo/Datafold/Metaplane/Validio** (ML-powered anomaly detection, column-level lineage, root cause analysis, impact analysis)
- Define **freshness/SLA monitoring**: **dbt Freshness**, **Dagster Asset Observations**, **Airflow SLAs**, custom alerting (Looker, Metabase, Grafana, PagerDuty)
- Build **anomaly detection**: **statistical** (Z-score, IQR, seasonal decomposition), **ML-based** (Isolation Forest, Prophet), **threshold vs learned**

### Data Governance & Catalog (Senior+)
- Deploy **data catalog**: **DataHub/OpenMetadata/Amundsen/Atlan/Collibra/Alation/Purview** (metadata, lineage, search, ownership, glossary)
- Implement **column-level lineage**: **OpenLineage/DataHub/Datafold/dbt** (cross-system: Spark→Snowflake→Looker, impact analysis, root cause)
- Enforce **privacy/compliance**: **PII detection** (AWS Macie, GCP DLP, Azure Purview), **tagging**, **masking**, **tokenization**, **encryption**, **GDPR/CCPA/HIPAA**
- Configure **access control**: **RBAC/ABAC** (Snowflake/BigQuery/Redshift/Databricks), **dynamic masking**, **row/column-level security**, **data sharing**

### Streaming & Real-Time (Senior+)
- Build **real-time pipelines**: **Flink SQL/ksqlDB/RisingWave/Materialize** (event time, watermarks, exactly-once, state backend, savepoints)
- Implement **CDC**: **Debezium** (MySQL/Postgres/MongoDB/SQL Server/Oracle, log-based, non-intrusive, schema evolution)
- Serve **low-latency analytics**: **ClickHouse/Druid/StarRocks/Doris/Pinot** (columnar, vectorized, materialized views, aggregations)
- Operate **event streaming**: **Kafka** (topics, partitions, retention, compaction, quotas, tiered storage), **Schema Registry** (Avro/Protobuf/JSON, compatibility)

### Strategy & Leadership (Staff+)
- Define **data platform strategy**: **build vs. buy**, **vendor evaluation**, **multi-year roadmap**, **cost optimization** (FinOps, attribution, anomaly detection)
- Build **self-serve data platform**: **500+ pipelines**, **100+ analysts**, **SLA 99.9%**, **cost/query <$0.01**, **sub-minute freshness for critical datasets**
- Lead **data governance program**: **data contracts**, **quality gates**, **ownership model**, **compliance** (SOC2, GDPR, HIPAA), **data mesh** (domain ownership, product thinking)
- Grow **data engineering org**: **hiring bar**, **career ladder**, **mentoring**, **tech talks**, **open source** (Airflow, dbt, Spark, Iceberg contributors)

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
- **SQL**, **Python**, **Spark**, **Airflow**, **dbt**
- **Snowflake**, **BigQuery**, **Redshift**, **Databricks**
- **Kafka**, **Data Lake**, **Data Warehouse**, **ETL**, **ELT**
- **Data Modeling**, **Data Quality**, **Great Expectations**, **dbt Tests**
- **Data Governance**, **Data Catalog**, **Lineage**
- **Kubernetes**, **Docker**, **AWS**, **Terraform**, **CI/CD**, **GitHub Actions**, **Observability**

### Strong Signal (Differentiators)
- **Flink**, **Delta Lake**, **Iceberg**, **Hudi**, **Debezium**, **CDC**
- **Dagster**, **Prefect**, **Temporal**, **ClickHouse**, **Druid**, **DataHub**, **OpenMetadata**
- **Monte Carlo**, **Datafold**, **Soda**, **Elementary**, **dbt Contracts**, **SQLMesh**
- **GCP**, **Azure**, **GitLab CI**, **ArgoCD**, **FinOps**

### Nice-to-Have (Specialization)
- **Redpanda**, **RisingWave**, **Materialize**, **Bytewax**, **Trino**, **Presto**, **DuckDB**, **StarRocks**, **Doris**, **Pinot**
- **Polars**, **Dask**, **Ray**, **dbt Semantic Layer**, **Cube**, **AtScale**, **LookML**, **OpenLineage**, **Pulumi**, **Crossplane**, **KEDA**, **Data Contracts**

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Junior (0-2 yrs)
- **Built** **ETL pipelines** (**Python**, **SQL**, **Airflow**) ingesting **10+ sources** → **Snowflake**; **latency <1hr**, **99% success rate**
- **Developed** **dbt models** (staging/marts); **wrote** **100+ tests** (unique, not_null, relationships, accepted_values); **coverage 85%**
- **Configured** **Great Expectations** checkpoints; **validated** **50+ tables**; **documented** **data quality reports** in **Data Docs**
- **Implemented** **CDC** via **Debezium** (MySQL → Kafka); **handled** **schema evolution** (Avro, backward compatibility)
- **Automated** **CI/CD** (**GitHub Actions**): **dbt parse/test**, **SQLFluff lint**, **Terraform plan/apply**; **PR gates** on **data quality**

### Mid (2-5 yrs)
- **Owned** **core data platform**: **ingestion → transformation → serving** for **200+ pipelines**, **50+ analysts**, **10TB/day**, **99.9% uptime**
- **Migrated** **legacy ETL** (Informatica/Talend) → **modern stack** (dbt, Airflow, Snowflake); **cut runtime 60%**, **cost 40%**, **onboarded 10 new sources**
- **Designed** **data models** (**Kimball** star schema, **SCD Type 2**); **implemented** **dbt semantic layer** (metrics, Cube); **enabled self-serve BI**
- **Built** **streaming pipeline** (**Flink**, **Kafka** → **ClickHouse**); **p99 latency <500ms**, **1M events/sec**, **exactly-once**
- **Deployed** **data observability** (**Monte Carlo**, **Datafold**); **column-level lineage**; **reduced incident MTTR 70%** (root cause in <15min)
- **Established** **data contracts** (**dbt Contracts**); **schema enforcement** in CI; **prevented 50+ breaking changes**/quarter

### Senior (5-8 yrs)
- **Architected** **lakehouse platform**: **S3/ADLS** → **Delta Lake/Iceberg** → **Spark/Databricks/Trino** → **Snowflake/BigQuery**; **open formats**, **ACID**, **time travel**
- **Led** **data mesh transformation**: **domain-oriented ownership**, **data products**, **self-serve infra**, **federated governance**; **onboarded 10 domains**
- **Optimized** **warehouse costs**: **Snowflake/BigQuery/Redshift** (query tuning, materialization, clustering, slot management); **cut spend 35%**, **$2M/yr saved**
- **Built** **real-time analytics**: **Flink SQL** + **RisingWave** + **ClickHouse**; **sub-second dashboards**, **10M events/sec**, **99.99% availability**
- **Implemented** **governance at scale**: **DataHub** (catalog, lineage, ownership), **PII detection** (Macie/DLP), **RBAC/column-level security**, **SOC2/GDPR ready**
- **Mentored** **10+ engineers**; **defined career ladder**; **raised hiring bar**; **tech lead** for **platform team**; **open source** (Airflow, dbt, Iceberg contributor)

### Staff (8-12 yrs)
- **Defined** **company-wide data strategy**: **multi-year roadmap**, **build vs. buy** (Fivetran/Airbyte vs custom, Monte Carlo vs build), **vendor contracts** ($5M+)
- **Built** **centralized data platform** serving **500+ pipelines**, **200+ analysts**, **100TB/day**, **SLA 99.99%**, **cost/query <$0.01**
- **Led** **data governance program**: **data contracts**, **quality SLAs**, **ownership model**, **compliance** (SOC2, GDPR, HIPAA, CCPA), **data mesh** at scale
- **Drove** **FinOps**: **cost attribution** (team/project/query), **anomaly detection**, **optimization** (rightsizing, reservations, serverless); **$5M/yr saved**
- **Grew** **data org** 20→100; **dual-track IC/Manager**; **industry hiring bar**; **conference keynotes**; **Airflow/dbt/Iceberg PMC/maintainer**
- **Advised** **C-suite** on **data investment** ($50M+); **board presentations**; **M&A data due diligence**

### Principal (12+ yrs)
- **Industry vision**: **data platform trends** (lakehouse, data mesh, AI-ready data, semantic layer, data contracts), **standards** (OpenLineage, Iceberg, Substrait)
- **Recognition**: **Fellow**, **Keynotes** (Data Council, Kafka Summit, dbt Coalesce), **Papers** (VLDB, SIGMOD, CIDR), **Patents**, **Advisory Boards**
- **Crisis leadership**: **data breach response**, **platform outage**, **regulatory audit**, **cost overrun**, **talent retention**
- **Transforms org**: **centralizes data**, **changes culture** (data as product, quality mindset, ownership), **builds data literacy** at scale

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `sql`, `python`, `spark`, `airflow`, `dbt`, `snowflake`, `bigquery`, `redshift`, `databricks`, `kafka`, `data lake`, `data warehouse`, `etl`, `elt`, `data modeling`, `data quality`, `great expectations`, `dbt tests`, `data governance`, `data catalog`, `lineage`, `kubernetes`, `docker`, `aws`, `terraform`, `ci/cd`, `github actions`, `observability`

### Lever
**Exact**: `sql`, `python`, `spark`, `airflow`, `dbt`, `snowflake`, `bigquery`, `redshift`, `databricks`, `kafka`, `data lake`, `data warehouse`, `etl`, `elt`, `data modeling`, `data quality`, `great expectations`, `dbt tests`, `data governance`, `data catalog`, `lineage`, `kubernetes`, `docker`, `aws`, `terraform`, `ci/cd`, `github actions`, `observability`

### Workday
**Exact (title case)**: `SQL`, `Python`, `Apache Spark`, `Apache Airflow`, `dbt`, `Snowflake`, `BigQuery`, `Redshift`, `Databricks`, `Apache Kafka`, `Data Lake`, `Data Warehouse`, `ETL`, `ELT`, `Data Modeling`, `Data Quality`, `Great Expectations`, `dbt Tests`, `Data Governance`, `Data Catalog`, `Lineage`, `Kubernetes`, `Docker`, `Amazon Web Services`, `Terraform`, `Continuous Integration`, `GitHub Actions`, `Observability`

### iCIMS
**Skill clusters**:
```
processing: ["SQL", "Python", "Spark", "Flink", "Kafka", "Databricks", "EMR", "Dataflow"]
warehousing: ["Snowflake", "BigQuery", "Redshift", "Databricks SQL", "ClickHouse", "Druid", "Trino", "Iceberg", "Delta Lake", "Hudi"]
orchestration: ["Airflow", "Dagster", "Prefect", "Temporal", "dbt", "SQLMesh"]
modeling: ["Data Modeling", "Kimball", "Data Vault", "Activity Schema", "Semantic Layer", "dbt Metrics", "Cube"]
quality: ["Great Expectations", "dbt Tests", "Soda", "Elementary", "Monte Carlo", "Datafold", "Data Contracts"]
governance: ["DataHub", "OpenMetadata", "Amundsen", "Atlan", "Collibra", "Lineage", "PII", "GDPR", "RBAC"]
infra: ["AWS", "GCP", "Azure", "Kubernetes", "Docker", "Terraform", "Pulumi", "ArgoCD", "GitHub Actions", "FinOps"]
```

### Taleo
**Keywords**: `SQL, Python, Spark, Airflow, dbt, Snowflake, BigQuery, Redshift, Databricks, Kafka, Data Lake, Data Warehouse, ETL, ELT, Data Modeling, Data Quality, Great Expectations, Kubernetes, Docker, AWS, Cloud, Terraform, CI/CD, GitHub, GitLab, Monitoring, Observability, Data Governance, Lineage, Catalog, Agile, Scrum`
**Boolean**: `("SQL" OR "Python" OR "Spark") AND ("Airflow" OR "Dagster" OR "Prefect" OR "Temporal" OR "dbt") AND ("Snowflake" OR "BigQuery" OR "Redshift" OR "Databricks") AND ("Kafka" OR "Flink" OR "CDC" OR "Debezium") AND ("AWS" OR "GCP" OR "Azure")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: Data Platform Engineer (Scale-Ups, Enterprise Data Platforms)
**Keywords**: `data platform`, `lakehouse`, `delta lake`, `iceberg`, `hudi`, `databricks`, `spark`, `trino`, `self-serve`, `developer experience`, `data mesh`, `domain ownership`, `data products`, `federated governance`, `finops`, `cost optimization`, `sla`, `observability`, `monte carlo`, `datafold`, `data contracts`, `dbt contracts`, `sqlmesh`
**Mirror**: Lead with **platform impact** (pipelines, analysts, SLA, cost/query). Use `architected`, `built`, `standardized`, `enabled`, `governed`. Emphasize **leverage**, **self-serve**, **reliability**, **cost efficiency**, **open standards**.

### Archetype 2: Analytics Engineer (dbt-First, BI Enablement, Modern Stack)
**Keywords**: `analytics engineer`, `dbt`, `dbt cloud`, `dbt core`, `semantic layer`, `dbt metrics`, `cube`, `atscale`, `lookml`, `sqlmesh`, `data modeling`, `kimball`, `data vault`, `activity schema`, `testing`, `dbt tests`, `great expectations`, `soda`, `elementary`, `documentation`, `data docs`, `ci/cd`, `github actions`, `data contracts`, `self-serve analytics`
**Mirror**: Lead with **modeling depth**, **testing rigor**, **semantic layer**, **analyst enablement**. Use `designed`, `modeled`, `tested`, `documented`, `published`. Emphasize **business logic in code**, **contracts**, **governance**, **discovery**.

### Archetype 3: Streaming / Real-Time Data Engineer (High-Throughput, Low-Latency)
**Keywords**: `streaming`, `real-time`, `flink`, `kafka`, `ksqldb`, `risingwave`, `materialize`, `redpanda`, `cdc`, `debezium`, `clickhouse`, `druid`, `pinot`, `starrocks`, `doris`, `event-driven`, `exactly-once`, `event time`, `watermarks`, `state backend`, `savepoints`, `low latency`, `high throughput`, `sub-second`
**Mirror**: Lead with **technical depth**, **scale**, **latency/throughput**, **exactly-once**. Use `built`, `optimized`, `tuned`, `operated`, `debugged`. Emphasize **stateful processing**, **event time correctness**, **operational excellence**, **cost per event**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `dbt` / `dbt Tests` / `dbt Contracts` | JD requires modern transformation; missing | Add `dbt` project details: models, tests, contracts, packages, semantic layer, CI |
| `Snowflake` / `BigQuery` / `Redshift` / `Databricks` | JD requires warehouse; missing | Add warehouse experience: partitioning, clustering, optimization, Snowpark/BigLake |
| `Airflow` / `Dagster` / `Prefect` / `Temporal` | JD requires orchestration; missing | Add orchestrator: DAGs/assets, dynamic mapping, sensors, deferrable operators, GitOps |
| `Kafka` / `Flink` / `CDC` / `Debezium` | JD requires streaming; missing | Add streaming: Kafka topics, Flink jobs, CDC pipelines, exactly-once, schema registry |
| `Data Quality` / `Great Expectations` / `Monte Carlo` / `Datafold` | JD requires observability; missing | Add quality: expectations, checkpoints, anomaly detection, column-level lineage, MTTR |
| `Data Governance` / `Data Catalog` / `Lineage` / `PII` | JD requires governance; missing | Add catalog: DataHub/OpenMetadata, lineage, ownership, PII detection, masking, RBAC |
| `Terraform` / `Pulumi` / `ArgoCD` / `GitOps` | Platform JD; missing IaC | Add IaC: modules, workspaces, state, GitOps, Kubernetes operators, environments |
| `Delta Lake` / `Iceberg` / `Hudi` | Lakehouse JD; missing table formats | Add table format: ACID, time travel, schema evolution, partition evolution, Z-order |
| `Mentoring` / `Career Ladder` / `Hiring Bar` | Senior+ JD; missing | Add leadership: mentored N, defined ladder, raised bar, interviewed 100+, tech talks |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| **GitHub: Data Tool / Operator / dbt Package** | `Open Source`, `Python`, `SQL`, `dbt`, `Airflow`, `Kubernetes`, `Community`, `Downloads` | Projects, GitHub Link |
| **Technical Blog: Data Platform / Modeling / Quality** | `Technical Writing`, `Data Engineering`, `Lakehouse`, `dbt`, `Data Quality`, `Observability`, `Governance` | Writing, Portfolio Link |
| **Conference Talk (Data Council, dbt Coalesce, Kafka Summit, KubeCon)** | `Public Speaking`, `Thought Leadership`, `Data Platform`, `Streaming`, `Governance`, `Open Source` | Speaking, Leadership |
| **dbt / Airflow / Iceberg Contribution** | `Open Source`, `Contributor`, `Core`, `PMC`, `Maintainer`, `Community` | Projects, GitHub Link |
| **Internal Platform Adoption Case Study** | `Platform Engineering`, `Adoption Metrics`, `Developer Productivity`, `Cost Savings`, `Change Management` | Experience, Projects |
| **Data Contract / Model Card (Sanitized)** | `Data Governance`, `Data Contracts`, `Schema Enforcement`, `SLA`, `Ownership`, `Breaking Change Detection` | Experience, Projects |

---

## Role-Specific ATS Optimization Notes

### Red Flags (Auto-Reject)
- **Only "SQL / Tableau / Looker"** — no Python/Spark/Airflow → Analyst, not Data Engineer
- **No orchestration tool** (Airflow/Dagster/Prefect/Temporal) → Can't build pipelines
- **No warehouse** (Snowflake/BigQuery/Redshift/Databricks) → Platform gap
- **No data quality/observability** for Mid+ → Engineering maturity gap
- **No cloud/IaC** (AWS/GCP/Azure + Terraform) → Infrastructure gap
- **>2 pages for <5 yrs** → Format penalty
- **Tables/columns/graphics** → Parser extraction failure

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `SQL`, `Python`, `Spark`, `Airflow`, `dbt`, `Snowflake`, `BigQuery`, `Redshift`, `Databricks`, `Kafka`, `Data Lake`, `Data Warehouse`, `ETL`, `ELT`, `Data Modeling`, `Data Quality` |
| High | 1.5% | 3.0% | `Great Expectations`, `dbt Tests`, `Data Governance`, `Data Catalog`, `Lineage`, `Kubernetes`, `Docker`, `AWS`, `Terraform`, `CI/CD`, `GitHub Actions`, `Observability`, `Flink`, `Delta Lake`, `Iceberg`, `Hudi`, `Debezium`, `CDC` |
| Medium | 1.0% | 2.5% | `Dagster`, `Prefect`, `Temporal`, `ClickHouse`, `Druid`, `DataHub`, `OpenMetadata`, `Monte Carlo`, `Datafold`, `Soda`, `Elementary`, `dbt Contracts`, `SQLMesh`, `GCP`, `Azure`, `GitLab CI`, `ArgoCD`, `FinOps` |
| Low | 0.5% | 1.5% | `Redpanda`, `RisingWave`, `Materialize`, `Bytewax`, `Trino`, `Presto`, `DuckDB`, `StarRocks`, `Doris`, `Pinot`, `Polars`, `Dask`, `Ray`, `dbt Semantic Layer`, `Cube`, `AtScale`, `LookML`, `OpenLineage`, `Pulumi`, `Crossplane`, `KEDA`, `Data Contracts` |

### NDA Abstraction
- **L2**: "Enterprise data platform (500+ pipelines, 100TB/day) on AWS/Snowflake/Databricks"
- **L3**: "Cut warehouse spend 35% ($2M/yr) via query optimization and materialization strategy"
- **L4**: "Reduced data warehouse costs 35% ($2M annually) through optimization"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `data-science/data-engineer`
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 10 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for applications, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (scope/scale/latency), Tech Lead (architecture/warehouse tuning), Exec (cost savings/data trust)
- [ ] Metrics validated via `metric_plausibility.py` (pipeline latency, data freshness, warehouse cost/query, MTTR, test coverage, lineage coverage)
- [ ] Portfolio cross-refs: GitHub/blog/talks/contributions with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024