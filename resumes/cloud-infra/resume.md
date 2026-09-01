# Paul Wendt

paulwendt567@gmail.com · +1-609-635-6144 · [LinkedIn](https://www.linkedin.com/in/paul-wendt-81380a260) · [GitHub](https://github.com/WillChangeThisLater)

## Summary
Cloud infrastructure engineer (5.5 yrs) who has owned production AWS systems end-to-end — architecture, security, cost, on-call — in environments where mistakes meant legal exposure, not just downtime. Ran infrastructure behind systems processing 1M+ videos/day and pipelines running thousands of daily jobs. Pragmatic: happiest as the accountable owner who makes the "how should we build this?" call and does the implementation.

## Experience

### SimpliSafe — Boston, MA

**Senior ML Ops Engineer** · Oct 2024 – Mar 2026 · (promoted to Senior Jun 2025)

- Owned production AWS services (Lambda, SQS, DynamoDB, EventBridge, S3) ingesting up to 1.2M videos/day; set the sampling architecture that cut ingest volume 75% — a major cost reduction — with a policy simulator wired into CI/CD blocking expensive changes pre-merge
- Led response to a compliance-critical incident (permission inversion affecting hundreds of thousands of users in a legally constrained data-retention regime): coordinated remediation with legal, quantified impact via data analysis, then built daily SQL-invariant and storage-reconciliation checks that caught a race condition, an erroneous backfill, and state drift
- Deployed and stabilized a vendor ML platform (Voxel51) on EKS: diagnosed vendor API instability, shipped the MongoDB-direct workaround that restored production viability, and handled IPv6/IPv4, networking, and MongoDB Atlas access from EKS workloads
- Ran a 4-month enablement program teaching 3 engineers CloudFormation, CI/CD, and on-call triage until they owned the video-ingestion service independently

**Data Engineer / Platform Engineer** · Nov 2021 – Oct 2024 · (promoted to DE II Jun 2023)

- Migrated GitHub Actions runner fleet from a dedicated EC2 instance to EKS (CDK + Helm), designing least-privilege IAM permissions; cut test queue delays from >1 hour to ~20 minutes
- Major implementer on a company-wide platform migration (cron → Dagster): built connectors, extended a YAML DSL serving 30+ users across 10 teams at thousands of daily runs
- Built ~50 finance-data pipelines into Apache Iceberg; backfilled ~150M images (~37.5 TB) via a multi-stage Step Functions architecture
- Designed "dependency sensor v2" preserving partition lineage across ~350 pipelines — a core platform primitive where the off-the-shelf solution produced wrong semantics

### John Hancock — Boston, MA

**Actuarial Associate** · May 2019 – Nov 2021

- Built annuity valuation tooling with reserving/regulatory stakeholders, including a Python AST transpiler compiling model specs to Excel
- Automated ~5 quarterly reporting workbooks (VBA); prepared capital/remittance forecasts for senior management

## Agentic engineering

- [Extended the pi agent harness](https://github.com/WillChangeThisLater/pi): video/audio input support, TUI modality indicators, push-to-talk dictation (STT), model-aware system prompts — all implemented end-to-end by agents under my direction and review
- [Built an agent-run job-search pipeline](https://github.com/WillChangeThisLater/ai-job-search): posting discovery, resume tailoring, browser-driven applications with screenshot verification

## Education & Certifications

**Temple University** — B.A. Actuarial Science, Minor CS · *Summa Cum Laude* (2019) · CKA (2023) · AWS Cloud Practitioner (2022)

## Technical Skills

- **Cloud/Infra:** AWS (Lambda, S3, DynamoDB, Kinesis, EventBridge, SQS, EC2, EKS, CloudFormation, CDK, SAM, MWAA, Athena), Kubernetes, Docker, Helm, GitHub Actions, IAM/least-privilege design
- **Languages & Data:** Python, SQL, Bash, Go · Dagster, Airflow, Iceberg, Kafka, Step Functions, DuckDB
