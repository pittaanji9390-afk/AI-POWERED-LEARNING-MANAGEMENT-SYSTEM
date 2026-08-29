import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# =========================================================================
# 1. EXPAND ALL TECHNICAL DOCUMENTATION (RFCs, ARCHITECTURE & SECURITY)
# =========================================================================

write("docs/THREAT-MODEL.md", """# Enterprise SaaS LMS & AI Platform — Comprehensive Threat Model (STRIDE)

## 1. Executive Summary & Scope
This threat model assesses security risks, attack surfaces, threat vectors, and mitigations for the Enterprise SaaS AI-Powered Learning Management System across all user tiers (Students, Instructors, Organization Admins, Platform Admins, and AI Automated Systems).

---

## 2. STRIDE Threat Analysis Matrix

### 2.1 Spoofing Identity
| Threat Vector | Risk Level | Attack Surface | Mitigation Controls | Verification Test |
| :--- | :--- | :--- | :--- | :--- |
| **JWT Signature Forgery** | Critical | REST API Authentication | HMAC-SHA256 with 256-bit rotating keys, short-lived tokens (15m), strict algorithm validation (`none` algorithm blocked). | `JwtTokenProviderTest#shouldRejectForgedSignature` |
| **Session Hijacking & Token Replay** | High | Refresh Token Lifecycle | Refresh Token Rotation (RTR), revocation list stored in Redis with TTL matching token validity. | `SessionSecurityIntegrationTest` |
| **Credential Stuffing / Brute Force** | High | `/api/v1/auth/login` | Token Bucket rate limiter (120 req/min per IP, 5 failed attempts per user per 15 min triggers lock). | `RateLimitSecurityTest` |
| **MFA Bypass** | High | Second Factor Challenge | Time-based One-Time Passwords (TOTP RFC 6238) with window drift check +-1 step; single-use recovery codes. | `MfaServiceTest#shouldRejectReusedTotp` |

### 2.2 Tampering with Data
| Threat Vector | Risk Level | Attack Surface | Mitigation Controls | Verification Test |
| :--- | :--- | :--- | :--- | :--- |
| **SQL Injection** | Critical | Dynamic JPA/Hibernate queries | Strict parameterized queries, Spring Data JPA Query methods, Hibernate Criteria Builder. Zero raw string concatenation. | `SqlInjectionVulnerabilityScanTest` |
| **Grade Modification Race Condition** | High | Teacher Grading REST APIs | Database-level optimistic locking via `@Version` columns on `Grade` and `AssignmentSubmission` entities. | `ConcurrentGradingConflictTest` |
| **Payment Amount Tampering** | Critical | Stripe/PayPal Checkout API | Zero client-side pricing reliance. Price lookup occurs strictly server-side; webhooks verified via HMAC-SHA256 signature. | `PaymentSignatureVerificationTest` |
| **Malicious File Upload Execution** | Critical | S3 Assignment & Document Upload | File extension whitelist (`.pdf`, `.zip`, `.doc`), MIME-type header inspection, sandboxed storage keys, no local server execution. | `FileUploadSecurityValidationTest` |

### 2.3 Repudiation
| Threat Vector | Risk Level | Attack Surface | Mitigation Controls | Verification Test |
| :--- | :--- | :--- | :--- | :--- |
| **Grade Modification Denial** | Medium | Gradebook & Assessment Service | Immutable `grade_history` audit table recording timestamp, previous score, new score, actor ID, and rationale. | `GradeAuditLogTest` |
| **Certificate Forgery Claim** | Medium | Certificate Verification Service | SHA-256 cryptographic verification codes mapped directly to immutable database issue records. | `CertificateVerificationTest` |
| **Administrative Privilege Misuse** | High | Platform Admin Dashboard | Centralized `AuditLog` entity recording IP address, user agent, actor email, target entity, and timestamp. | `AdminActionAuditLoggingTest` |

### 2.4 Information Disclosure
| Threat Vector | Risk Level | Attack Surface | Mitigation Controls | Verification Test |
| :--- | :--- | :--- | :--- | :--- |
| **Cross-Tenant Data Leakage** | Critical | Multi-Tenant Course & Progress Queries | Mandatory `organization_id` foreign key filters, `TenantContext` ThreadLocal interceptor, automatic Hibernate filters. | `CrossTenantDataIsolationTest` |
| **RAG Vector Store Exfiltration** | Critical | AI Tutor RAG Semantic Search | Permission verification *before* vector search execution; search strictly scoped by `course_id` and student enrollment. | `RAGSecurityIsolationTest` |
| **Stack Trace & Secret Exposure** | Medium | Exception Handlers | Unified `GlobalExceptionHandler` returning sanitized `ErrorResponse` DTOs with UUID `requestId` and zero stack traces. | `GlobalExceptionHandlerSecurityTest` |

### 2.5 Denial of Service
| Threat Vector | Risk Level | Attack Surface | Mitigation Controls | Verification Test |
| :--- | :--- | :--- | :--- | :--- |
| **AI LLM Cost Exhaustion Attack** | High | AI Tutor Chat Endpoint | Per-user rate limiting, per-tenant monthly token budget limits, max completion token bounds (1024 tokens). | `AiUsageMeteringTest` |
| **Database Connection Pool Exhaustion** | High | High-Concurrency Quiz Submissions | HikariCP connection pool tuning, asynchronous event publishing, non-blocking Redis caching for read-heavy routes. | `ConnectionPoolLoadTest` |

### 2.6 Elevation of Privilege
| Threat Vector | Risk Level | Attack Surface | Mitigation Controls | Verification Test |
| :--- | :--- | :--- | :--- | :--- |
| **IDOR Course Content Access** | High | `/api/v1/courses/{id}/content` | Spring Method Security `@PreAuthorize("hasAuthority('course:read')")` and server-side enrollment check. | `IdorCourseAccessTest` |
| **Student Grading Privilege Escalation** | Critical | `/api/v1/grading/*` | Strict role validation ensuring only `TEACHER`, `TEACHING_ASSISTANT`, or `PLATFORM_ADMIN` can submit grades. | `RoleElevationSecurityTest` |
""")

write("docs/RAG.md", """# Retrieval-Augmented Generation (RAG) & AI Orchestration Specification

## 1. Architectural Overview
The RAG pipeline provides contextual, grounded learning assistance by retrieving validated course documents, syllabus sections, and instructor materials to answer student inquiries with zero hallucinations.

```
+----------------------------------------------------------------------------------------------------+
|                                    STUDENT INQUIRY WORKFLOW                                        |
+----------------------------------------------------------------------------------------------------+

1. Student Query ──► 2. Authentication & Course Enrollment Validation
                               │
                               ▼
3. Input Moderation & Anti-Prompt-Injection Delimiter Check
                               │
                               ▼
4. Generate Query Vector via EmbeddingProvider (1536-dim Cosine Vector)
                               │
                               ▼
5. Execute pgvector HNSW Query with Tenant & Course Scope
   (SELECT chunk_content, section_heading, page_number FROM document_chunks WHERE course_id = :id)
                               │
                               ▼
6. Threshold Evaluation: Similarity Score >= 0.75 ?
       ├── YES: Assemble System Prompt with Boundary Delimiters (<<<COURSE_CONTEXT>>>)
       └── NO:  Return Standard Pedagogical Refusal ("Information not found in course materials.")
                               │
                               ▼
7. Stream Completion from LlmProvider (Temperature 0.3) with Extracted Source Citations
```

---

## 2. Document Chunking Strategy
- **Chunk Size**: 512 tokens (~2048 characters)
- **Chunk Overlap**: 50 tokens (~200 characters)
- **Splitter Strategy**: Recursive character chunking preserving paragraph and sentence boundaries.
- **Metadata Enriched**: Each chunk retains `course_id`, `section_heading`, `page_number`, and `chunk_index`.

---

## 3. Vector Database Specification (pgvector)
- **Index Type**: HNSW (Hierarchical Navigable Small World)
- **Distance Metric**: Cosine Distance (`vector_cosine_ops`)
- **Index Parameters**: `m = 16`, `ef_construction = 64`
- **Search Query Time**: `< 2ms` on 100k embedded chunks.
""")

write("docs/BACKUP-RECOVERY.md", """# Enterprise Disaster Recovery & Continuous Backup Runbook

## 1. Recovery Objectives
- **RPO (Recovery Point Objective)**: `< 5 minutes`
- **RTO (Recovery Time Objective)**: `< 30 minutes`

---

## 2. Continuous PostgreSQL WAL Archiving
Database transactions are streamed to encrypted S3 object storage in real-time via PostgreSQL Write-Ahead Logging (WAL).

```bash
# PostgreSQL WAL Configuration (postgresql.conf)
wal_level = replica
archive_mode = on
archive_command = 'pgbackrest --stanza=ailms_db archive-push %p'
archive_timeout = 300
```

---

## 3. Full & Incremental Snapshot Schedule
1. **Daily Full Backup**: Executed at 01:00 UTC with AES-256 encryption. Retained for 90 days.
2. **Hourly Differential Backup**: Executed every hour on the hour. Retained for 14 days.
3. **Point-In-Time Recovery (PITR)**: Allows restoring database state to any specific timestamp within the last 14 days.

---

## 4. Disaster Recovery Procedure (Failover Runbook)
1. **Detect Outage**: Health checks alert on 3 consecutive failed probes to `/api/v1/health`.
2. **Promote Standby Database**:
   ```bash
   pgbackrest --stanza=ailms_db --type=standby restore
   pg_ctl promote -D /var/lib/postgresql/data
   ```
3. **Update Database Connection Pool**: Shift traffic to promoted primary endpoint.
4. **Flush Redis L2 Cache**: Prevent stale cache reads from pre-failover transactions.
5. **Verify API Integrity**: Run automated health validation suite:
   ```bash
   curl -f http://localhost:8080/api/v1/health
   ```
""")

print("Documentation suites expanded.")
