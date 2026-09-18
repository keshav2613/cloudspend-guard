# CloudSpend Guard — Architecture

## Problem

Cloud resources created for development, testing, and experimentation are often left running after they are no longer required.

Unused EC2 instances, unattached EBS volumes, idle load balancers, and other resources can generate unnecessary cloud costs.

CloudSpend Guard provides visibility into AWS resource usage and identifies potential cost-saving opportunities.

## MVP

The first release will:

- Discover supported AWS resources using read-only AWS APIs.
- Retrieve cost and utilization information.
- Identify potentially idle or unused resources.
- Estimate potential savings.
- Display findings through a web dashboard.
- Allow recommendations to be filtered by resource type and severity.

CloudSpend Guard will **not automatically stop or delete AWS resources** in the MVP.

## High-Level Architecture

```text
                         User
                          │
                       HTTPS
                          │
                    AWS Load Balancer
                          │
               ┌──────────▼──────────┐
               │     Amazon EKS      │
               │                     │
               │   React Frontend    │
               │          │          │
               │      FastAPI API    │
               │          │          │
               │    Scanner Worker   │
               └──────────┬──────────┘
                          │
             ┌────────────┼─────────────┐
             │            │             │
        AWS APIs     Cost Explorer   CloudWatch
             │
             ▼
      Resource Inventory
             │
             ▼
     Recommendation Engine
             │
             ▼
        PostgreSQL
```

## Application Components

### Frontend

React and TypeScript provide the user-facing dashboard.

The dashboard will display:

- Current estimated cloud spend
- Cost trends
- Resource inventory
- Potential monthly savings
- Optimization recommendations
- Resource utilization information

### API

FastAPI provides REST endpoints consumed by the frontend.

Responsibilities include:

- Resource queries
- Cost information
- Recommendations
- Scan status
- Dashboard aggregation

### Resource Scanner

A Python worker uses the AWS SDK (`boto3`) to collect resource metadata.

Initial resource support will focus on:

- EC2 instances
- EBS volumes
- Elastic Load Balancers

Additional AWS services can be added incrementally.

### Recommendation Engine

Collected resource and utilization data is evaluated against defined rules.

Example:

```text
EC2 CPU utilization < 5% for 7 days
        ↓
Potentially idle resource
        ↓
Generate cost-saving recommendation
```

Recommendations are advisory only.

### Database

PostgreSQL stores:

- Resource inventory snapshots
- Scan results
- Cost information
- Recommendations

## AWS Authentication

The application will not store long-lived AWS access keys.

When deployed to EKS, workloads will use AWS IAM roles associated with Kubernetes workloads.

Permissions will follow least-privilege principles and initially provide read-only access to the AWS APIs required by the scanner.

## Infrastructure

AWS infrastructure will be provisioned using Terraform.

Major components will include:

- VPC
- Public/private subnets
- Amazon EKS
- Amazon ECR
- IAM
- Load balancing
- Database infrastructure
- Monitoring integrations

Terraform will use reusable modules and environment-specific configuration.

## Deployment

Application containers will be packaged with Docker.

Helm will manage Kubernetes application configuration.

Argo CD will provide GitOps-based deployment synchronization.

GitHub Actions will handle CI tasks including:

- Linting
- Automated tests
- Container builds
- Vulnerability scanning
- Terraform validation
- Infrastructure security scanning

## Observability

The platform will use:

- Prometheus for metrics
- Grafana for visualization
- AWS CloudWatch for AWS/platform logs and metrics

Application health endpoints and Kubernetes readiness/liveness probes will be implemented.

## Security

The project will progressively implement:

- IAM least privilege
- No committed credentials
- Environment-based configuration
- AWS Secrets Manager integration
- Container vulnerability scanning
- Infrastructure-as-Code security scanning
- Dependency scanning
- HTTPS
- Kubernetes security controls

## Engineering Principle

CloudSpend Guard will prefer the simplest appropriate AWS service for each workload.

Kubernetes will be used where it demonstrates a realistic container-platform requirement rather than moving every workload into EKS unnecessarily.
