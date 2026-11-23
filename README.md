<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/main/assets/hero-dark.svg">
  <img alt="Joun Mikhail — Cloud Support Engineer and IT Support Engineer. AWS serverless, monitoring and incident response, automation. Brno, Czech Republic, open to EU relocation." src="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/main/assets/hero-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://linkedin.com/in/john-mikhaill1"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="mailto:mikhailjoun@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-mikhailjoun%40gmail.com-00b4d8?style=for-the-badge&logo=gmail&logoColor=white"></a>
  <a href="https://frontend-jade-two-zfchqjb5ws.vercel.app"><img alt="Live demo" src="https://img.shields.io/badge/Live_demo-CareerFlow-8b5cf6?style=for-the-badge&logo=vercel&logoColor=white"></a>
</p>

I'm a **Cloud & IT Support Engineer** who builds and runs services on **AWS**. My projects are built the way production teams work: automated tests, CI/CD pipelines, infrastructure as code, least-privilege access, alarms that page someone, and written runbooks for when things break.

Based in **Brno, Czech Republic** · open to relocation across **Europe** · working languages **English** and **Arabic**.

> **Looking for:** IT Support Engineer · Cloud Support Engineer

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/main/assets/metrics-dark.svg">
  <img alt="At a glance: 400+ automated tests across 4 projects. 97% test coverage on the CareerFlow backend. 8 CI/CD workflows. 0 long-lived AWS keys, deploys use GitHub OIDC." src="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/main/assets/metrics-light.svg" width="100%">
</picture>

## What I bring

| Area | What I can do for your team | Where to see it |
| :-- | :-- | :-- |
| **Cloud (AWS)** | Build and support serverless services with Lambda, API Gateway, DynamoDB, IoT Core, SNS and Secrets Manager, defined as infrastructure as code (SAM) | [Device Registry API](https://github.com/Joun-Mikhail/device-registry-serverless-api) · [IoT Monitoring](https://github.com/Joun-Mikhail/iot-monitoring-system) |
| **Monitoring & incident response** | CloudWatch metrics, alarms and dashboards, SNS alerting, health probes, uptime checks with down and recovery alerts, step-by-step debugging playbooks | [IoT failure playbook](https://github.com/Joun-Mikhail/iot-monitoring-system#failure-modes-and-debugging-playbook) · [Service Watchdog](https://github.com/Joun-Mikhail/service-watchdog) |
| **Automation & CI/CD** | GitHub Actions pipelines with tests, linting, coverage gates and secret scanning; keyless OIDC deploys to AWS; post-deploy production smoke tests | [CareerFlow workflows](https://github.com/Joun-Mikhail/careerflow/tree/main/.github/workflows) · [this profile](#live-repository-status) |
| **Security fundamentals** | Least-privilege IAM per function, API-key authorizer backed by Secrets Manager, JWT with refresh-token rotation, bcrypt, dependency and secret audits | [Device Registry security](https://github.com/Joun-Mikhail/device-registry-serverless-api#security) |
| **Backend & APIs** | REST APIs in Python (FastAPI), PostgreSQL schema design and migrations, contract tests against an OpenAPI spec | [CareerFlow](https://github.com/Joun-Mikhail/careerflow) |
| **Linux & containers** | Docker, Docker Compose, Nginx reverse proxy, shell scripting, troubleshooting from logs | [CareerFlow](https://github.com/Joun-Mikhail/careerflow) |

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=aws,py,fastapi,postgres,docker,githubactions,linux,nginx,bash,git,react,ts&theme=dark">
    <img alt="AWS, Python, FastAPI, PostgreSQL, Docker, GitHub Actions, Linux, Nginx, Bash, Git, React, TypeScript" src="https://skillicons.dev/icons?i=aws,py,fastapi,postgres,docker,githubactions,linux,nginx,bash,git,react,ts&theme=light">
  </picture>
</p>

## Featured projects

### [CareerFlow](https://github.com/Joun-Mikhail/careerflow) · full-stack job-search platform

[![CI](https://github.com/Joun-Mikhail/careerflow/actions/workflows/ci.yml/badge.svg)](https://github.com/Joun-Mikhail/careerflow/actions/workflows/ci.yml)
![Coverage](https://img.shields.io/badge/backend_coverage-97%25-3fb950)
![Stack](https://img.shields.io/badge/React_·_FastAPI_·_PostgreSQL-1f2328)
[![Live demo](https://img.shields.io/badge/try_the_demo-no_signup-8b5cf6)](https://frontend-jade-two-zfchqjb5ws.vercel.app)

A production-style SaaS app for running a job search: Kanban pipeline, interviews, offers, tasks, analytics, a document vault and AI-assisted CV tailoring. It runs on the web, installs as a PWA and builds for iOS and Android from one codebase.

- **Layered backend.** Routers handle HTTP, services hold business rules and authorization, repositories own all SQL. Migrations run through Alembic.
- **Operated, not just built.** A `/health` probe returns `503` when the database is down. It also has Sentry error monitoring, structured audit logs, post-deploy smoke tests and a keep-warm job against cold starts.
- **Quality gates.** Pytest, Vitest, Ruff, mypy, ESLint, Bandit and pip-audit run in CI.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Joun-Mikhail/careerflow/main/docs/screenshots/dashboard-dark.png">
  <img alt="CareerFlow dashboard with application stats, upcoming interviews and pending tasks" src="https://raw.githubusercontent.com/Joun-Mikhail/careerflow/main/docs/screenshots/dashboard-light.png" width="100%">
</picture>

<details>
<summary><b>Architecture</b></summary>

```mermaid
flowchart LR
    U(["Web · PWA · mobile builds"]) -->|HTTPS| N["Nginx<br/>static assets + /api proxy"]
    N --> API["FastAPI<br/>routers → services → repositories"]
    API --> PG[("PostgreSQL 16")]
    API --> OBJ[("Object storage<br/>R2 / S3")]
    API -. errors .-> SEN["Sentry"]
    GA["GitHub Actions"] -. "CI · smoke tests · keep-warm" .-> API
```

</details>

### [serverless-notes-api](https://github.com/Joun-Mikhail/serverless-notes-api) · secure notes API on AWS

[![CI](https://github.com/Joun-Mikhail/serverless-notes-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Joun-Mikhail/serverless-notes-api/actions/workflows/ci.yml)
![Coverage](https://img.shields.io/badge/backend_coverage-99%25-3fb950)
![Stack](https://img.shields.io/badge/Lambda_·_Cognito_·_DynamoDB_·_SAM-FF9900)
![Tests](https://img.shields.io/badge/tests-193_passing-3fb950)
[![Live demo](https://img.shields.io/badge/try_the_demo-live-8b5cf6)](https://d11c0a7q5fx9qi.cloudfront.net)

Multi-user private notes app built the way real AWS workloads are built. Users sign in with Amazon Cognito (OAuth 2.0 + PKCE). Five Lambda handlers sit behind API Gateway. Each note is owned by one user — enforced atomically with DynamoDB conditional writes, not application code.

- **Security by design.** Least-privilege IAM: one DynamoDB action per Lambda. JWT scopes (`notes/read`, `notes/write`) validated at API Gateway. Uniform error responses prevent user enumeration.
- **Production-shaped ops.** Structured JSON logging, CloudWatch alarms, throttling, cursor pagination, optimistic locking, input validation at every layer.
- **Quality gates.** 193 tests (99% coverage), mypy strict, ruff, cfn-lint, sam validate, Playwright browser tests, axe accessibility audit — all in CI.
- **Deployed to AWS** (eu-north-1, 2026-11-17): 38/38 live API checks passed including authentication, isolation, CORS and throttling.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Joun-Mikhail/serverless-notes-api/main/evidence/screenshots/08-notes-dark-1280.png">
  <img alt="Serverless Notes — notes list in dark mode" src="https://raw.githubusercontent.com/Joun-Mikhail/serverless-notes-api/main/evidence/screenshots/03-notes-1280.png" width="100%">
</picture>

<details>
<summary><b>Architecture</b></summary>

```mermaid
flowchart LR
    U["Browser · React"] -- "sign in (PKCE)" --> C["Cognito"]
    U -- "HTTPS + Bearer token" --> G["API Gateway<br/>Cognito authorizer"]
    G --> L["Lambda × 5<br/>Python 3.13"]
    L --> D[("DynamoDB<br/>table + byUser GSI")]
    L -. "logs · metrics" .-> W["CloudWatch"]
```

</details>


### [Device Registry API](https://github.com/Joun-Mikhail/device-registry-serverless-api) · serverless REST API on AWS

[![CI](https://github.com/Joun-Mikhail/device-registry-serverless-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Joun-Mikhail/device-registry-serverless-api/actions/workflows/ci.yml)
![Coverage](https://img.shields.io/badge/coverage-92%25-3fb950)
![Stack](https://img.shields.io/badge/Lambda_·_API_Gateway_·_DynamoDB_·_SAM-FF9900)
[![Try it](https://img.shields.io/badge/try_the_app-in_browser-8b5cf6)](https://joun-mikhail.github.io/device-registry-serverless-api/app.html)

The registry that tracks a fleet of connected devices: what each one is, where it is, and whether it works. Five Lambda handlers sit behind API Gateway, all defined in a single SAM template.

- **Deploys with no stored cloud credentials.** GitHub Actions assumes an AWS role through OIDC, then runs `sam deploy` to `eu-central-1`.
- **Query-first data access.** Filtered lists use a DynamoDB GSI `Query` instead of a `Scan`, with cursor pagination.
- **Strict access.** A Lambda authorizer checks an API key held in Secrets Manager, and each function gets only the DynamoDB actions it needs.
- **125 tests.** Unit, contract and integration tests run behind a 91% coverage gate, plus `ruff` and `detect-secrets` pre-commit hooks.

<details>
<summary><b>Architecture</b></summary>

```mermaid
flowchart LR
    C(["Client"]) -->|"HTTPS + x-api-key"| GW["API Gateway<br/>HTTP API"]
    GW --> AUTH{{"Lambda authorizer"}}
    AUTH -. reads key .-> SM[("Secrets Manager")]
    GW --> FN["5 Lambda handlers<br/>create · get · list · update · delete"]
    FN --> DB[("DynamoDB<br/>+ type / createdAt GSI")]
    FN --> CW["CloudWatch<br/>structured logs · alarms · dashboard"]
    subgraph CICD["GitHub Actions"]
        T["pytest · ruff · contract tests"] --> D["OIDC → sam deploy"]
    end
    D -. CloudFormation .-> GW
```

</details>

### [IoT Monitoring System](https://github.com/Joun-Mikhail/iot-monitoring-system) · telemetry pipeline with alerting

![Stack](https://img.shields.io/badge/IoT_Core_·_Lambda_·_CloudWatch_·_SNS-1A9C3E)
![Tests](https://img.shields.io/badge/tests-unit_·_LocalStack_·_live_AWS-3fb950)

Sensors publish over MQTT/TLS to AWS IoT Core. A Lambda function validates each reading, classifies anomalies and emits CloudWatch metrics. An alarm pages on-call through SNS.

- **Failure injection built in.** The device simulator can drop, corrupt, delay or silence messages, so the alerting path is exercised and not just assumed to work.
- **Ready for on-call.** The README includes a **debugging playbook** for each failure mode: missing invoke permissions, certificate errors, import errors and silent alarms.
- **Honest scope.** It is documented as a prototype, with its limitations and design tradeoffs written down (QoS 1 vs 2, direct metrics vs log filters).

<details>
<summary><b>Architecture</b></summary>

```mermaid
flowchart LR
    S["Device simulator<br/>fault injection"] -->|"MQTT/TLS · X.509 · QoS 1"| IOT["AWS IoT Core"]
    IOT -->|IoT Rule| L["Lambda<br/>validate → classify"]
    L --> LOG["CloudWatch Logs"]
    L --> M["CloudWatch Metrics<br/>anomalies · errors · latency"]
    M --> A{"Alarm<br/>≥ 3 anomalies / 5 min"}
    A --> SNS["SNS → on-call email"]
```

</details>

### [Service Watchdog](https://github.com/Joun-Mikhail/service-watchdog) · uptime monitor with alerting

![Stack](https://img.shields.io/badge/Python_·_SMTP_·_YAML_config-3776AB)

A lightweight uptime monitor. It checks a list of endpoints on a schedule and emails once when a service goes down, without spamming on every failed check. When the service recovers, it sends a recovery notice with the total downtime.

<details>
<summary><b>Alert logic</b></summary>

```mermaid
stateDiagram-v2
    direction LR
    [*] --> Up
    Up --> Down: check fails → send DOWN alert
    Down --> Down: still failing → no duplicate alert
    Down --> Up: check passes → send RECOVERY with downtime
```

</details>

## How I ship and operate

The loop I build into my projects: catch problems before merge, deploy without manual steps, and know about failures before users do.

```mermaid
flowchart LR
    A["Commit"] --> B["Pre-commit<br/>lint · secret scan"]
    B --> C["CI<br/>unit · contract · coverage gate"]
    C --> D["Deploy<br/>IaC · OIDC · no stored keys"]
    D --> E["Observe<br/>logs · metrics · health checks"]
    E --> F["Respond<br/>alarm → runbook → fix"]
    F --> A
```

## Live repository status

This board is generated by [a small Python script](scripts/render_status.py) that queries the GitHub API. A [scheduled GitHub Actions workflow](.github/workflows/status-board.yml) tests the script and redraws the board every day. The profile is a tiny pipeline of its own.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/output/status-dark.svg">
  <img alt="Live status of featured repositories: CI result, primary language and last push, plus a language breakdown" src="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/output/status-light.svg" width="100%">
</picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/main/assets/footer-dark.svg">
  <img alt="Let's keep your systems running." src="https://raw.githubusercontent.com/Joun-Mikhail/Joun-Mikhail/main/assets/footer-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://linkedin.com/in/john-mikhaill1"><b>LinkedIn</b></a> ·
  <a href="mailto:mikhailjoun@gmail.com"><b>mikhailjoun@gmail.com</b></a> ·
  Brno, Czech Republic · open to EU relocation
</p>
