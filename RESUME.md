# RESUME Scratchpad (Source of Truth)

## Purpose
This file is a comprehensive scratchpad for all resume-relevant experience, impact, metrics, projects, skills, and context.
It is intentionally verbose. We will distill it into tailored resumes later.

## Personal
- Name: Paul Wendt
- Email: paulwendt567@gmail.com
- Phone: +1-609-635-6144
- Preferred locations: Boston / NYC / Philadelphia
- Seniority target: Staff preferred, Senior comfortable, II/III if fit is strong

## Education
- Temple University, B.A. Actuarial Science, minor in CS, Summa Cum Laude (Aug 2015 – May 2019)

## Certifications
- CKA (2023)
  - Applied directly in production work (GitHub runner migration to EKS, Voxel on EKS)
  - Especially useful for service topology decisions (internal deployment-to-deployment traffic vs externally exposed services)
  - Strong practical use of core K8s abstractions: Deployments, Services, Pods, CRDs
- AWS Cloud Practitioner (2022)
- ASA (2021), 8 exams passed

---

## Experience (raw)

### SimpliSafe (Boston, MA)
- Data Engineer / Platform Engineer (Nov 2021 – Oct 2024; promoted to DE II Jun 2023)
- ML Ops Engineer II (Oct 2024 – Mar 2026; promoted to Senior Jun 2025)

#### ML Ops evidence bank (high relevance)

**Core ingestion + compliance services**
- Built/maintained ML ingestion stack
- Ownership split:
  - Primary owner: Friday, Thanos
  - Technical owner with heavier collaboration: Cerebro, Heimdall
- Service details:
  - Cerebro (FastAPI): receives opt-in video notifications from Leia, validates payloads, emits downstream events
  - Friday: EventBridge -> SQS/Lambda/DynamoDB hold (72 hours legal waiting period) -> Flipbook fetch -> S3/Kinesis Firehose
    - implementation detail: rows were bucketed by 15-minute block timestamps at write time
    - sweeper Lambda ran every 15 minutes, computed the eligible block, and pulled/released records for downstream ingest
    - known downside: missed sweeps could drop data if the Lambda did not run for a block (e.g., AWS outage, account-level Lambda concurrency pressure)
    - this was an acknowledged risk (not fully mitigated at the time); impact was usually minor relative to total volume but could skew aggregate statistics
    - Friday CloudFormation stack was one of the more complex stacks in practice (many interdependent resources + tricky deployment dependencies)
  - Thanos: RTBF deletion service with production checks/tests
  - Heimdall: Kafka-driven AI toggle service, maps user-level toggles to camera-level downstream actions
- Load behavior:
  - Bursty daytime traffic handled by SQS buffering
  - Lambda concurrency capped at 50 (intentionally, to protect upstream systems)
  - Queue catch-up after daytime spikes was typically ~3–4 hours
  - Failure rate was generally low; anomaly alerts were in place
- Operational monitoring + ownership:
  - CloudFormation-managed CloudWatch dashboards/alarms
  - threshold alerts for failure modes (e.g., queue backlog >1 day, Lambda error rate >5%)
  - alerts routed to Slack channels (service alarms + daily datalake checks)
  - primary Friday maintainer; reviewed dashboards and alert channels daily
- Datalake outputs created for Friday/Cerebro/Thanos/Heimdall to support training and auditing

**Emergency training data bootstrap**
- At team start, no production training data available for ML engineers
- Built Step Functions + Lambda workflow to enumerate/copy very large ODMON EFS dataset into S3
- Backfilled ~150 million JPEG images over a multi-day run (~37.5 TB estimated, assuming ~250 KB/image)
- Solved timeout constraints via multi-stage path enumeration + copy strategy
- Unblocked early model training

**Heimdall incident + governance controls**
- Major toggle inversion bug (on/off logic reversed)
- Impacted hundreds of thousands of users and created significant legal/compliance risk
  - key constraint: in many states, video retention beyond 30 days is not legally permitted
- Partnered with manager to triage/remediate over multi-day incident response
- Coordinated heavily with legal to communicate impact and demonstrate remediation
- Used datalake analysis to quantify impact and validate fixes
- Productized governance checks via Dagster SQL invariants and reconciliation jobs
  - ran daily
  - metadata-level checks: e.g., if upstream Kafka state indicates user data should be deleted, verify Thanos metadata reflects deletion events
  - storage-level checks: S3 inventory reconciliation against nightly inventory snapshots
  - additional checks: detect Friday ingest for users Heimdall marks off; detect Heimdall state drift against upstream Kafka truth
  - primary first reviewer of failures (with some isolated checks owned by other teams)
- Later checks caught additional issues (Leia race condition, bad backfill from ODMON)

**Sampling redesign (major impact)**
- Baseline ingest volume before sampling: ~1.2M videos/day
- Post-sampling ingest volume: ~300k videos/day
- Designed/implemented version-controlled sampling framework in Friday
  - uniform sampling
  - deterministic sampling (camera/user based)
  - adhoc targeted inclusions when metadata lacked key relevance signals
- Safe rollout workflow for policy/config changes:
  - PR review was required
  - staged rollout in QA with health checks before production deployment
  - update cadence: weekly by default, plus ad hoc changes for business events (e.g., new camera release, beta program launch)
- Built a sampling policy simulator:
  - loaded production-like metadata from Cerebro datalake table (CSV export)
  - executed candidate sampling policy against large record sets to estimate match volume
  - answered questions like "will this new policy match too many records?"
- Wired simulator into CI/CD guardrails:
  - test asserted current policy could execute within 10 minutes on 100k records
  - 100k was set to ~1.5x the maximum record volume observed in a 15-minute window
  - prevented overly heavy policies that would exceed Lambda runtime budget
- Hex monitoring dashboard
- Immediate ~75% reduction in ingest volume with large downstream cost impact
- Average video size was ~4 MB (can be used to estimate storage/cost savings)
- Consumer impact:
  - primary direct consumer: ML data team (annotation availability depended on strategy)
  - indirect consumers: ML engineers (training set composition) and analytics (slight metric shifts)
- Built supporting Iceberg upsert-based data management patterns

**Voxel51 platform deployment + integration**
- Deployed Voxel51 on EKS (on-prem style deployment)
- Initial infra deployment was relatively fast with support from Voxel team + internal teammates
- Hard problem was production stability after adoption:
  - API was unstable in real use
  - long-running jobs often failed after 1+ hour, wasting ML engineer time and making the tool hard to trust
- Worked directly with Voxel team on remediation attempts:
  - increased API/dependency replica counts
  - moved workloads to larger nodes
  - added proxy/retry style request handling
  - issue persisted and root cause remained unclear on vendor side
- Landed workaround that restored usability:
  - configured Voxel SDK to connect directly to MongoDB instead of routing through unstable API path
  - made this the practical default via team communication + Confluence documentation
  - before fix: tool was effectively unusable for real workloads (most long-running pipelines failed)
  - after fix: long-running, real-data pipelines became viable again
- Additional infra work:
  - heavy Helm/deployment tuning + AWS networking
  - MongoDB Atlas integration with read/write access from EKS workloads
  - handled IPv4/IPv6 mismatch and other API/backend quirks
- Built CI/CD extension deployment mechanism to keep extension set explicit and reproducible
- Implemented custom delegated operator to trigger Anyscale jobs directly from Voxel
  - practical effect: ML engineers could select very large image cohorts (up to hundreds of thousands) in Voxel and run scalable downstream analysis pipelines on them
  - example workflow: evaluate a new detection model by routing selected dataset slices to an Anyscale pipeline and returning analysis outputs for review
- Voxel team adopted most of the implementation code and productionized it as a formal product feature

**Anyscale/Ray annotation pipelines**
- Built/assisted nightly ingestion + sync jobs between S3 and annotation platform
  - baseline nightly volume: ~3,000 videos
- S3 videos -> local convert `.mp4 -> .wmv` -> annotation upload
  - `.wmv` was a hard requirement from annotation vendor (vendor did not accept `.mp4`)
  - key constraint: conversion sometimes exceeds Lambda 15-min timeout
  - moved workload to Anyscale/Ray jobs
- Typical stabilized runtime: ~1–2 hours using ~10 small CPU nodes (varied by video volume and cluster size)
- Metadata sync back to S3 as JSON
- Built "raw latest" + historical Iceberg snapshots for annotation state
- Built Hex dashboard for day-level ingest status

**MWAA orchestration**
- Stood up AWS MWAA for orchestrating Anyscale-related DAGs
- Built custom GitHub Action to sync DAGs from repos into MWAA
- Lightweight and stable operationally

**SQL + analytics for ML evaluation**
- Strong SQL/querying experience supporting ML teams
- Partnered with ML engineer to build a robust model-comparison dashboard in Hex
- Implemented complex SQL logic to compare model precision/recall/F1 at tunable thresholds across caption models
- Bucketed captions into semantic categories (e.g., animal/car/person) so users could drill into model strengths/weaknesses by caption type
- Dashboard was heavily used for model evaluation decisions

**YOLOR inference modernization PoC**
- Goal: validate Anyscale service replacement for legacy TensorFlow YOLOR inference
- Responsibilities: load testing via Locust on Kubernetes; deployment tuning support (cluster topology + autoscaling)
- Target latency: ~110ms P95
- Scale target: comfortably handle ~1,000 concurrent requests at low cost
- Observed PoC behavior: ~1,000 concurrent requests on approximately 4 GPU nodes (best recollection)
- Outcome: PoC hit target cost/load goals and informed productionization path
- Important caveat: this was a successful PoC, not fully production-shipped by this team during tenure

**Mentorship / handoff**
- Ran a ~4-month transition for 3 ML engineers taking over Friday service (AWS + CloudFormation + practical pairing)
- End-state ownership transferred to annotation team across:
  - CI/CD pipelines
  - CloudFormation resources
  - CloudWatch + Grafana dashboards
  - datalake tables
  - sampling strategy feature set
- Most important enablement areas:
  - common alarm/error-case triage so on-call engineers could self-remediate recurring failures
  - CloudFormation fluency so engineers could confidently ship fixes/features without platform hand-holding
- Delivered dev-stack capability for parallel development:
  - genericized resource naming
  - branch-based stack deploys
  - automated stale stack teardown

#### Data Engineer evidence bank (high relevance)

**Dagster migration + platform evolution**
- Team moved from cron jobs on beefy EC2 to Dagster orchestration
- Lead staff engineer (Nathan) drove platform direction; Paul was a major implementer
- Migrated many legacy pipelines into source/transform/sink model
- Contributed to YAML-based DSL ecosystem used heavily by analysts + data engineers
- Platform scaled to thousands of daily runs and broad internal adoption (~30 users across 10 teams)

**CI/CD infrastructure modernization**
- Migrated GitHub Actions runners from single EC2 to EKS-backed runner deployment
- Used CDK + Helm; designed permissions for least privilege
- Hardest parts: permissioning + test-loop ergonomics
  - frequent permission failures surfaced deep into integration runs (~15 min in)
  - each fix required CloudFormation change -> redeploy -> rerun, slowing iteration
- Debugging hack that improved iteration: built a GitHub test path that opened a reverse shell back to workstation, allowing direct runner inspection (e.g., validate S3 permissions interactively)
- Before migration: unit + integration test delays often exceeded 1 hour
- After migration/parallelization: max observed integration delay ~20 minutes; unit tests ran almost immediately

**Dagster automation/testing**
- Built GraphQL client for interacting with Dagster APIs
- Most useful outcome: production-like automated sensor testing across ~6 core sensor types
  - examples: dependency sensor, asset freshness checks, validation sensors
  - testing sensors via CLI was difficult due to multi-step prerequisites and orchestration timing
  - strategy: stand up test pipelines/sensors, trigger pipeline A via GraphQL, wait for run completion/materialization, then assert dependent sensor B fired correctly afterward
- Enabled repeatable integration tests for cross-pipeline behavior (especially dependency sensor correctness)

**Dependency scheduling**
- Designed/implemented dependency sensor v2 where default Dagster behavior fell short on partition semantics
- Root issue in default behavior:
  - sensor detected that upstream asset A materialized and triggered dependent pipeline B
  - but it ran B for the latest partition (e.g., "yesterday") instead of A's materialized partition
- Why this mattered:
  - downstream pipelines often contained partitioned SQL transforming A's outputs
  - using mismatched partitions produced incorrect/irrelevant transformations
- v2 behavior preserved partition lineage (trigger B with the same partition key that A materialized)
- Adoption: used broadly across hundreds of pipelines (~50 critical, ~300 noncritical)
- Became core internal primitive despite rough implementation ergonomics

**Zuora + finance pipelines**
- Built ~50 pipelines syncing Zuora data into datalake across ~25 objects
  - ~5–10 objects were business-critical; others were lower-frequency but useful for debugging/ad-hoc analysis
- Core challenge: Zuora API inconsistency + ambiguous analyst requirements
  - Zuora objects had many properties and two relevant APIs (ZOQL and AQuA) returned different slices of needed data
  - analysts ultimately required data from both APIs, which led to dual-pipeline patterns per object in many cases
- Worked directly with analysts who could not code to translate data needs into pipelines
- Downstream use: subscription and finance reporting

**Iceberg adoption**
- Contributed to migration toward Apache Iceberg table format and related infra

---

### John Hancock (Boston, MA)
- Actuarial Associate (May 2019 – Nov 2021)
- Actuarial Intern (May 2018 – Aug 2018)

#### Actuarial evidence bank
- Implemented annuity valuation model with reserving + regulators
- Built Python AST transpiler to convert model specifications into Excel representations
- Strongest engineering signal beyond AST: VBA automation across core quarterly reporting spreadsheets
  - automated ~5 core quarterly workbooks
  - reduced recurring effort by ~10 hours per quarter (avoided ~2 hours manual update/check work per workbook)
- Prepared quarterly capital/remittance forecasts and presented to senior management
- Intern period: insurance sensitivity analyses, product calc/code review, early Excel->Python migration support (NumPy loader; project details partially fuzzy)

---

## A.T. / Sabbatical narrative (optional resume inclusion)
- Left SimpliSafe intentionally for planned Appalachian Trail thru-hike
- Dates: Apr 6, 2026 -> Aug 19, 2026 (~4.5 months)
- Completed full thru-hike; summited Katahdin
- Built/modified PinePhone trail setup to SSH via iPhone hotspot to home machine (technical side project)
- Usually best represented as:
  - short "Planned Sabbatical" line in experience, and/or
  - project bullet for PinePhone setup

---

## Projects (personal)
- go-llm (Go CLI)
- vault (embedding store)
- filter (RAG filtering)
- bash-agent experiment
- Trail PinePhone build + AT thru-hike

---

## Skills inventory (raw)
- Python, SQL, Bash, Go
- AWS (Lambda, S3, DynamoDB, Kinesis, EventBridge, SQS, EC2, EKS, ECS, CDK, SAM, MWAA, Athena, CloudFormation)
- Kubernetes, Docker, Helm
- Dagster, Iceberg, Kafka, Ray/Anyscale, Step Functions, Pandas, DuckDB
- GitHub Actions, CI/CD, jq/yq, tmux, ssh

---

## Open questions to resolve
- Fill concrete metrics for each project:
  - peak queue depth? retry/error rates? ingestion SLAs?
  - CI runtime/queue deltas with hard numbers?
- Clarify scope/ownership (led vs contributed) per major initiative
- Add strongest infra-centric Kubernetes troubleshooting story
  - current candidate (non-infra but useful): Dagster sensors passing tests but failing in production; debugged by exec-ing into sensor container, inspecting logs, and manually triggering sensors in-container to reproduce prod behavior
- Add strongest stories for:
  - Kubernetes operations and troubleshooting
  - reliability and incident response
  - performance and cost optimization
  - cross-team collaboration and influence
