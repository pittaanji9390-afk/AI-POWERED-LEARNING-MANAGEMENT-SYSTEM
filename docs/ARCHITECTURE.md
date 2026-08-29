# Complete System Architecture & Module Boundaries

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
