# Enterprise SaaS AI-Powered Learning Management System (LMS)

[![CI Pipeline](https://github.com/pittaanji9390-afk/AI-POWERED-LEARNING-MANAGEMENT-SYSTEM/actions/workflows/ci.yml/badge.svg)](https://github.com/pittaanji9390-afk/AI-POWERED-LEARNING-MANAGEMENT-SYSTEM/actions)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Monolith-indigo.svg)](docs/ARCHITECTURE.md)
[![Security](https://img.shields.io/badge/Security-Enterprise%20Multi--Tenant-emerald.svg)](docs/SECURITY.md)

Production-grade, enterprise multi-tenant SaaS Learning Platform and AI Tutoring engine engineered in **Java 21 / Spring Boot 3.3** and **React 19 / TypeScript / Vite / Tailwind CSS**.

---

## 🌟 Core Architecture Highlights
- **AI Abstraction Mesh**: Pluggable vendor SPI (`AiProvider`, `LlmProvider`, `EmbeddingProvider`, `ModerationProvider`) with zero lock-in.
- **RAG & Vector Retrieval**: Hallucination-resistant retrieval grounded in course documents with strict tenant/enrollment authorization checks.
- **Multi-Tenant Isolation**: Hard isolation via `organization_id` filters across databases, cache keys, and file storage.
- **Resilient Learning Engine**: Course builder, streaming video player, quizzes, rubrics, automated/AI-assisted grading, and verifiable credentials.

---

## 📚 Technical Documentation Index

| Document | Description |
| :--- | :--- |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Complete modular monolith architecture, layers, and service boundaries |
| [DATABASE.md](docs/DATABASE.md) | PostgreSQL 16+ ERD, table specs, foreign keys, and indexing strategy |
| [API.md](docs/API.md) | REST API contracts, standard error response format, and OpenAPI specs |
| [AI-ARCHITECTURE.md](docs/AI-ARCHITECTURE.md) | AI SPI provider mesh, prompt versioning, structured validation, and cost tracking |
| [RAG.md](docs/RAG.md) | Document chunking, pgvector embeddings, and hallucination defense pipeline |
| [SECURITY.md](docs/SECURITY.md) | JWT auth, Argon2id, RBAC + Fine-grained permissions, and rate limiting |
| [THREAT-MODEL.md](docs/THREAT-MODEL.md) | Comprehensive STRIDE threat analysis, prompt injection mitigations, and tests |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Docker Compose, Kubernetes HPA manifests, and Nginx ingress |
| [OPERATIONS.md](docs/OPERATIONS.md) | Runbooks, metrics, log formats, health probes, and alert thresholds |
| [BACKUP-RECOVERY.md](docs/BACKUP-RECOVERY.md) | RPO/RTO targets, automated PostgreSQL WAL backups, and disaster recovery |
| [TESTING.md](docs/TESTING.md) | Unit, integration, security, and end-to-end testing strategies |
| [AI-EVALUATION.md](docs/AI-EVALUATION.md) | Benchmark datasets, grounding evaluation metrics, and drift detection |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Git workflows, coding standards, and definition of done checklist |
| [CHANGELOG.md](docs/CHANGELOG.md) | Detailed version history and phase execution milestones |

---

## 🚀 Quick Start (Local Development)

### 1. Start Infrastructure via Docker Compose
```bash
docker compose up -d postgres redis
```

### 2. Run Backend Application
```bash
cd backend
./mvnw spring-boot:run
```

### 3. Run Frontend Application
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173`.
