# Paul Wendt

<style>
li { margin-bottom: 0; }
p { margin: 2px 0; }
h2 { margin-top: 0.55em; }
</style>


Email: paulwendt567@gmail.com | Phone: +1-609-635-6144

---

## Experience

### SimpliSafe — Boston, MA

**ML Ops Engineer** *(Promoted to Senior, Jun 2025)* · Oct 2024 – Mar 2026

Built ML data infrastructure serving video training data to computer vision models while maintaining AI opt-in compliance at scale.

- Built four production services for video ingestion, AI permission routing, and Right-to-be-Forgotten compliance; handled peak loads via AWS SQS buffering and Lambda concurrency limits (capped at 50 to protect upstream), maintaining steady throughput regardless of daily traffic spikes
- Designed and implemented sophisticated, version-controlled sampling mechanisms that reduced video ingestion volume by 75% without compromising training data quality or downstream statistical validity
- Deployed Voxel51 on-premise onto EKS: customized deployment Helm chart, stood up MongoDB Atlas cluster and configured AWS networking to grant EKS read/write access to the database
- Built Ray/Anyscale pipelines ingesting nightly batches of videos from S3 to our annotation platform, orchestrated end-to-end via MWAA Airflow; moved .mp4-to-.wmv conversions off Lambda functions (which time out at 15 minutes) into distributed workers that reliably process large video files

---

**Data Engineer / Platform Engineer** *(Promoted to II, Jun 2023)* · Nov 2021 – Oct 2024

Contributed to migration of company data platform from cron-based EC2 runners to Dagster orchestration.

- Helped migrate legacy cron-based pipelines to Dagster; contributed to a YAML-based DSL for pipeline authoring that served 30+ analysts across 10 teams, scaling to 1100+ daily pipelines
- Authored ~50 Zuora subscription/revenue pipelines pulling data into Apache Iceberg tables, powering hundreds of downstream financial reports on subscriber metrics
- Migrated GitHub Actions runner fleet from dedicated EC2 instances to EKS via CDK-managed Helm charts; rewrote test workflows to run in parallel, cutting queue times from hours to minutes
- Contributed to custom dependency scheduler that resolved edge cases where Dagster's default sensors failed under real-world workloads; deployed as core platform component

---

### John Hancock Life Insurance — Boston, MA

**Actuarial Associate**  
May 2019 – Nov 2021

- Implemented annuity valuation model with reserving team and state regulators; wrote Python AST transpiler converting specifications to Excel format — eliminated weeks of manual translation effort
- Automated quarterly valuation reports using VBA scripts, reducing 10 hours from recurring reporting cycle each quarter
- Prepared quarterly capital and remittance forecasts and presented results to senior management

---

## Education

**Temple University** — Philadelphia, PA  
B.A. in Actuarial Science, Minor in Computer Science · *Summa Cum Laude*  
Aug 2015 – May 2019

---

## Certifications

- **Certified Kubernetes Administrator (CKA)** — 2023
- **AWS Certified Cloud Practitioner** — 2022
- **Associate of the Society of Actuaries (ASA)** — 2021

---

## Projects

**go-llm** *(Go)*: CLI wrapper for LLM APIs — image input, site scraping, structured output, prompt caching, local models

**bash-agent.sh** *(Bash)*: Autonomous agent loop using LLM function calling — creates functions, executes code, observes results, iterates. No human in the loop

**vault** *(Python)*: Local embedding store for RAG — add text/images/URLs/directories, search via embeddings

**filter** *(Python)*: Relevance filtering for RAG — pipes embedding search results through an LLM to gate irrelevant context before it hits the model

**Trail PinePhone Build**: PinePhone modified for SSH-over-iPhone-hotspot remote development during an Appalachian Trail thru-hike

---

## Technical Skills

| Category | Technologies |
|----------|-------------|
| Languages | Python, SQL, Bash, Go |
| Cloud & Infra | AWS (Lambda, S3, DynamoDB, Kinesis, EventBridge, SQS, EC2, EKS, ECS, CDK, SAM, MWAA, Athena, CloudFormation, IAM), Kubernetes, Docker, Helm |
| Data & ML | Dagster, Apache Iceberg, Ray/Anyscale, Kafka, Step Functions, Hex Dashboards |
| DevOps & Tools | GitHub Actions (custom actions, EKS runners), CI/CD architecture · Git, Neovim, Tmux, yq/jq, GraphQL |
