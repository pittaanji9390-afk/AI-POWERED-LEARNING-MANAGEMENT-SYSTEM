# Database Schema & Relational Model Specification

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
