# Paul Wendt

Remote (US) · paulwendt567@gmail.com · +1-609-635-6144 · https://www.linkedin.com/in/paul-wendt-81380a260

## Summary

Senior engineer (5.5 yrs) who treats AI coding agents as the default way to build. Built and ran large-scale Python/AWS data infrastructure (1M+ videos/day ingestion, thousands of daily orchestration runs) in compliance-heavy environments, and now run my day-to-day work on an open-source agent harness I've forked and extended. Deep in data engineering (SQL, orchestration, table formats) and cloud infrastructure (K8s, IaC, CI/CD). US citizen; no sponsorship required.

## Experience

### SimpliSafe — Boston, MA

**Senior ML Ops Engineer** · Oct 2024 – Mar 2026 · (promoted to Senior Jun 2025)

- Built and operated production Python/AWS services ingesting up to 1.2M videos/day (EventBridge→SQS/Lambda→S3/Iceberg), the data foundation for all computer-vision training
- Designed version-controlled sampling policies (uniform/deterministic/adhoc) cut ingest volume 75% (1.2M → 300k/day) with large cost savings; wired a policy simulator into CI/CD to block overly expensive policy changes
- Built the governance layer for an ML data platform in a legally constrained domain (30-day retention, RTBF): daily Dagster SQL-invariant and S3-inventory reconciliation checks that caught a race condition, an erroneous backfill, and state drift — codified after leading multi-day incident response with legal on a toggle-inversion bug affecting hundreds of thousands of users
- Deployed and stabilized Voxel51 on EKS (vendor API instability → direct MongoDB SDK workaround); built a custom delegated operator bridging Voxel to Anyscale that the vendor adopted as a product feature

**Data Engineer / Platform Engineer** · Nov 2021 – Oct 2024 · (promoted to DE II Jun 2023)

- Major implementer on a Dagster migration (cron → orchestrated platform, thousands of daily jobs, ~30 users across 10 teams); designed "dependency sensor v2" preserving partition lineage across ~350 pipelines — a core platform primitive
- Migrated GitHub Actions runners from EC2 to EKS (CDK + Helm), cutting test delays from >1 hour to ~20 minutes; backfilled ~150M images (~37.5 TB) to bootstrap ML training data
- Built ~50 Zuora pipelines for finance reporting; wrote automated Dagster integration tests via a GraphQL client

### John Hancock — Boston, MA

**Actuarial Associate** · May 2019 – Nov 2021

- Built annuity valuation tooling with reserving/regulatory stakeholders, including a Python AST transpiler compiling model specs to Excel
- Automated ~5 quarterly reporting workbooks (VBA); prepared capital/remittance forecasts for senior management

## Agentic engineering (how I work now)

- [Extended the pi agent harness](https://github.com/WillChangeThisLater/pi): video/audio input support, TUI per-model modality indicators, push-to-talk dictation (STT), model-aware identity in system prompts — all implemented end-to-end by agents
- [Built an agent-run job-search pipeline](https://github.com/WillChangeThisLater/ai-job-search): posting discovery, evidence-bank-driven resume tailoring, browser form filling with screenshot verification, application tracking — with agent output held to a production bar (tests, SQL invariants, reconciliation checks), the same verification discipline I applied to ML data governance at SimpliSafe
- Daily driver: personal agent skill library (CDP browser automation, per-site controls files, tmux orchestration, X11 GUI automation)


## Education & Certifications

**Temple University** — B.A. Actuarial Science, Minor CS · *Summa Cum Laude* (2019) · CKA (2023) · ASA (2021)

**Skills:** Python · SQL · Bash · Go · AWS (Lambda, S3, DynamoDB, Kinesis, EventBridge, SQS, EKS, CloudFormation, CDK, MWAA) · Kubernetes · Docker · Helm · GitHub Actions · Dagster · Airflow · Iceberg · Kafka · Ray/Anyscale · DuckDB · Pandas · agent orchestration, CDP browser automation, AI-assisted verification
