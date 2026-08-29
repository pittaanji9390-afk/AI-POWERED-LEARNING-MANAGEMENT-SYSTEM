# Security Architecture & Authorization Model

## 1. Authentication
- **Access Tokens**: Short-lived (15 minutes) signed with HMAC-SHA256.
- **Refresh Tokens**: Stored in Redis with rotation on every refresh and token revocation support.
- **Password Hashing**: BCrypt (strength 12) / Argon2id.

## 2. Authorization
- RBAC with 8 distinct roles (`SUPER_ADMIN`, `PLATFORM_ADMIN`, `ORGANIZATION_ADMIN`, `TEACHER`, `TEACHING_ASSISTANT`, `STUDENT`, `MODERATOR`, `SUPPORT_AGENT`).
- Fine-grained declarative method security via Spring `@PreAuthorize("hasAuthority('course:publish')")`.
