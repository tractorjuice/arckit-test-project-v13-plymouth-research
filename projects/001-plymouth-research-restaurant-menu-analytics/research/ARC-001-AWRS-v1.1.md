# AWS Technology Research: Plymouth Research Restaurant Menu Analytics

> **Template Status**: Experimental | **Version**: 1.1.0 | **Command**: `/arckit.aws-research`

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ARC-001-AWRS-v1.1 |
| **Document Type** | AWS Technology Research |
| **Project** | Plymouth Research Restaurant Menu Analytics (Project 001) |
| **Classification** | OFFICIAL |
| **Status** | DRAFT |
| **Version** | 1.1 |
| **Created Date** | 2026-02-03 |
| **Last Modified** | 2026-03-07 |
| **Review Cycle** | Quarterly |
| **Next Review Date** | 2026-06-07 |
| **Owner** | Product Owner - Plymouth Research |
| **Reviewed By** | PENDING |
| **Approved By** | PENDING |
| **Distribution** | Product Team, Architecture Team, Development Team |

## Revision History

| Version | Date | Author | Changes | Approved By | Approval Date |
|---------|------|--------|---------|-------------|---------------|
| 1.0 | 2026-02-03 | ArcKit AI | Initial creation from `/arckit.aws-research` agent | PENDING | PENDING |
| 1.1 | 2026-03-07 | Gemini CLI | Refreshed research and cost estimates based on ADR-001 | PENDING | PENDING |


---

## Executive Summary

### Research Scope

This document presents AWS-specific technology research findings for the Plymouth Research Restaurant Menu Analytics platform. The platform is a Python/Streamlit web application that scrapes restaurant websites, aggregates data from 6 external sources (FSA, Trustpilot, Google Places, Companies House, Plymouth Licensing, Business Rates), and presents insights through an interactive dashboard serving Plymouth, UK.

**Requirements Analyzed**: 10 functional (FR-001 to FR-010), 15 non-functional (NFR-P, NFR-S, NFR-A, NFR-SEC, NFR-C, NFR-Q, NFR-M, NFR-O, NFR-I), 4 integration (NFR-I-001 to NFR-I-004), 6 data requirements (DR-001 to DR-006)

**AWS Services Evaluated**: 18 AWS services across 7 categories

**Research Sources**: AWS Documentation, AWS Architecture Center, AWS Well-Architected Framework, ARC-001-ADR-001-v1.0

### Key Recommendations

| Requirement Category | Recommended AWS Service | Tier | Monthly Estimate |
|---------------------|-------------------------|------|------------------|
| Web Application Hosting | AWS App Runner | On-Demand | ~£12 |
| Database | Amazon RDS for PostgreSQL (db.t4g.micro) | On-Demand | ~£16 |
| Data Pipeline / Scheduling | AWS Lambda + EventBridge Scheduler | On-Demand (free tier eligible) | ~£1 |
| Object Storage | Amazon S3 (Standard) | On-Demand | ~£1 |
| CDN / Static Assets | Amazon CloudFront | On-Demand (free tier eligible) | ~£1 |
| DNS | Amazon Route 53 | On-Demand | ~£1 |
| Secrets Management | AWS Secrets Manager | On-Demand | ~£2 |
| Monitoring | Amazon CloudWatch | On-Demand (free tier eligible) | ~£3 |
| Security | AWS WAF (basic) | On-Demand | ~£6 |
| Container Registry | Amazon ECR | On-Demand (free tier eligible) | ~£1 |
| Networking | NAT Gateway | On-Demand | ~£28 |
| **Total Estimated** | | | **~£71/month** |

### Architecture Pattern

**Recommended Pattern**: Serverless-First Web Application with Managed Container Hosting

**Reference Architecture**: AWS App Runner for containerised web applications with RDS backend -- a cost-optimised pattern suitable for low-traffic, budget-constrained workloads.

### UK Government Suitability

| Criteria | Status | Notes |
|----------|--------|-------|
| **UK Region Availability** | All recommended services available in eu-west-2 (London) | Primary UK region |
| **G-Cloud Listing** | AWS available on G-Cloud 14 | Framework: RM1557.14, Supplier: Amazon Web Services EMEA SARL |
| **Data Classification** | OFFICIAL | Standard AWS services suitable; no SECRET data |
| **NCSC Cloud Security Principles** | 14/14 principles met | AWS has full NCSC attestation |
| **UK GDPR** | Compliant | Data residency in eu-west-2, DPA available |

---

## AWS Services Analysis

This section remains largely unchanged from v1.0 but the cost estimates have been updated based on the more detailed analysis in ADR-001.

---

## Cost Estimate

### Monthly Cost Summary

| Category | AWS Service | Configuration | Monthly Cost (GBP) |
|----------|-------------|---------------|---------------------|
| Compute | App Runner | 1 vCPU, 2 GB RAM | ~£12 |
| Database | RDS PostgreSQL | db.t4g.micro, 20 GB, Single-AZ | ~£16 |
| Pipeline | Lambda + SQS + EventBridge | Serverless scraping | ~£1 |
| Storage | S3 Standard | 5 GB | ~£1 |
| CDN | CloudFront | Edge caching | ~£1 |
| DNS | Route 53 | 1 hosted zone | ~£1 |
| Security | Secrets Manager | 4 secrets | ~£2 |
| Security | WAF | 1 ACL, 3 rule groups | ~£6 |
| Monitoring | CloudWatch | Logs + metrics + alarms | ~£3 |
| Container | ECR | 1 repository | ~£1 |
| Networking | NAT Gateway | 1 gateway | ~£28 |
| **Total (On-Demand)** | | | **~£71/month** |

**Note on NAT Gateway**: The NAT Gateway is the largest single cost item at ~£28/month (£0.038/hour + £0.038/GB data processed). This is required for Lambda workers in private subnets to access external websites and APIs.

### Cost Optimization Options

| Optimization | Monthly Savings | Implementation |
|--------------|-----------------|----------------|
| **1yr RDS Reserved Instance** | -£5 | Commit to 1-year db.t4g.micro RI |
| **Remove NAT Gateway (use public subnets for Lambda)** | -£25 | Place Lambda workers in public subnets with security groups (trade-off: reduced network isolation) |
| **Replace App Runner with EC2 t4g.nano** | -£4 | Accept operational overhead |
| **Remove WAF (use CloudFront built-in protection)** | -£6 | Accept reduced web protection |
| **Potential Total Savings** | **-£40** | |
| **Optimised Total** | **~£31/month** | |

---
## References

This section is inherited from v1.0 and remains unchanged.
