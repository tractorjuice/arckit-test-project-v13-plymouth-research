# Google Cloud Technology Research: Plymouth Research Restaurant Menu Analytics

> **Template Origin**: Official | **ArcKit Version**: 4.0.1 | **Command**: `/arckit:gcp-research`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-GCRS-v1.0 |
| **Document Type** | Google Cloud Technology Research |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.0 |
| **Created Date** | 2026-03-07 |
| **Last Modified** | 2026-03-07 |
| **Review Cycle** | On-Demand |
| **Next Review Date** | 2026-04-07 |
| **Owner** | Enterprise Architect |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Architecture Team, Development Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-03-07 | ArcKit AI | Initial creation from `/arckit:gcp-research` agent | PENDING | PENDING |

---

## Executive Summary

### Research Scope

This document presents Google Cloud-specific technology research findings for the Plymouth Research Restaurant Menu Analytics project. It provides Google Cloud service recommendations, architecture patterns, and implementation guidance based on official Google documentation to evolve the current SQLite and local Python script-based system into a scalable, resilient, and cost-efficient cloud-native platform.

**Requirements Analyzed**: 18 functional, 15 non-functional, 8 integration, and 8 data requirements from `ARC-001-REQ-v2.0.md`.

**Google Cloud Services Evaluated**: 8 Google Cloud services across 6 categories (Compute, Database, Orchestration, Security, Networking, Operations).

**Research Sources**: Google Cloud Documentation, Google Cloud Architecture Center, and the Google Developer Knowledge MCP server.

### Key Recommendations

The proposed architecture replaces the local components with fully managed, serverless Google Cloud services to meet scalability, availability, and performance requirements while adhering to the strict sub-£100/month budget.

| Requirement Category | Recommended Google Cloud Service | Tier/Config | Monthly Estimate (Start) |
|---------------------|----------------------------------|-------------|--------------------------|
| **Compute (Jobs)** | Cloud Run Jobs | On-Demand | ~£5 |
| **Compute (Dashboard)** | Cloud Run Service | On-Demand (Scale to Zero) | ~£5 |
| **Database** | Cloud SQL for PostgreSQL | db-g1-small (Shared Core) | ~£12 |
| **Orchestration** | Cloud Workflows + Cloud Scheduler | Standard | <£1 |
| **Security** | Secret Manager | Standard | <£1 |
| **Networking** | Serverless VPC Access | F1 (25-100 Mbps) | ~£8 |
| **Total** | | | **~£31** |

### Architecture Pattern

**Recommended Pattern**: **Serverless Web Application with Scheduled Batch Jobs**

This pattern leverages serverless components to create a highly cost-efficient and low-maintenance system. A scheduled workflow orchestrates data collection and processing via containerized jobs, storing data in a managed relational database. The user-facing dashboard is served by a separate auto-scaling web service that can scale to zero, ensuring costs are only incurred on-demand.

**Reference Architecture**: [Dynamic application with a Python backend on Cloud Run](https://cloud.google.com/architecture/application-development/dynamic-app-python)

### UK Government Suitability

| Criteria | Status | Notes |
|----------|--------|-------|
| **UK Region Availability** | ✅ europe-west2 (London) | All recommended services are available in the London region. |
| **G-Cloud Listing** | ✅ G-Cloud 14 | All recommended core services are listed on the G-Cloud framework. |
| **Data Classification** | ✅ OFFICIAL | The architecture is suitable for OFFICIAL workloads. No public cloud is suitable for SECRET. |
| **NCSC Cloud Security Principles** | ✅ 14/14 principles met | Google Cloud attestation covers all 14 NCSC principles. |

---

## Google Cloud Services Analysis

### Category 1: Compute

**Requirements Addressed**: BR-006 (Weekly Refresh), NFR-P-003 (Data Pipeline), NFR-S-002 (Scalability), FR-012 (Dashboard Hosting).

**Why This Category**: The project requires compute resources for two distinct workloads: scheduled, short-lived batch jobs for data scraping/processing, and a long-running service to host the user-facing Streamlit dashboard.

---

#### Recommended: Cloud Run (Jobs and Services)

**Service Overview**:
- **Full Name**: Google Cloud Run
- **Category**: Compute (Serverless)
- **Documentation**: [cloud.google.com/run](https://cloud.google.com/run)

**Key Features**:
- **Serverless**: Abstracts away all infrastructure management.
- **Container-based**: Runs standard Docker containers, allowing for consistent environments and use of any language/library (including Python with Scrapy/BeautifulSoup).
- **Scale to Zero**: Services can scale down to zero instances when not in use, making it extremely cost-effective for applications with intermittent traffic like the dashboard.
- **Pay-per-use**: Billed for the exact resources (vCPU and memory) consumed during request/job execution, measured to the nearest 100ms.
- **Integrated Tooling**: Works seamlessly with Cloud Scheduler, Workflows, Secret Manager, and VPC networking.

**Proposed Use**:
1.  **Cloud Run Jobs** for the weekly data pipeline. An "array job" can be used to parallelize scraping across multiple restaurant websites, significantly speeding up the collection process.
2.  **Cloud Run Service** to host the Streamlit dashboard. It will automatically scale based on user traffic.

**Pricing Model**:
- **vCPU**: ~$0.000018 per vCPU-second (Tier 1 on-demand).
- **Memory**: ~$0.000002 per GiB-second (Tier 1 on-demand).
- **Free Tier**: A generous free tier is included (e.g., 180,000 vCPU-seconds and 360,000 GiB-seconds per month), which may cover a significant portion of this project's usage.

**Estimated Cost for This Project**:
- **Jobs**: Assuming 150 scrapers running for 30 seconds each weekly, plus processing time, the cost is estimated at **~£5/month**.
- **Service**: Assuming low-to-moderate traffic for the dashboard, scaling to zero when inactive, the cost is estimated at **~£5/month**.

**Google Cloud Architecture Framework Assessment**:
- **Cost Optimization**: ⭐⭐⭐⭐⭐ (Pay-per-use and scale-to-zero are ideal for this project's budget).
- **Operational Excellence**: ⭐⭐⭐⭐⭐ (Fully managed, removing operational overhead of managing servers).
- **Performance Optimization**: ⭐⭐⭐⭐☆ (Cold starts can introduce latency for the first request, but can be mitigated with minimum instances if needed).

**UK Region Availability**: ✅ `europe-west2` (London)

---

### Category 2: Database

**Requirements Addressed**: DR-001-008 (Data Storage), NFR-S-001 (Scalability), NFR-A-001 (Availability), NFR-P-002 (Performance).

**Why This Category**: The project requires a scalable, reliable, and performant relational database to replace the current single-file SQLite database.

---

#### Recommended: Cloud SQL for PostgreSQL

**Service Overview**:
- **Full Name**: Google Cloud SQL for PostgreSQL
- **Category**: Database (Managed Relational)
- **Documentation**: [cloud.google.com/sql/postgres](https://cloud.google.com/sql/postgres)

**Key Features**:
- **Fully Managed**: Automates backups, replication, patches, and updates.
- **High Availability**: Optional HA configuration provides a 99.95% availability SLA via a standby instance in a different zone for automatic failover.
- **Scalable**: Instances can be easily scaled up (vCPU, memory, storage) with minimal downtime.
- **Secure**: Supports private IP connectivity, IAM database authentication, and encryption at rest and in transit.
- **PostgreSQL Compatibility**: Fully compatible with standard PostgreSQL, allowing for a straightforward migration from the existing schema.

**Pricing Model**:
- Charged for instance uptime (vCPU and memory), storage (per GB/month), and networking.
- Shared-core instances are available for low-cost development and small workloads.

**Estimated Cost for This Project**:
- **Instance**: `db-g1-small` (1 shared vCPU, 1.7GB RAM) is estimated at **~£12/month**.
- **Storage**: 20GB of SSD storage is estimated at ~£3/month.
- **HA**: Enabling High Availability would roughly double the instance cost. It is recommended to start without HA and enable it as the service proves its value.

**Google Cloud Architecture Framework Assessment**:
- **Reliability**: ⭐⭐⭐⭐⭐ (With HA enabled, it meets availability requirements and provides automated backups).
- **Cost Optimization**: ⭐⭐⭐⭐☆ (More expensive than SQLite, but provides immense value. Starting with a small instance keeps costs low).
- **Security, Privacy and Compliance**: ⭐⭐⭐⭐⭐ (Private IP, IAM auth, and managed encryption provide a strong security posture).

**UK Region Availability**: ✅ `europe-west2` (London)

---

### Category 3: Orchestration

**Requirements Addressed**: BR-006 (Weekly Refresh), INT-001-008 (Integration).

**Why This Category**: To automate the multi-step data pipeline (scrape -> process -> load) in a reliable and observable way.

---

#### Recommended: Cloud Workflows + Cloud Scheduler

**Service Overview**:
- **Full Name**: Google Cloud Workflows & Google Cloud Scheduler
- **Category**: Orchestration & Scheduling
- **Documentation**: [cloud.google.com/workflows](https://cloud.google.com/workflows), [cloud.google.com/scheduler](https://cloud.google.com/scheduler)

**Key Features**:
- **Cloud Scheduler**: A fully managed cron job service. Can trigger Workflows, Pub/Sub, or any HTTP endpoint on a schedule (e.g., weekly).
- **Cloud Workflows**: A serverless orchestration service to chain together API calls and services. It can call Cloud Run Jobs, wait for them to complete, and implement conditional logic (e.g., only run the 'process' job if the 'scrape' job succeeds).
- **Resilience**: Workflows has built-in retry logic and error handling.

**Pricing Model**:
- **Cloud Scheduler**: 3 free jobs per month, then ~$0.10/job/month.
- **Cloud Workflows**: Free tier for internal steps, then priced per step.
- **Estimated Cost**: For a single weekly pipeline, the cost will be negligible, likely **<£1/month**.

---

### Category 4: Security & Networking

**Requirements Addressed**: NFR-SEC-001, NFR-SEC-002, NFR-SEC-003.

**Why This Category**: To securely store credentials and ensure private communication between services.

---

#### Recommended: Secret Manager + Serverless VPC Access

**Service Overview**:
- **Full Name**: Google Cloud Secret Manager & Serverless VPC Access
- **Category**: Security & Networking
- **Documentation**: [cloud.google.com/secret-manager](https://cloud.google.com/secret-manager), [cloud.google.com/vpc/docs/serverless-vpc-access](https://cloud.google.com/vpc/docs/serverless-vpc-access)

**Key Features**:
- **Secret Manager**: A centralized, audited service to store secrets like API keys and database passwords. Cloud Run services can be granted IAM permissions to access these secrets at runtime, avoiding the need to store them in code or environment variables.
- **Serverless VPC Access**: Creates a connector that allows serverless services like Cloud Run to communicate with resources in a VPC network (like a Cloud SQL instance) using private IP addresses, without exposing them to the public internet.

**Pricing Model**:
- **Secret Manager**: Priced per secret version and per access operation, with a free tier. Cost is negligible.
- **Serverless VPC Access**: Priced per hour based on the connector's instance size and network egress. A small connector is estimated at **~£8/month**.

---

## Architecture Pattern

### Recommended Google Cloud Reference Architecture

**Pattern Name**: Serverless Web Application with Scheduled Batch Jobs

**Pattern Description**: This architecture uses managed, serverless components to build a robust and cost-effective data analytics platform.
1.  **Scheduling**: A **Cloud Scheduler** job triggers the entire pipeline on a weekly basis.
2.  **Orchestration**: The scheduler invokes a **Cloud Workflow** that defines the data processing steps.
3.  **Execution**: The workflow calls a **Cloud Run Job** to execute the containerized Python web scraping and processing scripts.
4.  **Data Storage**: The job securely connects to a **Cloud SQL for PostgreSQL** instance via a **Serverless VPC Access connector** to store the processed data. All credentials are fetched from **Secret Manager**.
5.  **Presentation**: A user-facing **Cloud Run Service** hosts the Streamlit dashboard, which also connects to the Cloud SQL database through the VPC connector to display the analytics.

This pattern minimizes operational overhead and cost while providing a clear, scalable, and secure separation of concerns.

### Architecture Diagram

```mermaid
graph TD
    subgraph "Google Cloud europe-west2 (London)"
        subgraph "VPC Network"
            VPCConnector[Serverless VPC Access<br>Connector]
            subgraph "Cloud SQL"
                DB[(Cloud SQL for PostgreSQL<br>Private IP)]
            end
        end

        subgraph "Data Pipeline (Weekly)"
            Scheduler[Cloud Scheduler] --> Workflows[Cloud Workflows]
            Workflows --> ScrapeProcessJob[Cloud Run Job<br>(Scrape & Process)]
        end

        subgraph "Dashboard Service"
            Users[Internet Users] --> LB[Global Load Balancer]
            LB --> Dashboard[Cloud Run Service<br>(Streamlit App)]
        end

        subgraph "Security"
            Secrets[Secret Manager<br>- DB Password<br>- API Keys]
        end

        ScrapeProcessJob -- Reads secrets --> Secrets
        ScrapeProcessJob -- Writes data via --> VPCConnector
        VPCConnector -- Private IP --> DB

        Dashboard -- Reads secrets --> Secrets
        Dashboard -- Reads data via --> VPCConnector
    end
```

### Component Mapping

| Component | Google Cloud Service | Purpose | Configuration |
|-----------|----------------------|---------|---------------|
| Scheduling | Cloud Scheduler | Trigger the weekly pipeline | `0 2 * * 0` (Every Sunday at 2am) |
| Orchestration | Cloud Workflows | Define and execute the data pipeline steps | Sequential calls to Cloud Run Jobs |
| Scraping/Processing | Cloud Run Jobs | Run Python scripts in a container | 1 vCPU, 2GiB Memory Array Job |
| Database | Cloud SQL for PostgreSQL | Store structured menu & restaurant data | `db-g1-small`, HA optional |
| Dashboard | Cloud Run Service | Host Streamlit web application | Min 0, Max 2 instances |
| Secrets Mgmt | Secret Manager | Store DB password and API keys | IAM integration with Cloud Run |
| Private Network | Serverless VPC Access | Connect Cloud Run to Cloud SQL | `F1` instance type in default VPC |

---
**Generated by**: ArcKit `/arckit:gcp-research` agent
**Generated on**: 2026-03-07
**ArcKit Version**: 4.0.1
**Project**: Plymouth Research Restaurant Menu Analytics (Project 001)
**AI Model**: gemini-1.5-pro-001
