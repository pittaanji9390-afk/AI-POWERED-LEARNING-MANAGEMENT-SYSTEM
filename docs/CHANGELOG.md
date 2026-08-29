# System Changelog

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
