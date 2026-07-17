---
role_id: "data-science/ml-engineer"
canonical_title: "Machine Learning Engineer"
aliases: ["ML Engineer", "MLOps Engineer", "Applied ML Engineer", "ML Platform Engineer", "AI Engineer"]
seniority_levels: ["Junior", "Mid", "Senior", "Staff", "Principal"]
related_roles: ["data-scientist", "data-engineer", "software-engineer", "research-engineer", "devops-platform/devops-engineer"]
ats_keywords:
  - "Python"
  - "PyTorch"
  - "TensorFlow"
  - "MLOps"
  - "Model Deployment"
  - "Kubernetes"
  - "Docker"
  - "AWS"
  - "GCP"
  - "SageMaker"
  - "Vertex AI"
  - "MLflow"
  - "Kubeflow"
  - "Feature Store"
  - "Model Monitoring"
  - "Distributed Training"
  - "Model Optimization"
  - "ONNX"
  - "TensorRT"
  - "vLLM"
  - "TGI"
  - "LLM"
  - "Transformers"
  - "RAG"
  - "Fine-tuning"
  - "RLHF"
  - "DPO"
  - "CI/CD"
  - "GitHub Actions"
  - "Terraform"
  - "Observability"
  - "Evidently"
  - "Data Engineering"
  - "Spark"
  - "Airflow"
  - "dbt"
ats_skills_taxonomy:
  ml_frameworks:
    - "PyTorch: nn.Module, Autograd, DDP/FSDP/DeepSpeed, Mixed Precision, torch.compile, TorchScript, Export (ONNX, AOTInductor)"
    - "TensorFlow/Keras: tf.function, Distribution Strategies, TFX, SavedModel, TFLite, TFRT, XLA"
    - "JAX/Flax: JIT, pmap/vmap, SPMD, Pallas, Orbax, Equinox, Levanter, MaxText"
    - "Hugging Face: Transformers, Accelerate, PEFT (LoRA/QLoRA/DoRA), TRL (SFT/DPO/PPO), Optimum, Text-Generation-Inference"
    - "LLM Ecosystem: vLLM, TGI, SGLang, llama.cpp, ollama, LMDeploy, TensorRT-LLM, MLC-LLM (Quantization, Speculative Decoding, PagedAttention)"
  mlops_platform:
    - "Experiment Tracking: MLflow, Weights & Biases, ClearML, Neptune, Comet, Dagshub (Artifacts, Metrics, Params, Models, Lineage)"
    - "Model Registry: MLflow, Vertex AI, SageMaker, BentoML (Versioning, Staging, Aliases, Lineage, Approval Gates, Rollback)"
    - "Feature Store: Feast, Tecton, Hopsworks, Databricks FS (Offline/Online, Point-in-Time Correctness, Materialization, TTL)"
    - "Orchestration: Airflow, Dagster, Prefect, Temporal, Kubeflow Pipelines, Vertex AI Pipelines (DAGs, Caching, Retries, SLA)"
    - "Serving: Triton, TorchServe, BentoML, FastAPI, vLLM, TGI, SGLang (Batch/Streaming/Real-time, gRPC/REST, Autoscaling, Canary)"
    - "Monitoring: Evidently, WhyLabs, Arize, Fiddler, Prometheus/Grafana (Data Drift, Concept Drift, Performance, Business Metrics, Alerting)"
    - "Data Versioning: DVC, LakeFS, Delta Lake, Iceberg, Hudi (Time Travel, Branching, Reproducibility, Lineage)"
    - "CI/CD for ML: GitHub Actions/GitLab CI + CML/DVC, Automated Testing (Data/Schema/Model Quality), Gates (Metrics Thresholds)"
  distributed_training:
    - "Data Parallelism: DDP, FSDP (Full Shard, Hybrid Shard, State Dict), DeepSpeed (ZeRO-1/2/3, Offload, Pipeline Parallelism)"
    - "Model Parallelism: Tensor Parallel, Pipeline Parallel, Sequence Parallel, Expert Parallel (MoE), 3D Parallelism"
    - "Communication: NCCL, Gloo, MPI, RCCL (All-Reduce, All-Gather, Reduce-Scatter, Broadcast, P2P)"
    - "Optimization: Gradient Accumulation, Activation Checkpointing, Mixed Precision (FP16/BF16), Flash Attention, Kernel Fusion"
    - "Infrastructure: Slurm, Kubernetes (Kubeflow, Kueue, Volcano), Ray, MosaicML, AWS Batch, SageMaker Distributed"
  model_optimization:
    - "Quantization: PTQ (GPTQ, AWQ, SmoothQuant, OmniQuant), QAT, INT8/INT4/NF4/FP8, Calibration, Outlier Handling"
    - "Distillation: Knowledge Distillation (Logit, Feature, Attention), Sequence-Level, MiniLLM, GKD"
    - "Pruning: Magnitude, Movement, Wanda, SparseGPT, LoRAPrune (Structured/Unstructured, Global/Local)"
    - "Compilation: torch.compile, ONNX Runtime, TensorRT, TVM, XLA, MLC-LLM, IREE (Graph Capture, Kernel Tuning)"
    - "Speculative Decoding: Medusa, Eagle, Lookahead, Draft Models, Tree Attention, Acceptance Rate Optimization"
    - "Serving Optimization: PagedAttention, Continuous Batching, Prefix Caching, Chunked Prefill, Disaggregated Prefill"
  data_engineering_ml:
    - "Processing: Spark (PySpark, Structured Streaming), Polars, DuckDB, Ray Data, Dask (Distributed, Out-of-Core, Lazy)"
    - "Streaming: Kafka, Flink, Redpanda, RisingWave, Materialize (Event Time, Watermarks, Exactly-Once, State)"
    - "Warehouses: Snowflake, BigQuery, Redshift, Databricks, ClickHouse (Columnar, Partitioning, Clustering, MV)"
    - "Feature Engineering: Feast, Tecton, Chronon, Butterfree (Aggregations, Embeddings, Time Windows, PIT Correctness)"
    - "Data Quality: Great Expectations, dbt Tests, Soda, Monte Carlo, Elementary (Freshness, Schema, Distribution, RI)"
  llm_systems:
    - "RAG: Vector DB (Pinecone, Weaviate, Milvus, Qdrant, Chroma, PGVector), Embeddings (BGE, E5, Voyage, OpenAI), Reranking (Cohere, BGE, Jina), Chunking, Hybrid Search"
    - "Agents: LangChain, LangGraph, AutoGen, CrewAI, LlamaIndex, Semantic Kernel (Tools, Memory, Planning, Reflection, Multi-Agent)"
    - "Fine-tuning: LoRA/QLoRA/DoRA (PEFT), Full Fine-tuning (FSDP/DeepSpeed), DPO/PPO/KTO/ORPO (Alignment), SFT (Chat/Instruct)"
    - "Evaluation: LLM-as-Judge, Benchmarks (MMLU, GSM8K, HumanEval, MT-Bench, AlpacaEval), RAGAS, TruLens, DeepEval"
    - "Guardrails: NeMo Guardrails, Guardrails AI, Llama Guard, Prompt Injection, PII Detection, Hallucination Detection, Constitutional AI"
  infrastructure:
    - "Cloud: AWS (SageMaker, Batch, EC2, ECS/EKS, Inferentia/Trainium), GCP (Vertex AI, TPU, GKE), Azure (ML, AKS, NDv5)"
    - "Kubernetes: Kubeflow, KServe, Kueue, Volcano, Knative, Gateway API (Model Serving, Autoscaling, Canary, Multi-Model)"
    - "Compute: GPU (H100/A100/V100/T4), TPU (v4/v5), Trainium/Inferentia, NVLink/NVSwitch, RDMA/RoCE, Slurm"
    - "Storage: S3/GCS/Blob, EFS/FSx/Lustre/WEKA/JuiceFS (High-Throughput, Low-Latency, POSIX, S3 API)"
    - "Networking: VPC, Placement Groups, EFA, SR-IOV, DPDK, Container Networking (Cilium, Calico, CNI)"
seniority_signals:
  junior:
    - "Implements ML training pipelines under guidance; writes unit tests for data transforms and model components"
    - "Deploys models to staging/production via CI/CD; configures serving (Triton/TorchServe/FastAPI)"
    - "Runs hyperparameter tuning; logs experiments in MLflow/W&B; compares baselines"
    - "Optimizes inference: ONNX export, TensorRT, quantization (INT8); benchmarks latency/throughput"
    - "Participates in code reviews; learns MLOps tools (Airflow, Kubeflow, Feast); documents in markdown"
  mid:
    - "Owns ML services end-to-end: training → validation → deployment → monitoring → retraining"
    - "Builds MLOps pipelines: feature store (Feast), experiment tracking (MLflow), model registry, CI/CD (GitHub Actions + CML)"
    - "Implements distributed training: DDP/FSDP/DeepSpeed; scales to multi-node multi-GPU; optimizes throughput"
    - "Deploys LLM inference: vLLM/TGI; configures PagedAttention, continuous batching, prefix caching; benchmarks"
    - "Establishes model monitoring: Evidently/WhyLabs; drift alerts (data/concept), performance degradation, business metrics"
    - "Mentors juniors; improves team standards: code quality, reproducibility (DVC/LakeFS), testing, documentation"
    - "Collaborates with DS/Product on requirements; translates modeling needs to engineering specs"
  senior:
    - "Architects ML platform: feature store, model registry, serving infra, monitoring, governance — self-serve for 50+ ML practitioners"
    - "Leads LLM platform: fine-tuning (LoRA/FSDP), RAG (vector DB, reranking), evaluation (LLM-as-judge, RAGAS), guardrails"
    - "Optimizes training at scale: FSDP/DeepSpeed, 3D parallelism, activation checkpointing, flash attention, kernel fusion"
    - "Drives model optimization: quantization (GPTQ/AWQ/NF4), distillation, speculative decoding, compilation (torch.compile/TensorRT)"
    - "Establishes ML governance: model cards, bias/fairness audits, regulatory compliance (EU AI Act), risk assessments"
    - "Mentors Senior MLE; grows Staff MLE; defines career ladder; raises hiring bar; contributes to open source (vLLM, PyTorch, HF)"
    - "Partners with EM/PM on resourcing; prioritizes platform investment; balances feature vs. infrastructure work"
  staff:
    - "Defines company-wide ML/AI infrastructure strategy: multi-year roadmap, build vs. buy, vendor evaluation, cost optimization"
    - "Builds centralized ML platform serving 500+ models: standards, SLAs (p99 <100ms), cost/model <$50/mo, 99.9% uptime"
    - "Leads high-stakes ML: recommendation (revenue-critical), fraud ($1B+ protected), LLM platform (100B+ tokens/day)"
    - "Grows Staff+ MLE cohort; defines IC/Manager tracks; industry hiring bar; NeurIPS/ICML/KDD publications; patents"
    - "Influences C-suite on AI investment ($100M+); presents to board; M&A technical due diligence"
    - "Represents company: keynotes, CNCF/LF AI projects, standards bodies, open source leadership"
  principal:
    - "Company-wide AI infrastructure vision; long-term research agenda; competitive moat via proprietary systems"
    - "Industry recognition: Fellow, Keynotes, Patents (50+), Editorial Boards, Standards (MLCommons, ONNX, PyTorch)"
    - "Crisis leadership: model failures, GPU shortage, regulatory response (EU AI Act), reputational risk"
    - "Transforms org: builds research lab, centralizes ML platform, changes culture at scale"
ats_weight_hints:
  must_have:
    - "Python"
    - "PyTorch"
    - "TensorFlow"
    - "MLOps"
    - "Model Deployment"
    - "Kubernetes"
    - "Docker"
    - "AWS"
    - "MLflow"
    - "Feature Store"
    - "Model Monitoring"
    - "Distributed Training"
    - "Model Optimization"
    - "ONNX"
    - "TensorRT"
    - "CI/CD"
    - "GitHub Actions"
    - "Observability"
    - "Evidently"
  strong_signal:
    - "GCP"
    - "SageMaker"
    - "Vertex AI"
    - "Kubeflow"
    - "vLLM"
    - "TGI"
    - "LLM"
    - "Transformers"
    - "RAG"
    - "Fine-tuning"
    - "RLHF"
    - "DPO"
    - "LoRA"
    - "QLoRA"
    - "Flash Attention"
    - "FSDP"
    - "DeepSpeed"
    - "Spark"
    - "Airflow"
    - "dbt"
    - "Feast"
    - "Tecton"
  nice_to_have:
    - "JAX"
    - "Flax"
    - "Ray"
    - "Dask"
    - "Polars"
    - "DuckDB"
    - "Iceberg"
    - "Delta Lake"
    - "Temporal"
    - "Dagster"
    - "Prefect"
    - "SGLang"
    - "llama.cpp"
    - "MLC-LLM"
    - "NeMo Guardrails"
    - "Constitutional AI"
    - "SLSA"
    - "Sigstore"
ats_parser_hints:
  greenhouse:
    - "python"
    - "pytorch"
    - "tensorflow"
    - "mlops"
    - "model deployment"
    - "kubernetes"
    - "docker"
    - "aws"
    - "mlflow"
    - "feature store"
    - "model monitoring"
    - "distributed training"
    - "model optimization"
    - "onnx"
    - "tensorrt"
    - "ci/cd"
    - "github actions"
    - "observability"
    - "evidently"
  lever:
    - "python"
    - "pytorch"
    - "tensorflow"
    - "mlops"
    - "model deployment"
    - "kubernetes"
    - "docker"
    - "aws"
    - "mlflow"
    - "feature store"
    - "model monitoring"
    - "distributed training"
    - "model optimization"
    - "onnx"
    - "tensorrt"
    - "ci/cd"
    - "github actions"
    - "observability"
    - "evidently"
  workday:
    - "Python"
    - "PyTorch"
    - "TensorFlow"
    - "MLOps"
    - "Model Deployment"
    - "Kubernetes"
    - "Docker"
    - "Amazon Web Services"
    - "MLflow"
    - "Feature Store"
    - "Model Monitoring"
    - "Distributed Training"
    - "Model Optimization"
    - "ONNX"
    - "TensorRT"
    - "Continuous Integration"
    - "GitHub Actions"
    - "Observability"
    - "Evidently"
  icims:
    skill_clusters:
      ml_frameworks: ["Python", "PyTorch", "TensorFlow", "JAX", "Hugging Face", "Transformers", "Accelerate", "PEFT"]
      mlops: ["MLflow", "Kubeflow", "Docker", "Kubernetes", "AWS SageMaker", "GCP Vertex AI", "Model Serving", "Monitoring", "Feature Store"]
      training: ["Distributed Training", "DDP", "FSDP", "DeepSpeed", "Flash Attention", "Mixed Precision", "Gradient Accumulation"]
      optimization: ["Quantization", "GPTQ", "AWQ", "Distillation", "Pruning", "ONNX", "TensorRT", "torch.compile", "vLLM", "TGI"]
      data: ["Spark", "Airflow", "dbt", "Feast", "Tecton", "Snowflake", "BigQuery", "Kafka", "Flink", "Ray"]
      llm: ["LLM", "RAG", "Fine-tuning", "RLHF", "DPO", "LoRA", "QLoRA", "Vector Database", "Evaluation", "Guardrails"]
---
## Role Summary

> **Machine Learning Engineer** — Productionizes ML at scale. Bridges Data Science and Engineering: takes models from notebook to reliable, monitored, cost-effective services. Owns ML platform: training, deployment, monitoring, governance. Expert in distributed systems, GPU optimization, MLOps. At Senior+ architects ML platform; at Staff+ sets company-wide AI infrastructure strategy.

---

## Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

### ML Platform & MLOps (All Levels)
- Build **end-to-end MLOps pipelines**: **MLflow/W&B** (experiment tracking), **Feast/Tecton** (feature store), **Model Registry** (versioning, staging, lineage), **CI/CD** (GitHub Actions + CML/DVC, automated gates)
- Implement **model serving**: **Triton/TorchServe/BentoML/vLLM/TGI** (batch/streaming/real-time, gRPC/REST, autoscaling, canary, multi-model)
- Establish **model monitoring**: **Evidently/WhyLabs/Arize** (data drift, concept drift, performance degradation, business metric alerting, retraining triggers)
- Enable **reproducibility**: **DVC/LakeFS/Delta Lake/Iceberg** (data versioning, time travel, branching), **pinned dependencies**, **containerized environments**

### Distributed Training & Optimization (Mid+)
- Scale **distributed training**: **DDP/FSDP/DeepSpeed** (ZeRO-1/2/3, offload, pipeline parallelism), **3D parallelism** (tensor/pipeline/expert), **Flash Attention**, **activation checkpointing**, **mixed precision (BF16/FP8)**
- Optimize **model inference**: **quantization** (GPTQ, AWQ, SmoothQuant, NF4/FP8), **distillation** (logit/feature/attention), **pruning** (Wanda, SparseGPT), **compilation** (torch.compile, ONNX Runtime, TensorRT, TVM, MLC-LLM)
- Deploy **LLM inference at scale**: **vLLM/TGI/SGLang** (PagedAttention, continuous batching, prefix caching, chunked prefill, disaggregated prefill, speculative decoding)

### LLM Systems & GenAI (Senior+)
- Build **RAG pipelines**: vector DB (Pinecone/Weaviate/Milvus/Qdrant/PGVector), embeddings (BGE/E5/Voyage), reranking (Cohere/BGE/Jina), chunking strategies, hybrid search, evaluation (RAGAS, TruLens)
- Implement **fine-tuning**: **LoRA/QLoRA/DoRA** (PEFT), **full fine-tuning** (FSDP/DeepSpeed), **alignment** (DPO/PPO/KTO/ORPO), **SFT** (chat/instruct), **evaluation** (LLM-as-judge, MMLU, GSM8K, HumanEval, MT-Bench)
- Develop **agentic systems**: **LangGraph/LangChain/AutoGen/CrewAI/LlamaIndex** (tools, memory, planning, reflection, multi-agent), **guardrails** (NeMo, Guardrails AI, Llama Guard, prompt injection, PII, hallucination detection)

### Data Engineering for ML (All Levels)
- Process **large-scale ML data**: **Spark/Polars/DuckDB/Ray Data/Dask** (distributed, out-of-core, lazy), **Kafka/Flink/Redpanda** (streaming, event-time, exactly-once)
- Build **feature pipelines**: **Feast/Tecton/Chronon** (aggregations, embeddings, time windows, point-in-time correctness, materialization, TTL)
- Ensure **data quality**: **Great Expectations/dbt Tests/Soda/Monte Carlo** (freshness, schema, distribution, referential integrity, anomaly detection)

### Infrastructure & Cloud (Mid+)
- Provision **ML infrastructure**: **AWS SageMaker/Batch/EC2/EKS/Inferentia/Trainium**, **GCP Vertex AI/TPU/GKE**, **Azure ML/AKS/NDv5**
- Operate **Kubernetes for ML**: **Kubeflow/KServe/Kueue/Volcano/Knative** (model serving, autoscaling, canary, multi-model, gang scheduling)
- Optimize **compute & storage**: GPU (H100/A100), TPU, Trainium/Inferentia, NVLink, RDMA/RoCE, high-throughput storage (Lustre/WEKA/JuiceFS/FSx)

### Strategy & Leadership (Staff+)
- Define **ML platform strategy**: build vs. buy, vendor evaluation, cost optimization, multi-year roadmap, standards/SLAs
- Build **centralized ML platform** serving **500+ models**: self-serve, governance, cost/model <$50/mo, p99 <100ms, 99.9% uptime
- Lead **high-stakes ML**: recommendation (revenue-critical), fraud ($1B+ protected), LLM platform (100B+ tokens/day)
- Grow **Staff+ MLE cohort**; define **IC/Manager tracks**; **industry hiring bar**; **publications** (NeurIPS/ICML/KDD); **patents**
- Influence **C-suite on AI investment** ($100M+); present to **board**; **M&A technical due diligence**

---

## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
- **Python**, **PyTorch**, **TensorFlow**, **MLOps**, **Model Deployment**
- **Kubernetes**, **Docker**, **AWS** (or GCP/Azure)
- **MLflow**, **Feature Store**, **Model Monitoring**, **Distributed Training**, **Model Optimization**
- **ONNX**, **TensorRT**, **CI/CD**, **GitHub Actions**, **Observability**, **Evidently**

### Strong Signal (Differentiators)
- **SageMaker**, **Vertex AI**, **Kubeflow**, **vLLM**, **TGI**, **LLM**, **Transformers**, **RAG**, **Fine-tuning**, **RLHF**, **DPO**
- **LoRA/QLoRA**, **Flash Attention**, **FSDP**, **DeepSpeed**, **Spark**, **Airflow**, **dbt**, **Feast**, **Tecton**
- **Quantization (GPTQ/AWQ)**, **Distillation**, **Speculative Decoding**, **PagedAttention**

### Nice-to-Have (Specialization)
- **JAX/Flax**, **Ray/Dask**, **Polars/DuckDB**, **Iceberg/Delta Lake**, **Temporal/Dagster/Prefect**
- **SGLang**, **llama.cpp**, **MLC-LLM**, **NeMo Guardrails**, **Constitutional AI**, **SLSA/Sigstore**

---

## Seniority Signal Keywords (Verb/Metric Combos)

### Junior (0-2 yrs)
- **Implemented** **training pipeline** (PyTorch, DDP) for **image classification**; **deployed** via **Triton/Docker**; **latency <50ms**
- **Configured** **MLflow** experiment tracking; **logged** 200+ runs; **compared** baselines (ResNet, EfficientNet, ViT)
- **Exported** model to **ONNX**; **applied** **TensorRT INT8 quantization**; **achieved 3x speedup** on T4
- **Built** **CI/CD** (GitHub Actions + CML) for **automated testing** (data schema, model quality gates)
- **Participated** in **code reviews**; **documented** **MLOps runbooks** (deployment, rollback, monitoring)

### Mid (2-5 yrs)
- **Owned** **recommendation service** (Two-Tower, **Feast feature store**, **vLLM serving**); **end-to-end latency <100ms**, **99.9% uptime**
- **Built** **MLOps platform**: **MLflow** (tracking/registry), **Airflow** (orchestration), **Evidently** (monitoring), **GitHub Actions** (CI/CD gates)
- **Scaled** **distributed training** to **8 nodes × 8 A100** (FSDP, **ZeRO-3**, activation checkpointing); **throughput 500K samples/sec**
- **Deployed** **LLM inference** (Llama-3-70B, **vLLM**, **INT4 AWQ**); **p99 latency 200ms**, **throughput 50 tok/s/GPU**
- **Established** **model monitoring**: **data drift alerts** (PSI >0.2), **concept drift** (performance drop >5%), **auto-retraining triggers**
- **Mentored** **2 junior MLE**; **improved** **reproducibility**: **DVC**, **pinned deps**, **containerized envs**, **test coverage 85%**

### Senior (5-8 yrs)
- **Architected** **centralized ML platform** serving **100+ models**: **feature store**, **registry**, **serving**, **monitoring**, **governance** — **self-serve for 50+ practitioners**
- **Led** **LLM platform**: **fine-tuning** (LoRA/FSDP), **RAG** (Milvus, BGE, Cohere rerank), **evaluation** (LLM-as-judge, RAGAS), **guardrails** (NeMo)
- **Optimized** **training at scale**: **FSDP/DeepSpeed**, **3D parallelism**, **Flash Attention 2**, **kernel fusion**; **cut training time 40%**, **cost 30%**
- **Drove** **model optimization**: **quantization** (GPTQ/AWQ/NF4), **distillation**, **speculative decoding**, **torch.compile/TensorRT**; **inference cost -60%**
- **Established** **ML governance**: **model cards**, **bias audits** (disparate impact <1.25), **EU AI Act readiness**, **risk assessments**
- **Partnered** with **EM/PM** on **resourcing**; **grew MLE team 5→20**; **defined IC track**; **hiring bar**; **open source contributions** (vLLM, PyTorch)

### Staff (8-12 yrs)
- **Defined** **company-wide ML infrastructure strategy**: **multi-year roadmap**, **build vs. buy**, **vendor eval**, **cost optimization** ($10M+ GPU budget)
- **Built** **ML platform** serving **500+ models**: **standards**, **SLAs (p99 <100ms)**, **cost/model <$50/mo**, **99.9% uptime**, **multi-region**
- **Led** **high-stakes ML**: **recommendation** (15% revenue lift), **fraud** ($1B+ protected), **LLM platform** (100B+ tokens/day, 99.99% availability)
- **Grew** **Staff+ MLE cohort** 3→12; **defined dual-track IC/Manager**; **industry hiring bar**; **NeurIPS/ICML/KDD papers**; **patents**
- **Advised** **C-suite** on **AI investment** ($100M+); **presented to board**; **M&A technical due diligence**
- **Open source leadership**: **core maintainer** (vLLM, PyTorch, HF Transformers); **10M+ downloads**; **keynotes**

### Principal (12+ yrs)
- **Company-wide AI infrastructure vision**; **long-term research agenda**; **competitive moat** via **proprietary systems**
- **Industry recognition**: **Fellow**, **Keynotes**, **Patents (50+)**, **Editorial Boards**, **Standards** (MLCommons, ONNX, PyTorch)
- **Crisis leadership**: **model failures**, **GPU shortage**, **regulatory response** (EU AI Act), **reputational risk**
- **Transforms org**: **builds research lab**, **centralizes ML platform**, **changes culture at scale**

---

## ATS Parser Keyword Maps (Per-Parser)

### Greenhouse
**Exact**: `python`, `pytorch`, `tensorflow`, `mlops`, `model deployment`, `kubernetes`, `docker`, `aws`, `mlflow`, `feature store`, `model monitoring`, `distributed training`, `model optimization`, `onnx`, `tensorrt`, `ci/cd`, `github actions`, `observability`, `evidently`
**Stemming**: `deploy`→`deployed`/`deploying`, `optimiz`→`optimized`/`optimizing`, `train`→`trained`/`training`/`trainer`
**Fuzzy**: `mlops`≈`ml ops`, `feature store`≈`feast`≈`tecton`, `llm`≈`large language model`, `rag`≈`retrieval augmented generation`

### Lever
**Exact**: `python`, `pytorch`, `tensorflow`, `mlops`, `model deployment`, `kubernetes`, `docker`, `aws`, `mlflow`, `feature store`, `model monitoring`, `distributed training`, `model optimization`, `onnx`, `tensorrt`, `ci/cd`, `github actions`, `observability`, `evidently`
**Normalization**: `hugging face`→`huggingface`, `transformers`→`hf transformers`, `pytorch lightning`→`lightning`, `mlflow`→`mlflow tracking`

### Workday
**Exact (title case)**: `Python`, `PyTorch`, `TensorFlow`, `MLOps`, `Model Deployment`, `Kubernetes`, `Docker`, `Amazon Web Services`, `MLflow`, `Feature Store`, `Model Monitoring`, `Distributed Training`, `Model Optimization`, `ONNX`, `TensorRT`, `Continuous Integration`, `GitHub Actions`, `Observability`, `Evidently`

### iCIMS
**Skill clusters**:
```
ml_frameworks: ["Python", "PyTorch", "TensorFlow", "JAX", "Hugging Face", "Transformers", "Accelerate", "PEFT"]
mlops: ["MLflow", "Kubeflow", "Docker", "Kubernetes", "AWS SageMaker", "GCP Vertex AI", "Model Serving", "Monitoring", "Feature Store"]
training: ["Distributed Training", "DDP", "FSDP", "DeepSpeed", "Flash Attention", "Mixed Precision", "Gradient Accumulation"]
optimization: ["Quantization", "GPTQ", "AWQ", "Distillation", "Pruning", "ONNX", "TensorRT", "torch.compile", "vLLM", "TGI"]
data: ["Spark", "Airflow", "dbt", "Feast", "Tecton", "Snowflake", "BigQuery", "Kafka", "Flink", "Ray"]
llm: ["LLM", "RAG", "Fine-tuning", "RLHF", "DPO", "LoRA", "QLoRA", "Vector Database", "Evaluation", "Guardrails"]
```
**Weighting**: ml_frameworks (0.25) + mlops (0.2) + training (0.15) + optimization (0.15) + data (0.1) + llm (0.15)

### Taleo
**Keywords**: `Python`, `PyTorch`, `TensorFlow`, `Machine Learning`, `Deep Learning`, `Kubernetes`, `Docker`, `AWS`, `Cloud`, `MLOps`, `Model`, `Deploy`, `MLflow`, `Kubeflow`, `SageMaker`, `GPU`, `CUDA`, `Distributed`, `Training`, `Inference`, `Optimization`, `Quantization`, `ONNX`, `TensorRT`, `CI/CD`, `GitHub`, `GitLab`, `Monitoring`, `Drift`, `Agile`, `Scrum`
**Boolean**: `("PyTorch" OR "TensorFlow" OR "JAX") AND ("Kubernetes" OR "K8s" OR "EKS" OR "GKE") AND ("MLOps" OR "MLflow" OR "Kubeflow" OR "SageMaker") AND ("Docker" OR "Container") AND ("AWS" OR "GCP" OR "Azure")`

---

## Typical JD Patterns (3 Archetypes)

### Archetype 1: MLOps / Platform Focus (Scale-Ups, Enterprise ML Platforms)
**Keywords**: `mlops`, `ml platform`, `feature store`, `model registry`, `model serving`, `monitoring`, `ci/cd`, `github actions`, `kubeflow`, `kserve`, `mlflow`, `feast`, `tecton`, `evidently`, `distributed training`, `fsdp`, `deepspeed`, `reproducibility`, `governance`, `model cards`, `bias audit`, `self-serve`, `developer experience`, `sla`, `cost optimization`
**Mirror**: Lead with **platform impact** (models served, teams enabled, SLA, cost/model). Use `built`, `architected`, `standardized`, `enabled`, `governed`. Emphasize **leverage**, **self-serve**, **reliability**, **cost efficiency**.

### Archetype 2: LLM / GenAI Engineering (AI Labs, GenAI Products, Enterprise AI)
**Keywords**: `llm`, `generative ai`, `transformer`, `fine-tuning`, `lora`, `qlora`, `rag`, `vector database`, `pinecone`, `weaviate`, `milvus`, `reranking`, `vllm`, `tgi`, `sgang`, `quantization`, `gptq`, `awq`, `distillation`, `speculative decoding`, `pagedattention`, `rlhf`, `dpo`, `kto`, `alignment`, `guardrails`, `nemo`, `llamaguard`, `evaluation`, `llm-as-judge`, `ragas`, `mmlu`, `human_eval`, `agents`, `langgraph`, `autogen`, `crewai`
**Mirror**: Lead with **technical depth**, **scale**, **novel techniques**. Use `pioneered`, `optimized`, `deployed`, `benchmarked`, `open-sourced`. Emphasize **GPU efficiency**, **latency/throughput**, **quality preservation**, **safety**.

### Archetype 3: Applied ML / Production ML (Recommendation, Ads, Fraud, Forecasting)
**Keywords**: `recommendation`, `ranking`, `two-tower`, `sasrec`, `bert4rec`, `ctr`, `cvr`, `gmV`, `fraud`, `anomaly detection`, `forecasting`, `tft`, `deepar`, `prophet`, `feature engineering`, `feature store`, `real-time`, `online inference`, `latency`, `throughput`, `a/b testing`, `experimentation`, `causal inference`, `incrementality`, `mlops`, `model monitoring`, `drift detection`, `retraining`
**Mirror**: Lead with **business metrics** (CTR +X%, Revenue +Y%, Fraud prevented $Z). Use `built`, `deployed`, `optimized`, `measured`, `iterated`. Emphasize **end-to-end ownership**, **real-time constraints**, **experiment rigor**, **production scale**.

---

## Gap Analysis Triggers

| Missing Keyword | Trigger | Action |
|-----------------|---------|--------|
| `MLflow` / `W&B` / `Experiment Tracking` | JD requires MLOps; missing | Add `MLflow`/`W&B`; describe tracking, registry, lineage, reproducibility |
| `Feature Store` / `Feast` / `Tecton` | JD requires; missing | Add `Feast`/`Tecton`; describe feature definitions, PIT correctness, online/offline |
| `Model Monitoring` / `Evidently` / `Drift Detection` | JD requires; missing | Add `Evidently`/`WhyLabs`/`Arize`; describe drift alerts, performance monitoring, retraining triggers |
| `Distributed Training` / `FSDP` / `DeepSpeed` | JD requires scale; resume has single-GPU only | Add `FSDP`/`DeepSpeed`/`DDP`; describe multi-node, ZeRO, activation checkpointing, Flash Attention |
| `Model Optimization` / `Quantization` / `TensorRT` / `vLLM` | JD requires inference optimization; missing | Add `Quantization (GPTQ/AWQ/NF4)`, `TensorRT`, `vLLM/TGI`, `Distillation`, `Speculative Decoding` |
| `LLM` / `RAG` / `Fine-tuning` / `RLHF` | GenAI JD; missing | Add `LLM Fine-tuning (LoRA/FSDP)`, `RAG (Vector DB, Reranking)`, `RLHF/DPO`, `Guardrails`, `Evaluation` |
| `Kubernetes` / `KServe` / `Kubeflow` | ML Platform JD; missing | Add `Kubernetes (KServe, Kubeflow, Kueue)`, `Docker`, `Helm`; describe model serving, autoscaling |
| `Mentoring` / `Career Ladder` / `Hiring Bar` | Senior+ JD; missing | Add `Mentored N MLE`, `Defined Career Ladder`, `Raised Hiring Bar`, `Interviewed 100+` |

---

## Portfolio Cross-Reference Signals

| Artifact | Keywords | Reference Location |
|----------|----------|-------------------|
| **GitHub: ML Library / Tool / Operator** | `Open Source`, `Python`, `PyTorch`, `Kubernetes`, `Community`, `Downloads`, `Contributors` | Projects, GitHub Link |
| **Technical Blog: MLOps / LLM / Optimization** | `Technical Writing`, `MLOps`, `LLM`, `Quantization`, `Distributed Training`, `Best Practices` | Writing, Portfolio Link |
| **Conference Talk (NeurIPS, ICML, KubeCon, MLconf)** | `Public Speaking`, `Thought Leadership`, `MLOps`, `LLM`, `Optimization`, `Open Source` | Speaking, Leadership |
| **MLCommons / MLPerf Submission** | `Benchmarking`, `Performance`, `MLPerf`, `Training`, `Inference`, `Optimization` | Projects, MLCommons |
| **Internal Platform Adoption Case Study** | `Platform Engineering`, `Adoption Metrics`, `Developer Productivity`, `Cost Savings`, `Change Management` | Experience, Projects |
| **Model Card / System Card (Sanitized)** | `Model Governance`, `Bias Audit`, `Fairness`, `Documentation`, `Responsible AI`, `EU AI Act` | Experience, Projects |

---

## Role-Specific ATS Optimization Notes

### Red Flags (Auto-Reject)
- **Only "scikit-learn / Pandas"** — no PyTorch/TensorFlow → Data Scientist, not ML Engineer
- **No deployment/serving keywords** — "notebook only" → Can't productionize
- **No MLOps tools** (MLflow, Kubeflow, Feast, Evidently) → Engineering gap
- **No distributed training** for Senior+ → Scale gap
- **No GPU/cloud specifics** → Infrastructure inexperience
- **>2 pages for <5 yrs** → Format penalty
- **Tables/columns/graphics** → Parser extraction failure

### Density Targets
| Priority | Min | Max | Terms |
|----------|-----|-----|-------|
| Critical | 2.0% | 3.5% | `Python`, `PyTorch`, `TensorFlow`, `MLOps`, `Model Deployment`, `Kubernetes`, `Docker`, `AWS`, `MLflow`, `Feature Store`, `Model Monitoring`, `Distributed Training` |
| High | 1.5% | 3.0% | `vLLM`, `TGI`, `LLM`, `Transformers`, `RAG`, `Fine-tuning`, `RLHF`, `DPO`, `LoRA`, `Quantization`, `TensorRT`, `ONNX`, `FSDP`, `DeepSpeed`, `SageMaker`, `Vertex AI` |
| Medium | 1.0% | 2.5% | `MLflow`, `Kubeflow`, `Evidently`, `Spark`, `Airflow`, `dbt`, `Feast`, `Tecton`, `GitHub Actions`, `CI/CD`, `Observability`, `Mentoring`, `Code Review` |
| Low | 0.5% | 1.5% | `JAX`, `Ray`, `Polars`, `DuckDB`, `Iceberg`, `Delta Lake`, `SGLang`, `llama.cpp`, `NeMo Guardrails`, `Constitutional AI`, `SLSA`, `Sigstore` |

### NDA Abstraction
- **L2**: "Large-scale ML platform (500+ models, 10K+ GPU-hours/day) on AWS/Kubernetes"
- **L3**: "Cut inference latency 60% and GPU cost 40% via quantization and speculative decoding"
- **L4**: "Reduced inference latency 60% and GPU spend 40% through model optimization"

---

## Quick Tailoring Checklist

- [ ] Role ID confirmed: `data-science/ml-engineer`
- [ ] Seniority detected from JD → correct verb tier applied
- [ ] All 10 must-have terms in Skills + 2+ Experience bullets each
- [ ] Parser exact matches: Greenhouse/Lever/Workday/iCIMS/Taleo covered
- [ ] Density calibrated: Critical 2-3.5%, High 1.5-3%, Medium 1-2.5%, Low 0.5-1.5%
- [ ] Signal tags valid (10 controlled tags only, contextual)
- [ ] NDA level: L3 for applications, L2 for portfolio
- [ ] Audience layers: HR (keywords), HM (scope/scale/latency), Tech Lead (architecture/kernels), Exec (GPU cost/business impact)
- [ ] Metrics validated via `metric_plausibility.py` (latency, throughput, GPU utilization, cost/model, drift PSI, training time, tokens/sec)
- [ ] Portfolio cross-refs: GitHub/blog/talks/MLPerf with expected keywords
- [ ] Format: Single `main.tex`, linear, no tables/columns, UTF-8 + T1 fontenc
- [ ] Overleaf-ready: Compiles on TeX Live 2024