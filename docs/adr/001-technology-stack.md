# ADR-001: Initial Technology Stack

## Status

Accepted

## Context

CloudSpend Guard requires a web interface, REST API, AWS resource discovery, persistent storage, infrastructure automation, container orchestration, CI/CD, and observability.

## Decision

The initial technology stack will use:

- React + TypeScript — frontend
- FastAPI + Python — backend API
- boto3 — AWS integration
- PostgreSQL — persistent storage
- Docker — containerization
- Terraform — AWS infrastructure
- Amazon EKS — Kubernetes platform
- Helm — Kubernetes packaging
- Argo CD — GitOps deployment
- GitHub Actions — CI
- Prometheus + Grafana — application/platform observability
- AWS CloudWatch — AWS monitoring and logging

## Rationale

Python provides mature AWS SDK support through boto3 and works well for resource analysis and automation.

React and TypeScript provide a maintainable foundation for an interactive dashboard.

Terraform provides declarative and repeatable AWS infrastructure provisioning.

Kubernetes, Helm, and Argo CD demonstrate production-style container deployment and GitOps practices.

## Consequences

The platform contains multiple infrastructure components and therefore requires careful cost management.

Development will begin locally with lightweight services before AWS infrastructure is provisioned.

Cloud services will be introduced incrementally rather than deploying the complete architecture immediately.
