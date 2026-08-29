import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# 1. README.md
write("README.md", """# Enterprise SaaS AI-Powered Learning Management System (LMS)

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
""")

# 2. docs/ARCHITECTURE.md
write("docs/ARCHITECTURE.md", """# Complete System Architecture & Module Boundaries

## 1. Architectural Philosophy
The system implements a **Modular Monolith** pattern with clear logical boundaries. Modules communicate via strongly typed Java interfaces, DTOs, and asynchronous domain events.

```
+-------------------------------------------------------------------------------+
|                             CLIENT INTERFACES                                 |
|         React 19 SPA (TanStack Query, Tailwind CSS, Lucide, Axios)            |
+---------------------------------------+---------------------------------------+
                                        | (REST / SSE / WebSockets)
+---------------------------------------v---------------------------------------+
|                           API GATEWAY & SECURITY                              |
|   Rate Limiter (Redis) | JWT Authenticator | Multi-Tenant Request Interceptor  |
+---------------------------------------+---------------------------------------+
                                        |
+---------------------------------------v---------------------------------------+
|                            APPLICATION MODULES                                |
|  - Identity & Auth          - Course & Builder         - AI Tutor (RAG)       |
|  - Organizations (Tenancy)  - Learning Player          - AI Quiz Generator    |
|  - User Profiles            - Quizzes & Question Bank  - Analytics & Reports  |
|  - Media & PDF Ingestion    - Assignments & Grading    - Payments & Coupons   |
+---------------------------------------+---------------------------------------+
                                        |
+---------------------------------------v---------------------------------------+
|                         INFRASTRUCTURE & PERSISTENCE                          |
|  PostgreSQL 16 (Relational + pgvector) | Redis 7 (Cache/Locks) | S3 Object Store |
+-------------------------------------------------------------------------------+
```

## 2. Estimated Lines of Code Target
- Backend domain & business logic: ~20,000 LOC
- Frontend React SPA: ~15,000 LOC
- Automated tests: ~10,000 LOC
- AI / RAG / Personalization engine: ~5,000 LOC
- Database schema & migrations: ~3,000 LOC
- Security, Auth, & Audit logging: ~3,000 LOC
- Infrastructure, Docker, K8s, CI/CD: ~2,500 LOC
- Scripts, documentation & configs: ~2,500 LOC
**Target Codebase: ~61,000 meaningful LOC**
""")

# 3. docs/DATABASE.md
write("docs/DATABASE.md", """# Database Schema & Relational Model Specification

## 1. PostgreSQL 16+ Architecture
- **Schema Management**: Flyway migrations in `backend/src/main/resources/db/migration/`.
- **Primary Keys**: UUID v4 generated via `gen_random_uuid()`.
- **Audit Columns**: `created_at`, `updated_at`, `created_by`, `updated_by`, `version` (optimistic locking).
- **Tenant Isolation**: `organization_id` foreign key on all tenant-bound tables with composite indexes.

## 2. Entity Groups
1. `organizations`, `users`, `user_roles`, `user_permissions`
2. `courses`, `course_sections`, `lessons`, `lesson_resources`
3. `enrollments`, `learning_progress`, `learning_events`
4. `quizzes`, `questions`, `question_options`, `quiz_questions`, `quiz_attempts`
5. `assignments`, `assignment_submissions`, `rubrics`, `grades`
6. `certificates`, `ai_conversations`, `ai_messages`, `audit_logs`
""")

# 4. docs/API.md
write("docs/API.md", """# API Architecture & Endpoint Standards

## 1. Global Standard Response Format
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {},
  "timestamp": "2026-08-29T23:55:00Z",
  "requestId": "9c8b76e1-5e22-4e07-a3a2-094ec2352cb2"
}
```

## 2. Standard Error Response Format
```json
{
  "timestamp": "2026-08-29T23:55:00Z",
  "requestId": "9c8b76e1-5e22-4e07-a3a2-094ec2352cb2",
  "status": 400,
  "code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "fieldErrors": [
    {
      "field": "title",
      "message": "Title is required",
      "rejectedValue": ""
    }
  ]
}
```
""")

# 5. docs/AI-ARCHITECTURE.md
write("docs/AI-ARCHITECTURE.md", """# AI SPI Layer & Model Orchestration

## 1. Zero Vendor Lock-In Provider Mesh
All AI interactions operate through decoupled Java Service Provider Interfaces (SPI):
- `AiProvider`: Core health & telemetry interface
- `LlmProvider`: Chat completion, async streaming, structured JSON schema generation
- `EmbeddingProvider`: Text-to-vector embedding generation (1536 dimension default)
- `ModerationProvider`: Content safety and risk scoring

## 2. Supported Adaptors
1. `MockAiProvider`: Offline testing & deterministic local integration
2. `OpenAiProvider`: OpenAI GPT-4o / text-embedding-3
3. `AzureAiProvider`: Azure OpenAI private endpoints
4. `OllamaProvider`: Local self-hosted models (Llama 3, Mistral)
""")

# 6. docs/RAG.md
write("docs/RAG.md", """# Retrieval-Augmented Generation (RAG) Architecture

## 1. Document Ingestion Pipeline
```
Document Upload (PDF/Doc) 
  --> MIME Validation 
  --> Text Extraction (Apache Tika) 
  --> Recursive Token Chunking (512 tokens, 50 overlap) 
  --> Embedding Generation 
  --> pgvector Storage (HNSW Cosine Index)
```

## 2. Hallucination Control & Prompt Injection Defense
- RAG queries enforce `organization_id` and `course_id` permission checks BEFORE vector search.
- Prompts use explicit boundary delimiters (`<<<COURSE_CONTEXT>>>`) to prevent user documents from overriding system directives.
- If similarity score is below confidence threshold (0.75), tutor triggers refusal behavior: *"The course material does not provide sufficient information."*
""")

# 7. docs/SECURITY.md
write("docs/SECURITY.md", """# Security Architecture & Authorization Model

## 1. Authentication
- **Access Tokens**: Short-lived (15 minutes) signed with HMAC-SHA256.
- **Refresh Tokens**: Stored in Redis with rotation on every refresh and token revocation support.
- **Password Hashing**: BCrypt (strength 12) / Argon2id.

## 2. Authorization
- RBAC with 8 distinct roles (`SUPER_ADMIN`, `PLATFORM_ADMIN`, `ORGANIZATION_ADMIN`, `TEACHER`, `TEACHING_ASSISTANT`, `STUDENT`, `MODERATOR`, `SUPPORT_AGENT`).
- Fine-grained declarative method security via Spring `@PreAuthorize("hasAuthority('course:publish')")`.
""")

# 8. docs/THREAT-MODEL.md
write("docs/THREAT-MODEL.md", """# Comprehensive Threat Model (STRIDE)

| Threat | Attack Surface | Mitigation |
| :--- | :--- | :--- |
| **Prompt Injection** | Uploaded course PDFs & chat inputs | System prompt sandboxing, strict delimiter parsing, refusal rules |
| **Tenant Data Leakage** | Cross-tenant REST queries | JPA Tenant filters, repository enforcement, `TenantContext` validation |
| **IDOR / Unauthorized Access** | Course content / Grades | Server-side enrollment verification before delivering signed S3 URLs |
| **Payment Manipulation** | Checkout webhooks | HMAC-SHA256 webhook signatures, Redis idempotency locks |
""")

# 9. docs/DEPLOYMENT.md
write("docs/DEPLOYMENT.md", """# Deployment Architecture & Infrastructure

## Containerization
- **Multi-Stage Dockerfile** for backend (Eclipse Temurin JRE 21 on Alpine Linux, running as non-root user `ailms`).
- **Nginx Ingress** serving compiled React frontend and routing `/api/*` to backend service.
- **Kubernetes Manifests** with readiness/liveness health probes and Horizontal Pod Autoscaling (HPA).
""")

# 10. docs/OPERATIONS.md
write("docs/OPERATIONS.md", """# Operations, Runbooks & Observability

## Monitoring & Metrics
- Health checks: `/api/v1/health` and Spring Boot `/actuator/health`.
- Prometheus metrics: `/actuator/prometheus`.
- Structured JSON logging with `X-Request-ID` tracing across all layers.
""")

# 11. docs/BACKUP-RECOVERY.md
write("docs/BACKUP-RECOVERY.md", """# Backup & Disaster Recovery Architecture

## Recovery Objectives
- **RPO (Recovery Point Objective)**: < 5 minutes (via PostgreSQL Continuous WAL archiving).
- **RTO (Recovery Time Objective)**: < 30 minutes.

## Backup Routine
1. Daily full database snapshots with AES-256 encryption.
2. Point-in-time recovery (PITR) enabled via pgBackRest / S3 object storage.
""")

# 12. docs/TESTING.md
write("docs/TESTING.md", """# Quality Assurance & Testing Strategy

- **Backend Unit & Integration Tests**: JUnit 5, Mockito, Spring Security Test, Testcontainers.
- **Security & Authorization Tests**: Tenant boundary tests, permission matrix tests.
- **Deterministic AI Tests**: Structured schema compliance, RAG grounding, prompt injection resistance.
""")

# 13. docs/AI-EVALUATION.md
write("docs/AI-EVALUATION.md", """# AI Evaluation Framework & Quality Benchmarks

## Evaluation Metrics
1. **Factual Grounding**: Percentage of generated claims traceable directly to source context.
2. **Citation Precision**: Verification that cited module/page exists and supports claim.
3. **Refusal Correctness**: Proper refusal when answering out-of-domain questions.
""")

# 14. docs/CONTRIBUTING.md
write("docs/CONTRIBUTING.md", """# Developer Guidelines & Definition of Done

## Definition of Done (DoD)
Every feature must include:
1. JPA Entity + Flyway Migration
2. Repository with tenant isolation
3. Service with business rules & transactional boundaries
4. REST Controller with DTO validation & Swagger annotations
5. React UI component with loading/error/empty states
6. Automated unit/integration tests
""")

# 15. docs/CHANGELOG.md
write("docs/CHANGELOG.md", """# System Changelog

## [1.0.0-PHASE1] - 2026-08-29
### Added
- Foundation architecture documentation across all 14 domains.
- Java 21 / Spring Boot 3.3 backend modular monolith project structure with Maven POM.
- Core configs: OpenAPI, Security, CORS, Jackson, Redis Cache, Async thread pools.
- Standard API response contracts, ErrorCode enumeration, and GlobalExceptionHandler.
- Multi-tenant domain base (`BaseEntity`, `AuditableEntity`, `TenantAwareEntity`).
- Security architecture: JWT Token Provider, JWT Filter, UserPrincipal, UserRole, Permission.
- Pluggable AI SPI Mesh (`AiProvider`, `LlmProvider`, `EmbeddingProvider`, `ModerationProvider`, `MockAiProvider`).
- Subsystem SPIs (`SearchService`, `ObjectStorageService`, `PaymentGatewayProvider`, `NotificationSender`).
- Flyway V1 PostgreSQL initial schema covering multi-tenancy, courses, quizzes, assignments, certificates, and audit logs.
- React 19 + TypeScript + Vite + Tailwind CSS frontend with layouts, UI components, catalog, player, and AI tutor studio.
- Docker Compose, Kubernetes manifests, Nginx configs, and GitHub Actions CI workflow.
""")

print("All documentation files written successfully.")
