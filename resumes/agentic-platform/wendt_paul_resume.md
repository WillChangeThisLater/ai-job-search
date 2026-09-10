# Paul Wendt

Email: paulwendt567@gmail.com | Phone: +1-609-635-6144
LinkedIn: [linkedin.com/in/paul-wendt-81380a260](https://www.linkedin.com/in/paul-wendt-81380a260) | GitHub: [github.com/WillChangeThisLater](https://github.com/WillChangeThisLater)

## Summary

Senior engineer with 5 years of experience who treats AI coding agents as the default way to build. Built and ran large-scale Python/AWS data infrastructure in compliance-heavy environments, and now run my day-to-day work on an open-source agent harness I've forked and extended. Deep in data engineering and cloud infrastructure. US citizen; no sponsorship required.

## Experience

### SimpliSafe — Boston, MA

**Senior ML Ops Engineer**
*Oct 2024 – Mar 2026*

Owned the data infrastructure feeding computer vision model training.

- Built and operated production Python/AWS services ingesting up to 1.2M videos/day, the data foundation for all computer-vision training
- Designed a version-controlled video sampling framework that cut ingestion volume ~75% (1.2M to ~300K videos/day) and wired policy simulator into CI/CD to block deployments exceeding lambda execution timeouts
- Built a compliant ML data governance layer (30-day retention/RTBF) using daily Dagster SQL-invariants and S3 inventory reconciliations.
- Deployed Voxel51 on AWS EKS and engineered a custom delegated operator bridging the platform to Anyscale/Ray distributed compute; code was upstreamed and adopted by the vendor as a core product feature.

**Data Engineer II**
*Nov 2021 – Oct 2024*

Major implementer on the team that migrated the data platform from cron jobs on EC2 to Dagster orchestration.

- Migrated legacy EC2 cron pipelines to an orchestrated source/transform/sink model on Dagster, scaling the platform to thousands of daily runs
- Co-authored a YAML-based DSL on top of the new architecture to democratize pipeline creation for 30+ analysts across 10 teams
- Designed a custom Dagster dependency sensor to preserve partition lineage across 350+ downstream pipelines
- Migrated GitHub Actions runners from a standalone EC2 box to EKS (CDK + Helm), cutting integration test runtimes from over an hour to under 20 minutes

### John Hancock — Boston, MA

**Actuarial Associate** · May 2019 – Nov 2021

- Built annuity valuation tooling with reserving/regulatory stakeholders, including a Python AST transpiler compiling model specs to Excel
- Automated ~5 core quarterly reporting workbooks with VBA, cutting ~10 hours per quarter from the reporting cycle


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

- **Trail PinePhone Build**: Configured a mobile Linux environment utilizing Tailscale VPN and SSH-over-hotspot to establish secure, remote shell sessions into a distributed Anyscale cluster during a 4.5 month thru-hike
- **AI Job Search Pipeline**: Multi-agent pipeline that sweeps job boards daily, vets postings against a structured evidence bank, and suggests the best listings
- **Pi Harness Extension**: Extended open-source Pi harness to support multi-modal audio/video input streaming, push-to-talk dictation (STT), and custom TUI model-state indicators

---

## Technical Skills

| Category | Technologies |
|----------|-------------|
| Languages | Python, SQL, Bash, Go |
| Data | Apache Iceberg, Dagster, Kafka, Airflow/MWAA, Athena, Pandas, DuckDB, Hex |
| Cloud & Infra | AWS (EKS, CDK, Lambda, Step Functions, DynamoDB, S3, SQS, Kinesis Firehose, EventBridge), Kubernetes, Helm, Ray/Anyscale |
| DevOps | GitHub Actions (custom actions, EKS runners), CI/CD architecture, ML data pipelines |
| Tools | Git, Neovim, Tmux, SSH, jq/yq, GraphQL |
