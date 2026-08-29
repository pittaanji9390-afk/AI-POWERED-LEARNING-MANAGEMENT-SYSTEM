# Comprehensive REST API Specification & Data Contracts

## 1. Authentication Endpoints (`/api/v1/auth`)
- `POST /api/v1/auth/register`: Register learner/instructor with strong password validation.
- `POST /api/v1/auth/login`: Authenticate credentials, return JWT access + refresh tokens.
- `POST /api/v1/auth/refresh`: Rotate refresh token and issue new access token.
- `POST /api/v1/auth/mfa/setup`: Generate TOTP secret and recovery codes.
- `POST /api/v1/auth/mfa/verify`: Verify 6-digit TOTP code and activate MFA.

## 2. Course Management (`/api/v1/courses`)
- `GET /api/v1/courses/catalog`: Search & browse published public courses.
- `POST /api/v1/courses`: Create new course draft (Teacher / Admin).
- `PUT /api/v1/courses/{id}/state`: Transition lifecycle state (`DRAFT` -> `IN_REVIEW` -> `PUBLISHED`).
- `POST /api/v1/courses/{id}/sections`: Add curriculum module section.
- `POST /api/v1/courses/{id}/lessons`: Add video/PDF/interactive lesson.

## 3. Assessments & Exams (`/api/v1/assessments`)
- `POST /api/v1/assessments/quizzes`: Create quiz with deterministic questions.
- `POST /api/v1/assessments/quizzes/{id}/attempt`: Start timed attempt.
- `POST /api/v1/assessments/quizzes/{id}/submit`: Submit answers, compute score, and provide explanation.
- `POST /api/v1/assessments/assignments/{id}/submit`: Submit assignment files or technical writeup.
- `POST /api/v1/assessments/assignments/{id}/grade`: Record teacher rubric evaluation.

## 4. AI Orchestration (`/api/v1/ai`)
- `POST /api/v1/ai/tutor/ask`: Socratic course Q&A with pgvector semantic retrieval and citation tags.
- `POST /api/v1/ai/generate-quiz`: Structured schema quiz generation for teacher approval.
- `POST /api/v1/ai/grade`: Pre-grade subjective assignment submissions based on rubric criteria.

## 5. Payments & Subscriptions (`/api/v1/payments`)
- `POST /api/v1/payments/checkout`: Initialize tokenized Stripe checkout session.
- `POST /api/v1/payments/webhook`: Webhook handler with HMAC-SHA256 signature verification.
- `POST /api/v1/payments/coupons/validate`: Concurrency-safe coupon discount validation.
