# Comprehensive Threat Model (STRIDE)

| Threat | Attack Surface | Mitigation |
| :--- | :--- | :--- |
| **Prompt Injection** | Uploaded course PDFs & chat inputs | System prompt sandboxing, strict delimiter parsing, refusal rules |
| **Tenant Data Leakage** | Cross-tenant REST queries | JPA Tenant filters, repository enforcement, `TenantContext` validation |
| **IDOR / Unauthorized Access** | Course content / Grades | Server-side enrollment verification before delivering signed S3 URLs |
| **Payment Manipulation** | Checkout webhooks | HMAC-SHA256 webhook signatures, Redis idempotency locks |
