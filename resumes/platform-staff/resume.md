# Paul Wendt

paulwendt567@gmail.com · +1-609-635-6144 · [LinkedIn](https://www.linkedin.com/in/paul-wendt-81380a260) · [GitHub](https://github.com/WillChangeThisLater)

## Summary
Platform engineer (5.5 yrs) who has owned production systems end-to-end across four services, a company-wide data platform, and vendor deployments — from ambiguous problem through architecture, build, and operation. Deep in Python/AWS, Kubernetes, and data systems at scales up to 1M+ videos/day, in compliance-heavy environments where security and legal constraints shaped the architecture. Track record of setting direction other engineers build on and mentoring engineers into system ownership.

## Experience

### SimpliSafe — Boston, MA

**Senior ML Ops Engineer** · Oct 2024 – Mar 2026 · (promoted to Senior Jun 2025)

- Owned a production Python/AWS service stack (ingestion, permission routing, deletion/compliance) processing up to 1.2M videos/day; set the sampling architecture that cut ingest volume 75% (1.2M → 300k/day) with a policy simulator wired into CI/CD so expensive policy changes were blocked pre-merge
- Led response to a compliance-critical bug (permission inversion, hundreds of thousands of users): coordinated remediation with legal, quantified impact via data analysis, then built daily invariant checks that later caught a race condition and state drift
- Deployed and stabilized a vendor ML platform (Voxel51) on EKS; built a custom operator bridging it to our compute cluster — the vendor adopted it as a product feature
- Set direction across teams: authored CloudFormation/CI/CD patterns, drove branch-based dev-stack deploys, built CloudWatch dashboards and alarming, participated in on-call, and ran a 4-month enablement program (infra, dashboards, on-call triage) that transitioned production ownership of the video-ingestion service to 3 ML engineers

**Data Engineer / Platform Engineer** · Nov 2021 – Oct 2024 · (promoted to DE II Jun 2023)

- Major implementer on a company-wide platform migration (cron → Dagster): built connectors and extended a YAML DSL serving 30+ users across 10 teams at thousands of daily runs
- Designed "dependency sensor v2" preserving partition lineage across ~350 pipelines — a core platform primitive where the off-the-shelf solution produced wrong semantics
- Migrated GitHub Actions runners from EC2 to EKS (CDK + Helm), cutting test delays from >1 hour to ~20 minutes
- Built ~50 finance-data pipelines into Apache Iceberg; backfilled ~150M images (~37.5 TB) via a multi-stage Step Functions architecture

### John Hancock — Boston, MA

**Actuarial Associate** · May 2019 – Nov 2021

- Built annuity valuation tooling with reserving/regulatory stakeholders, including a Python AST transpiler compiling model specs to Excel
- Automated ~5 quarterly reporting workbooks (VBA); prepared capital/remittance forecasts for senior management

## Agentic engineering

- [Extended the pi agent harness](https://github.com/WillChangeThisLater/pi): added video/audio input support, TUI per-model modality indicators, push-to-talk dictation (STT), and model-aware identity in system prompts — all implemented end-to-end by agents under my direction and review
- [Built an agent-run job-search pipeline](https://github.com/WillChangeThisLater/ai-job-search): posting discovery, evidence-bank-driven resume tailoring, browser-driven applications with screenshot verification, tracked outcomes

## Education & Certifications

**Temple University** — B.A. Actuarial Science, Minor CS · *Summa Cum Laude* (2019) · CKA (2023) · ASA (2021)

## Technical Skills

- **Languages & Cloud:** Python, SQL, Bash, Go · AWS (Lambda, S3, DynamoDB, Kinesis, EventBridge, SQS, EKS, CloudFormation, CDK, SAM, MWAA), Kubernetes, Docker, Helm, GitHub Actions
- **Data & tooling:** Dagster, Airflow, Iceberg, Kafka, Ray/Anyscale, DuckDB · agent orchestration, CDP automation, AI-assisted review
