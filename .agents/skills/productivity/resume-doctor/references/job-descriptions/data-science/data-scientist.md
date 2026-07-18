---
role_id: "data-science/data-scientist"
canonical_title: "Data Scientist"
aliases: ["Applied Scientist", "ML Researcher", "Quantitative Analyst", "Analytics Engineer", "Decision Scientist"]
seniority_levels: ["Junior", "Mid", "Senior", "Staff", "Principal"]
related_roles: ["ml-engineer", "data-engineer", "analytics-engineer", "research-scientist"]
ats_keywords:
  - "Python"
  - "SQL"
  - "Machine Learning"
  - "Statistics"
  - "A/B Testing"
  - "Experimentation"
  - "PyTorch"
  - "TensorFlow"
  - "Scikit-learn"
  - "XGBoost"
  - "LightGBM"
  - "Pandas"
  - "NumPy"
  - "Feature Engineering"
  - "Model Deployment"
  - "MLOps"
  - "Docker"
  - "Kubernetes"
  - "AWS"
  - "GCP"
  - "Data Visualization"
  - "Tableau"
  - "Looker"
  - "Causal Inference"
  - "Time Series"
  - "NLP"
  - "Computer Vision"
  - "Recommendation Systems"
  - "Forecasting"
  - "Anomaly Detection"
  - "Model Monitoring"
  - "Data Storytelling"
  - "Stakeholder Communication"
ats_skills_taxonomy:
  core_ml:
    - "Supervised Learning: Regression, Classification, Ranking, XGBoost, LightGBM, CatBoost, Tabular DL (TabNet, FT-Transformer)"
    - "Unsupervised: Clustering (K-means, HDBSCAN), Dimensionality Reduction (PCA, UMAP, t-SNE), Anomaly Detection (Isolation Forest, Autoencoders)"
    - "Deep Learning: PyTorch, TensorFlow/Keras, JAX/Flax, Transformers, CNNs, RNNs, Attention, Diffusion Models"
    - "NLP: Transformers (BERT, GPT, T5, Llama), Tokenization, Fine-tuning, RAG, Embeddings, LLMs (OpenAI, Anthropic, Open Source)"
    - "Computer Vision: Detection (YOLO, DETR), Segmentation (SAM, Mask R-CNN), Classification (ViT, ConvNeXt), Generative (Stable Diffusion, GANs)"
    - "Time Series: Forecasting (Prophet, NeuralProphet, TFT, DeepAR), Anomaly Detection, Seasonal Decomposition, State Space Models"
    - "Recommendation: Collaborative Filtering (ALS, Matrix Factorization), Content-Based, Hybrid, Two-Tower, Session-Based, Bandits"
    - "Causal Inference: RCT, Diff-in-Diff, IV, Regression Discontinuity, Synthetic Control, Causal Forests, Double ML"
    - "RL/Bandits: Contextual Bandits (LinUCB, Thompson Sampling), Off-Policy Evaluation, RLHF, DPO, PPO"
  mlops_engineering:
    - "Model Training: Distributed (DDP, FSDP, DeepSpeed), Mixed Precision, Gradient Accumulation, Checkpointing"
    - "Experiment Tracking: MLflow, Weights & Biases, ClearML, Neptune, Comet, Dagshub"
    - "Feature Store: Feast, Tecton, Hopsworks, Databricks Feature Store (Offline/Online, Point-in-Time Correctness)"
    - "Model Registry: MLflow, Vertex AI, SageMaker, BentoML (Versioning, Staging, Lineage, Approval Gates)"
    - "Serving: TorchServe, Triton, BentoML, FastAPI, gRPC, TensorRT, ONNX Runtime, vLLM, TGI (Batch/Streaming/Real-time)"
    - "Monitoring: Evidently, WhyLabs, Arize, Fiddler, Prometheus/Grafana (Drift, Performance, Data Quality, Business Metrics)"
    - "Orchestration: Airflow, Dagster, Prefect, Temporal, Kubeflow Pipelines, Vertex AI Pipelines (DAGs, Retries, SLA)"
    - "CI/CD for ML: GitHub Actions/GitLab CI + DVC/CML, Automated Testing (Unit, Integration, Data/Schema, Model Quality)"
    - "Data Versioning: DVC, LakeFS, Delta Lake, Iceberg, Hudi (Time Travel, Branching, Reproducibility)"
    - "Infrastructure: Docker, Kubernetes (Kubeflow, KServe), AWS (SageMaker, Batch, EMR), GCP (Vertex AI, Dataflow), Azure ML"
  data_engineering:
    - "SQL: Advanced (Window Functions, CTEs, Recursive, Pivot/Unpivot, Lateral Join, Query Optimization, EXPLAIN ANALYZE)"
    - "Warehouses: Snowflake, BigQuery, Redshift, Databricks, ClickHouse, DuckDB (Columnar, Partitioning, Clustering, Materialized Views)"
    - "Processing: Spark (PySpark, Structured Streaming), Flink, Polars, DuckDB, Ray, Dask (Distributed, Out-of-Core)"
    - "Streaming: Kafka, Flink, Redpanda, RisingWave, Materialize (Event Time, Watermarks, Exactly-Once, State)"
    - "Orchestration: Airflow (Dynamic DAGs, TaskFlow, Deferrable Operators), Dagster (Software-Defined Assets), Prefect"
    - "Quality: Great Expectations, dbt Tests, Soda, Monte Carlo, Elementary (Freshness, Schema, Distribution, Referential Integrity)"
    - "Modeling: dbt (Models, Tests, Docs, Exposures, Metrics, Semantic Layer), SQLMesh, Dataform"
  statistics_experimentation:
    - "Frequentist: Hypothesis Testing (t-test, Chi-square, ANOVA, Permutation), Power Analysis, Sample Size, Multiple Testing (Bonferroni, BH, Holm)"
    - "Bayesian: A/B Testing (Beta-Binomial, Gaussian), Credible Intervals, Prior Elicitation, Posterior Predictive Checks, Decision Rules"
    - "Sequential: SPRT, mSPRT, Always Valid Inference, Group Sequential, Alpha Spending (O'Brien-Fleming, Pocock)"
    - "Quasi-Experimental: Diff-in-Diff, Synthetic Control, Causal Impact, IV, RDD, Matching, Propensity Score, Double ML"
    - "Variance Reduction: CUPED, CUPAC, Control Variates, Stratification, Triggering, Post-Stratification"
    - "Guardrails: Sample Ratio Mismatch, Network Effects, Interference, Novelty Effects, Carryover, Multiple Metrics"
  communication_product:
    - "Data Storytelling: Narrative Structure, Visual Hierarchy, Cognitive Load, Audience Adaptation (Exec vs. Tech)"
    - "Visualization: Plotly, Matplotlib, Seaborn, Altair, Vega-Lite, Observable, Tableau, Looker, Superset, Streamlit"
    - "Reporting: Jupyter/Quarto, Notebooks → PDF/HTML/Slides, Parameterized Reports, Automated Dashboards"
    - "Stakeholder Management: Translating Business Questions → ML Problems, Setting Expectations, Managing Uncertainty"
    - "Documentation: Model Cards, Data Cards, System Cards, Risk Assessments, Fairness/Bias Audits, Model Documentation"
seniority_signals:
  junior:
    - "Cleans, explores, and analyzes data with Python/SQL; builds baseline models"
    - "Implements ML pipelines under guidance; writes unit tests for data/transforms"
    - "Runs A/B tests; computes p-values, confidence intervals; presents findings"
    - "Creates visualizations and dashboards (Tableau, Looker, Streamlit) for stakeholders"
    - "Documents work in Jupyter/Quarto; participates in code reviews; learns MLOps tools"
  mid:
    - "Owns ML projects end-to-end: problem framing → data → modeling → deployment → monitoring"
    - "Designs experiments: power analysis, randomization, guardrails, sequential analysis"
    - "Builds production ML systems: feature engineering, model training, serving, CI/CD"
    - "Applies causal inference: diff-in-diff, IV, synthetic control for observational studies"
    - "Optimizes models: hyperparameter tuning, distillation, quantization, ONNX/TensorRT"
    - "Mentors juniors; improves team standards: code quality, reproducibility, documentation"
    - "Collaborates with Product/Eng on feature design; translates business needs to ML specs"
  senior:
    - "Defines ML strategy for business domain: identifies high-ROI opportunities, builds roadmap"
    - "Architects ML platform: feature store, model registry, serving infra, monitoring, governance"
    - "Leads complex initiatives: ranking/recommendation systems, LLM fine-tuning, real-time personalization"
    - "Establishes experimentation culture: platform, stats rigor, self-serve, velocity + quality"
    - "Drives model governance: bias/fairness audits, model cards, regulatory compliance (EU AI Act)"
    - "Mentors Senior DS; grows Staff DS; defines career ladder; raises hiring bar"
    - "Partners with EM/PM on resourcing, prioritization, technical debt, platform investment"
    - "Publishes/applies research: NeurIPS/ICML/ICLR/KDD; open source contributions; patents"
  staff:
    - "Sets company-wide ML/AI strategy aligned with business; multi-year roadmap"
    - "Builds centralized ML platform serving 100+ models; defines standards, SLAs, cost optimization"
    - "Leads high-stakes ML: fraud detection ($1B+ protected), recommendation (revenue-critical), LLM platform"
    - "Grows Staff+ DS cohort; defines IC/Manager tracks; industry hiring bar"
    - "Influences C-suite on AI investment; presents to board; M&A technical due diligence"
    - "Represents company: keynotes, papers, open source leadership, standards bodies"
  principal:
    - "Company-wide AI/ML vision; long-term research agenda; competitive differentiation"
    - "Industry recognition: Fellow, Keynotes, Patents, Editorial Boards, Standards (IEEE, ISO)"
    - "Crisis leadership: model failures, regulatory response, reputational risk"
    - "Transforms org: builds research lab, centralizes ML, changes culture at scale"
ats_weight_hints:
  must_have:
    - "Python"
    - "SQL"
    - "Machine Learning"
    - "Statistics"
    - "A/B Testing"
    - "Experimentation"
    - "PyTorch"
    - "TensorFlow"
    - "Scikit-learn"
    - "Pandas"
    - "NumPy"
    - "Feature Engineering"
    - "Model Deployment"
    - "MLOps"
    - "Docker"
    - "Data Visualization"
    - "Tableau"
    - "Looker"
    - "Causal Inference"
    - "Time Series"
  strong_signal:
    - "XGBoost"
    - "LightGBM"
    - "PyTorch"
    - "TensorFlow"
    - "MLflow"
    - "Kubernetes"
    - "AWS"
    - "GCP"
    - "SageMaker"
    - "Vertex AI"
    - "Feature Store"
    - "Model Monitoring"
    - "Evidently"
    - "NLP"
    - "Transformers"
    - "LLM"
    - "Recommendation Systems"
    - "Forecasting"
    - "Anomaly Detection"
    - "Mentoring"
    - "Code Review"
  nice_to_have:
    - "JAX"
    - "Flax"
    - "Ray"
    - "Dask"
    - "Polars"
    - "DuckDB"
    - "Iceberg"
    - "Delta Lake"
    - "dbt"
    - "Dagster"
    - "Prefect"
    - "Temporal"
    - "vLLM"
    - "TGI"
    - "RLHF"
    - "DPO"
    - "Causal Forests"
    - "Double ML"
ats_parser_hints:
  greenhouse:
    - "python"
    - "sql"
    - "machine learning"
    - "statistics"
    - "a/b testing"
    - "experimentation"
    - "pytorch"
    - "tensorflow"
    - "scikit-learn"
    - "pandas"
    - "numpy"
    - "feature engineering"
    - "model deployment"
    - "mlops"
    - "docker"
    - "kubernetes"
    - "aws"
    - "gcp"
    - "data visualization"
    - "tableau"
    - "looker"
    - "causal inference"
    - "time series"
  lever:
    - "python"
    - "sql"
    - "machine learning"
    - "statistics"
    - "a/b testing"
    - "experimentation"
    - "pytorch"
    - "tensorflow"
    - "sklearn"
    - "pandas"
    - "numpy"
    - "feature engineering"
    - "mlops"
    - "docker"
    - "kubernetes"
    - "aws"
    - "gcp"
    - "visualization"
    - "tableau"
    - "looker"
    - "causal inference"
    - "time series"
  workday:
    - "Python"
    - "SQL"
    - "Machine Learning"
    - "Statistics"
    - "A/B Testing"
    - "Experimentation"
    - "PyTorch"
    - "TensorFlow"
    - "Scikit-learn"
    - "Pandas"
    - "NumPy"
    - "Feature Engineering"
    - "Model Deployment"
    - "MLOps"
    - "Docker"
    - "Kubernetes"
    - "Amazon Web Services"
    - "Google Cloud Platform"
    - "Data Visualization"
    - "Tableau"
    - "Looker"
    - "Causal Inference"
    - "Time Series"
  icims:
    skill_clusters:
      ml_core: ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "XGBoost", "LightGBM", "Pandas", "NumPy"]
      mlops: ["MLflow", "Kubeflow", "Docker", "Kubernetes", "AWS SageMaker", "GCP Vertex AI", "Model Serving", "Monitoring"]
      data: ["SQL", "Snowflake", "BigQuery", "Redshift", "Spark", "Airflow", "dbt", "Feature Store"]
      stats: ["A/B Testing", "Experimentation", "Causal Inference", "Bayesian", "Power Analysis", "Sequential Testing"]
      communication: ["Data Visualization", "Tableau", "Looker", "Jupyter", "Streamlit", "Storytelling", "Stakeholder Management"]
      domains: ["NLP", "Computer Vision", "Time Series", "Recommendation", "Forecasting", "Anomaly Detection", "LLM"]
---
## Role Summary

> **Data Scientist** — Translates business problems into measurable ML solutions. Owns the full lifecycle: problem framing, data preparation, modeling, evaluation, deployment, monitoring. Combines statistical rigor with engineering discipline. Communicates uncertainty and impact to stakeholders. At Senior+ defines ML strategy and platform; at Staff+ sets company-wide AI direction.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### Modeling & Experimentation (All Levels)
- Build **production ML models**: **XGBoost/LightGBM/CatBoost** (tabular), **PyTorch/TensorFlow** (deep learning), **Transformers** (NLP/LLM)
- Design and run **rigorous experiments**: **power analysis**, **randomization**, **guardrail metrics**, **sequential testing** (SPRT/mSPRT), **variance reduction** (CUPED)
- Apply **causal inference**: **Diff-in-Diff**, **Synthetic Control**, **IV**, **Regression Discontinuity**, **Double ML**, **Causal Forests** for observational studies
- Develop **specialized solutions**: **Recommendation** (Two-Tower, SASRec, Bandits), **Forecasting** (TFT, DeepAR, Prophet), **Anomaly Detection** (Isolation Forest, VAE), **NLP** (RAG, Fine-tuning, RLHF/DPO)
- Implement **model optimization**: **distillation**, **quantization** (INT8/INT4), **ONNX/TensorRT**, **vLLM/TGI** for LLM serving

### MLOps & Engineering (Mid+)
- Build **end-to-end ML pipelines**: **Airflow/Dagster/Prefect** orchestration, **Feast/Tecton** feature store, **MLflow/W&B** experiment tracking
- Implement **model serving**: **Triton/TorchServe/BentoML/FastAPI**, **batch/streaming/real-time**, **gRPC/REST**, **autoscaling**, **canary deployment**
- Establish **monitoring**: **Evidently/WhyLabs/Arize** (data drift, concept drift, performance degradation, business metric alerting)
- Enable **CI/CD for ML**: **GitHub Actions + CML/DVC**, automated testing (data/schema/model quality), **reproducibility** (DVC/LakeFS/Delta Lake)
- Manage **infrastructure**: **Docker**, **Kubernetes (Kubeflow/KServe)**, **AWS SageMaker**, **GCP Vertex AI**, **cost optimization** (spot, right-sizing)

### Data & Analytics (All Levels)
- Write **advanced SQL**: window functions, CTEs, recursive, lateral joins, query optimization (`EXPLAIN ANALYZE`), partitioning/clustering
- Work with **modern warehouses**: **Snowflake/BigQuery/Redshift/Databricks/ClickHouse/DuckDB** (columnar, materialized views, time travel)
- Process **large-scale data**: **Spark/Polars/Dask/Ray** (distributed, out-of-core), **Kafka/Flink** (streaming, event-time, exactly-once)
- Build **analytics foundations**: **dbt** (models, tests, docs, semantic layer), **data quality** (Great Expectations, Soda, Monte Carlo)

### Strategy & Leadership (Senior+)
- Define **ML roadmap**: identify high-ROI opportunities, estimate effort/impact, sequence investments, manage portfolio risk
- Architect **ML platform**: feature store, model registry, serving, monitoring, governance — **self-serve for 50+ data scientists**
- Lead **cross-functional initiatives**: ranking overhaul, LLM platform, real-time personalization, fraud detection modernization
- Establish **experimentation culture**: platform, stats rigor (Bayesian/Sequential), self-serve tools, velocity + quality gates
- Drive **model governance**: **bias/fairness audits**, **model cards**, **regulatory compliance** (EU AI Act, SR 11-7), **risk assessments**
- Mentor **Senior DS**; grow **Staff DS**; define **career ladder**; raise **hiring bar**; publish **research** (NeurIPS/ICML/KDD)

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
- **Python**, **SQL**, **Machine Learning**, **Statistics**, **A/B Testing**, **Experimentation**
- **PyTorch**, **TensorFlow**, **Scikit-learn**, **Pandas**, **NumPy**
- **Feature Engineering**, **Model Deployment**, **MLOps**, **Docker**
- **Data Visualization**, **Tableau**, **Looker** (or equivalent)
- **Causal Inference**, **Time Series** (domain-adaptive)

### Strong Signal (Differentiators)
- **XGBoost**, **LightGBM**, **MLflow**, **Kubernetes**, **AWS**, **GCP**, **SageMaker**, **Vertex AI**
- **Feature Store**, **Model Monitoring**, **Evidently**, **NLP**, **Transformers**, **LLM**, **Recommendation Systems**
- **Forecasting**, **Anomaly Detection**, **Mentoring**, **Code Review**, **dbt**, **Airflow**, **Spark**

### Nice-to-Have (Specialization Signals)
- **JAX/Flax**, **Ray/Dask**, **Polars/DuckDB**, **Iceberg/Delta Lake**, **dbt/Dagster/Prefect/Temporal**
- **vLLM/TGI**, **RLHF/DPO**, **Causal Forests**, **Double ML**, **Bayesian Optimization**, **AutoML**

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Junior (0-2 yrs)
- **Built** **baseline classification model** (XGBoost, **AUC 0.87**) for churn prediction; **deployed** via **FastAPI/Docker**
- **Analyzed** **10M+ events** in **SQL/Python**; **identified** **top 5 drivers** of conversion drop-off
- **Ran** **A/B tests** (n=50K/group); **computed** p-values, CIs; **presented** findings to Product
- **Created** **Tableau/Looker dashboards** tracking **KPIs** (DAU, retention, revenue); **automated** weekly reports
- **Implemented** **data validation** (Great Expectations); **caught** **schema drift** before production impact

### Mid (2-5 yrs)
- **Owned** **recommendation system** (Two-Tower, **15% CTR lift**, **$2M+ incremental ARR**); **end-to-end**: data → serving → monitoring
- **Designed** **experimentation framework**: **sequential testing**, **CUPED**, **guardrails**; **increased** test velocity **3x**
- **Built** **feature store** (Feast) serving **50+ models**; **reduced** feature computation latency **80%**
- **Applied** **causal inference** (Diff-in-Diff, Synthetic Control) to **measure** **marketing incrementality**; **saved $500K** wasted spend
- **Optimized** **LLM inference**: **vLLM + quantization (INT4)**; **cut** latency **60%**, **cost 70%** at same quality
- **Mentored** **2 junior DS**; **established** **code review standards**; **improved** **reproducibility** (DVC, pinned deps)

### Senior (5-8 yrs)
- **Defined** **ML strategy** for **marketplace ranking** ($500M GMV); **roadmap**: 3 pillars, 12 quarters, **projected 15% revenue lift**
- **Architected** **centralized ML platform** (Feature Store, Registry, Serving, Monitoring) serving **100+ models**, **10K req/s**
- **Led** **LLM fine-tuning** (Llama-3-70B, **DPO/RLHF**) for **customer support**; **automated 40% tickets**, **CSAT +15**
- **Established** **experimentation culture**: **self-serve platform**, **Bayesian/sequential stats**, **200+ tests/qtr**, **rigor + speed**
- **Drove** **model governance**: **bias audits** (disparate impact <1.25), **model cards**, **EU AI Act readiness**
- **Partnered** with **EM/PM** on **resourcing**; **grew** **DS team 5→15**; **defined** **IC track**; **hired** **Staff DS**

### Staff (8-12 yrs)
- **Set** **company-wide AI strategy** aligned with **$10B+ market cap**; **multi-year roadmap**: GenAI, Ranking, Forecasting
- **Built** **ML platform** serving **500+ models**; **standardized** SLAs (p99 <100ms), **cost/model <$50/mo**, **99.9% uptime**
- **Led** **fraud detection modernization** (Graph Neural Nets + Real-time Features); **prevented $1B+ fraud** annually
- **Grew** **Staff+ DS cohort 3→12**; **defined** **dual-track IC/Manager**; **industry hiring bar**; **NeurIPS/ICML papers**
- **Advised** **C-suite** on **AI investment** ($100M+); **presented** to **board**; **M&A technical due diligence**
- **Open source leadership**: **core contributor** (PyTorch, vLLM, Feast); **10M+ downloads**; **keynotes**

### Principal (12+ yrs)
- **Defined** **company AI vision**; **long-term research agenda**; **competitive moat** via **proprietary models/data**
- **Industry recognition**: **ACM/IEEE Fellow**, **Keynotes** (NeurIPS, KDD), **Patents** (50+), **Editorial Boards**
- **Crisis leadership**: **model failure response**, **regulatory engagement** (EU AI Act, White House EO), **reputation management**
- **Transformed** **org**: **built research lab** (50 researchers), **centralized ML** (200→500 DS), **culture change** at scale

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `python`, `sql`, `machine learning`, `statistics`, `a/b testing`, `experimentation`, `pytorch`, `tensorflow`, `scikit-learn`, `pandas`, `numpy`, `feature engineering`, `model deployment`, `mlops`, `docker`, `kubernetes`, `aws`, `gcp`, `data visualization`, `tableau`, `looker`, `causal inference`, `time series`
**Stemming**: `deploy`→`deployed`/`deploying`, `optimize`→`optimized`/`optimizing`, `experiment`→`experimented`/`experimenting`
**Fuzzy**: `mlops`≈`ml ops`, `a/b testing`≈`ab testing`≈`experimentation`, `feature store`≈`feast`≈`tecton`

### Lever
**Exact**: `python`, `sql`, `machine learning`, `statistics`, `a/b testing`, `experimentation`, `pytorch`, `tensorflow`, `sklearn`, `pandas`, `numpy`, `feature engineering`, `mlops`, `docker`, `kubernetes`, `aws`, `gcp`, `visualization`, `tableau`, `looker`, `causal inference`, `time series`
**Normalization**: `xgboost`/`lightgbm`/`catboost`→`gradient boosting`, `mlflow`/`wandb`/`clearml`→`experiment tracking`

### Workday
**Exact (title case)**: `Python`, `SQL`, `Machine Learning`, `Statistics`, `A/B Testing`, `Experimentation`, `PyTorch`, `TensorFlow`, `Scikit-learn`, `Pandas`, `NumPy`, `Feature Engineering`, `Model Deployment`, `MLOps`, `Docker`, `Kubernetes`, `Amazon Web Services`, `Google Cloud Platform`, `Data Visualization`, `Tableau`, `Looker`, `Causal Inference`, `Time Series`

### iCIMS
**Skill clusters**:
```
ml_core: ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "XGBoost", "LightGBM", "Pandas", "NumPy"]
mlops: ["MLflow", "Kubeflow", "Docker", "Kubernetes", "AWS SageMaker", "GCP Vertex AI", "Model Serving", "Monitoring"]
data: ["SQL", "Snowflake", "BigQuery", "Redshift", "Spark", "Airflow", "dbt", "Feature Store"]
stats: ["A/B Testing", "Experimentation", "Causal Inference", "Bayesian", "Power Analysis", "Sequential Testing"]
communication: ["Data Visualization", "Tableau", "Looker", "Jupyter", "Streamlit", "Storytelling", "Stakeholder Management"]
domains: ["NLP", "Computer Vision", "Time Series", "Recommendation", "Forecasting", "Anomaly Detection", "LLM"]
```
**Weighting**: ml_core (0.3) + mlops (0.2) + data (0.15) + stats (0.15) + communication (0.1) + domains (0.1)

### Taleo
**Keywords**: `Python`, `SQL`, `Machine Learning`, `Statistics`, `R`, `PyTorch`, `TensorFlow`, `Scikit-learn`, `A/B Testing`, `Experiment`, `Model`, `Deploy`, `Docker`, `Kubernetes`, `AWS`, `Cloud`, `Visualization`, `Tableau`, `PowerBI`, `Agile`, `Scrum`, `Git`
**Boolean**: `("Python" OR "R") AND ("SQL" OR "BigQuery" OR "Snowflake") AND ("PyTorch" OR "TensorFlow" OR "Scikit-learn") AND ("A/B Testing" OR "Experiment") AND ("Docker" OR "Kubernetes" OR "Cloud")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: Applied ML / Product DS (Consumer, Marketplace, Ads, Recommender)
**Keywords**: `recommendation`, `ranking`, `personalization`, `ctr`, `cvr`, `gmV`, `revenue`, `a/b testing`, `experimentation`, `causal inference`, `bandits`, `reinforcement learning`, `two-tower`, `sasrec`, `real-time`, `feature store`, `mlops`, `model serving`, `latency`, `throughput`, `ab testing`, `statistical significance`, `power analysis`
**Mirror**: Lead with **business metrics moved** (CTR +X%, Revenue +Y%). Use `built`, `deployed`, `optimized`, `measured`. Emphasize **end-to-end ownership**, **experiment rigor**, **production scale**.

### Archetype 2: Research / Frontier ML (LLM, GenAI, Computer Vision, Speech)
**Keywords**: `llm`, `generative ai`, `transformer`, `bert`, `gpt`, `llama`, `fine-tuning`, `rlhf`, `dpo`, `rag`, `embeddings`, `vector database`, `pinecone`, `weaviate`, `milvus`, `vllm`, `tgi`, `quantization`, `distillation`, `neurips`, `icml`, `iclr`, `publications`, `patents`, `research`, `novel architecture`, `scaling laws`, `alignment`, `safety`, `red teaming`
**Mirror**: Lead with **technical novelty**, **publications**, **open source impact**. Use `pioneered`, `published`, `open-sourced`, `benchmarked`. Emphasize **research-to-production translation**, **scaling**, **efficiency**.

### Archetype 3: Analytics / Decision Science / Business DS (FinTech, HealthTech, B2B SaaS)
**Keywords**: `causal inference`, `incrementality`, `marketing mix modeling`, `mmm`, `attribution`, `ltv`, `cac`, `churn`, `retention`, `segmentation`, `cohort analysis`, `forecasting`, `demand planning`, `pricing optimization`, `experimentation`, `bayesian`, `stan`, `pymc`, `decision science`, `stakeholder management`, `data storytelling`, `tableau`, `looker`, `sql`, `python`, `r`
**Mirror**: Lead with **business decisions influenced**, **$ impact**. Use `measured`, `attributed`, `optimized`, `recommended`, `presented to exec`. Emphasize **statistical rigor**, **communication**, **cross-functional partnership**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `PyTorch` / `TensorFlow` | JD requires DL; resume has only sklearn | Add `PyTorch`/`TensorFlow`; describe 1+ DL project (architecture, data, results) |
| `MLflow` / `W&B` / `Experiment Tracking` | JD requires MLOps; missing | Add `MLflow`/`W&B`; describe experiment tracking, model registry, reproducibility |
| `Feature Store` / `Feast` / `Tecton` | JD requires; missing | Add `Feast`/`Tecton`; describe feature definitions, point-in-time correctness, online/offline |
| `Model Monitoring` / `Evidently` / `Drift Detection` | JD requires; missing | Add `Evidently`/`WhyLabs`/`Arize`; describe drift alerts, performance monitoring, retraining triggers |
| `Causal Inference` / `Diff-in-Diff` / `IV` | JD requires; resume has only A/B testing | Add `Causal Inference`, `Diff-in-Diff`, `Synthetic Control`, `IV`, `Double ML`; cite observational study |
| `LLM` / `RAG` / `Fine-tuning` / `RLHF` | GenAI JD; missing | Add `LLM Fine-tuning (LoRA/QLoRA)`, `RAG (Vector DB, Reranking)`, `RLHF/DPO`, `vLLM/TGI` |
| `Kubernetes` / `Kubeflow` / `KServe` | ML Platform JD; missing | Add `Kubernetes (Kubeflow, KServe)`, `Docker`, `Helm`; describe model serving, autoscaling |
| `Mentoring` / `Career Ladder` / `Hiring Bar` | Senior+ JD; missing | Add `Mentored N DS`, `Defined Career Ladder`, `Raised Hiring Bar`, `Interviewed 100+` |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| **Kaggle / Competition** (Top 1% / Gold) | `Competitive ML`, `Feature Engineering`, `Ensembling`, `Publication` | Projects, GitHub Link |
| **GitHub: ML Library / Tool** | `Open Source`, `Python`, `PyTorch`, `Community`, `Downloads`, `Contributors` | Projects, GitHub Link |
| **Research Papers** (NeurIPS/ICML/ICLR/KDD) | `Research`, `Publication`, `Peer Review`, `Novelty`, `Citations` | Publications, Google Scholar |
| **Technical Blog** (Distill, Towards Data Science, Personal) | `Technical Writing`, `Communication`, `MLOps`, `Best Practices`, `Tutorials` | Writing, Portfolio Link |
| **Conference Talk / Workshop** | `Public Speaking`, `Knowledge Sharing`, `Community`, `Thought Leadership` | Speaking, Leadership |
| **Model Card / System Card** (Sanitized) | `Model Governance`, `Bias Audit`, `Fairness`, `Documentation`, `Responsible AI` | Experience, Projects |
| **Internal ML Platform Adoption** | `Platform Engineering`, `Developer Experience`, `Adoption Metrics`, `Change Management` | Experience, Leadership |

---

## Role-Specific ATS Optimization Notes

### Red Flags (Auto-Reject)
- **Only "Pandas/SQL"** — no modeling keywords → Analyst, not Data Scientist
- **No deployment/MLOps** — "Jupyter only" → Can't productionize
- **No experiment statistics** (power, p-value, CI, sequential) → Rigor gap
- **Only accuracy/F1** — no business metrics (revenue, retention, CTR) → Impact gap
- **No causal inference** for Senior+ → Observational limitation
- **>2 pages for <5 yrs** → Format penalty
- **Tables/columns/graphics** → Parser extraction failure

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `Python`, `SQL`, `Machine Learning`, `Statistics`, `A/B Testing`, `PyTorch`, `TensorFlow`, `Feature Engineering`, `Model Deployment`, `MLOps` |
| High | 1.5% | 3.0% | `XGBoost`, `LightGBM`, `MLflow`, `Kubernetes`, `AWS`, `GCP`, `SageMaker`, `Vertex AI`, `Feature Store`, `Model Monitoring`, `Causal Inference`, `Time Series`, `NLP`, `LLM` |
| Medium | 1.0% | 2.5% | `Pandas`, `NumPy`, `Scikit-learn`, `Docker`, `Airflow`, `dbt`, `Snowflake`, `BigQuery`, `Tableau`, `Looker`, `Mentoring`, `Code Review` |
| Low | 0.5% | 1.5% | `JAX`, `Ray`, `Polars`, `DuckDB`, `Iceberg`, `Delta Lake`, `vLLM`, `TGI`, `RLHF`, `DPO`, `Causal Forests`, `Double ML` |

### NDA Abstraction
- **L2**: "Large-scale recommendation system (100M+ users, 1B+ events/day) on AWS/Kubernetes"
- **L3**: "Improved CTR 15% and revenue $5M+/yr via two-tower architecture and real-time feature store"
- **L4**: "Drove 15% CTR lift and $5M+ annual revenue through ranking model modernization"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `data-science/data-scientist`
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 10 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for applications, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (scope/scale/metrics), Tech Lead (architecture/tools), Exec (business impact/$)
- [ ] Metrics validated via `metric_plausibility.py` (statistical claims, cohort sizes, lift %s, p-values)
- [ ] Portfolio cross-refs: Kaggle/GitHub/Papers/Blog/Talks with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024