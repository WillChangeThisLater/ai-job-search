# Paul Wendt

Email: paulwendt567@gmail.com | Phone: +1-609-635-6144

---

## Experience

### SimpliSafe — Boston, MA

**Senior ML Ops Engineer**
*Oct 2024 – Mar 2026*

Owned the data infrastructure feeding computer vision model training.

- Built and operated four production data services (video ingestion, AI-permission routing, Right-to-be-Forgotten deletion) on EventBridge → SQS → Lambda → S3/Kinesis Firehose
- Designed a version-controlled video sampling framework which cut video ingestion volume ~75% — 1.2M to ~300K videos/day, resulting in significant cost savings
- Productized data governance as daily Dagster jobs: SQL invariants and S3 inventory reconciliations verified deletion events, detected ingest drift against upstream Kafka state, and caught multiple cross-service bugs
- Built Ray/Anyscale pipelines moving nightly video batches and metadata JSON between S3 and an annotation platform, orchestrated via MWAA Airflow

**Data Engineer II**
*Nov 2021 – Oct 2024*

Major implementer on the team that migrated the data platform from cron jobs on EC2 to Dagster orchestration.

- Migrated legacy cron pipelines to a source/transform/sink model on Dagster, contributing to a YAML-based DSL used by ~30 analysts and data engineers across 10 teams; platform scaled to hundreds of pipelines with thousands of daily runs
- Designed a dependency sensor preserving partition lineage where Dagster's default triggered downstream pipelines with the wrong partition keys, which became a core platform primitive across ~350 pipelines
- Migrated GitHub Actions runners from a single EC2 box to EKS (CDK + Helm, least-privilege IAM); parallelized test suites, cutting integration test runtimes from over an hour to under 20 minutes
- Authored ~50 pipelines syncing ~25 Zuora objects into Apache Iceberg tables to power subscription and finance reporting; navigated dual ZOQL/AQuA API inconsistencies and translated non-technical analysts' requirements into production pipelines

### John Hancock Life Insurance — Boston, MA

**Actuarial Associate**
*May 2019 – Nov 2021*

- Implemented annuity valuation model with reserving team and state regulators; wrote a Python AST transpiler converting model specifications to Excel, eliminating weeks of manual translation effort
- Automated ~5 core quarterly reporting workbooks with VBA, cutting ~10 hours per quarter from the reporting cycle

---

## Education

**Temple University** — Philadelphia, PA
*Aug 2015 – May 2019*
B.A. in Actuarial Science, Minor in Computer Science · *Summa Cum Laude*

---

## Certifications

- **Certified Kubernetes Administrator (CKA)** — 2023
- **AWS Certified Cloud Practitioner** — 2022
- **Associate of the Society of Actuaries (ASA)** — 2021

---

## Projects

- **Trail PinePhone Build**: Modified PinePhone for SSH-over-iPhone-hotspot remote development during an Appalachian Trail thru-hike
- **AI Job Search Pipeline** *(Python + pi agent harness)*: Multi-agent pipeline that sweeps job boards daily, vets postings against a structured evidence bank, and suggests the best listings based on my experience and preferences.
- **vault** *(Python)*: Local embedding store for RAG — add text/images/URLs/directories, search via embeddings


---

## Technical Skills

| Category | Technologies |
|----------|-------------|
| Languages | Python, SQL, Bash, Go |
| Data | Apache Iceberg, Dagster, Kafka, Airflow/MWAA, Athena, Pandas, DuckDB, Hex |
| Cloud & Infra | AWS (S3, Lambda, SQS, Kinesis Firehose, EventBridge, DynamoDB, Step Functions, ECS, EKS, CDK, CloudFormation), Kubernetes, Docker, Helm, Ray/Anyscale |
| DevOps | GitHub Actions (custom actions, EKS runners), CI/CD architecture, ML data pipelines |
| Tools | Git, Neovim, Tmux, SSH, jq/yq, GraphQL |
