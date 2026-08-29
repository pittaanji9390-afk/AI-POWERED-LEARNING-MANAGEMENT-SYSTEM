# Deployment Architecture & Infrastructure

## Containerization
- **Multi-Stage Dockerfile** for backend (Eclipse Temurin JRE 21 on Alpine Linux, running as non-root user `ailms`).
- **Nginx Ingress** serving compiled React frontend and routing `/api/*` to backend service.
- **Kubernetes Manifests** with readiness/liveness health probes and Horizontal Pod Autoscaling (HPA).
