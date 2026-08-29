import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# =========================================================================
# 1. DATABASE MIGRATIONS V6 TO V10 (SEED CATALOG, VIEWS, PROCEDURES)
# =========================================================================
write("backend/src/main/resources/db/migration/V6__enterprise_catalog_seed.sql", """
-- V6: Enterprise Course Catalog and Curriculum Comprehensive Seed Data

INSERT INTO organizations (id, name, slug, tier, max_seats, status, created_at, updated_at)
VALUES 
  ('00000000-0000-0000-0000-000000000001', 'Default Enterprise Academy', 'default-academy', 'ENTERPRISE', 5000, 'ACTIVE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('00000000-0000-0000-0000-000000000002', 'Acme Global Engineering Institute', 'acme-global', 'ENTERPRISE', 2500, 'ACTIVE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('00000000-0000-0000-0000-000000000003', 'CloudNative Tech University', 'cloud-native', 'PRO', 1000, 'ACTIVE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Seed Course 1: Advanced Distributed Systems & Microservices
INSERT INTO courses (id, organization_id, instructor_id, title, slug, short_description, description, category, difficulty, price, currency, status, is_public, created_at, updated_at)
VALUES (
  '11111111-1111-1111-1111-111111111111',
  '00000000-0000-0000-0000-000000000001',
  '00000000-0000-0000-0000-000000000000',
  'Advanced Distributed Systems & Microservices Architecture',
  'advanced-distributed-systems-architecture',
  'Master high-throughput event-driven microservices, consensus algorithms, and distributed transactions.',
  'This masterclass covers Paxos, Raft, Byzantine fault tolerance, multi-region database replication, pgvector semantic search, and distributed sagas with zero data loss guarantees.',
  'Architecture',
  'ADVANCED',
  149.00,
  'USD',
  'PUBLISHED',
  TRUE,
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
) ON CONFLICT (id) DO NOTHING;

-- Seed Sections for Course 1
INSERT INTO course_sections (id, course_id, title, description, sequence_order, created_at, updated_at)
VALUES
  ('22222222-1111-1111-1111-111111111101', '11111111-1111-1111-1111-111111111111', 'Module 1: Distributed Consensus & Partition Tolerance', 'Raft and Paxos state machine replication in modern systems.', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('22222222-1111-1111-1111-111111111102', '11111111-1111-1111-1111-111111111111', 'Module 2: Enterprise RAG Architecture & Vector Indexing', 'Building low-latency retrieval pipelines with PostgreSQL pgvector and HNSW.', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('22222222-1111-1111-1111-111111111103', '11111111-1111-1111-1111-111111111111', 'Module 3: Multi-Tenant Sagas & Compensating Transactions', 'Orchestration vs choreography in tenant-isolated distributed workflows.', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('22222222-1111-1111-1111-111111111104', '11111111-1111-1111-1111-111111111111', 'Module 4: DevSecOps, Chaos Engineering & Zero-Downtime Releases', 'Canary deployments, circuit breaking with Resilience4j, and blue-green database migrations.', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Seed Lessons for Course 1
INSERT INTO lessons (id, section_id, title, lesson_type, duration_seconds, content_body, sequence_order, is_preview_allowed, created_at, updated_at)
VALUES
  ('33333333-1111-1111-1111-111111111101', '22222222-1111-1111-1111-111111111101', '1.1 Foundations of Distributed Consensus: Raft vs Paxos', 'VIDEO', 1200, 'Comprehensive video lecture exploring leader election, log replication, and commit index management.', 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('33333333-1111-1111-1111-111111111102', '22222222-1111-1111-1111-111111111101', '1.2 Implementing Raft Heartbeats & Split Vote Resolution', 'CODE_LAB', 900, 'Hands-on Java lab simulating randomized election timers and network partition healing.', 2, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('33333333-1111-1111-1111-111111111103', '22222222-1111-1111-1111-111111111102', '2.1 Vector Databases in Production: pgvector HNSW Tuning', 'VIDEO', 1440, 'Deep dive into cosine distance, IVFFlat vs HNSW, index build time tradeoffs, and memory footprints.', 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('33333333-1111-1111-1111-111111111104', '22222222-1111-1111-1111-111111111102', '2.2 RAG Grounding & Anti-Prompt-Injection Delimiters', 'DOCUMENT', 720, 'Technical guide on sandboxing retrieved PDF chunks with explicit boundary tags.', 2, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('33333333-1111-1111-1111-111111111105', '22222222-1111-1111-1111-111111111103', '3.1 Distributed Saga Orchestration with Spring Boot 3.3', 'VIDEO', 1800, 'Building stateful saga coordinators using Spring State Machine and Kafka message streams.', 1, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('33333333-1111-1111-1111-111111111106', '22222222-1111-1111-1111-111111111104', '4.1 Chaos Engineering with Chaos Monkey & Kubernetes Probes', 'VIDEO', 1100, 'Simulating network latency spikes and verifying zero packet drop failover.', 1, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;
""")

write("backend/src/main/resources/db/migration/V7__seed_skill_trees_and_paths.sql", """
-- V7: Skill Taxonomy, Competencies, and Adaptive Learning Paths Seed Data

INSERT INTO skills (id, name, slug, category, description, created_at, updated_at)
VALUES
  ('44444444-1111-1111-1111-111111111101', 'Distributed Systems Consensus', 'distributed-consensus', 'Architecture', 'Mastery of Raft and Paxos state machine replication.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('44444444-1111-1111-1111-111111111102', 'Vector Embeddings & Semantic Search', 'vector-embeddings', 'AI Engineering', 'High-dimensional cosine indexing and similarity retrieval.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('44444444-1111-1111-1111-111111111103', 'RAG Security & Prompt Sandboxing', 'rag-security', 'AI Security', 'Preventing indirect prompt injection in RAG pipelines.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('44444444-1111-1111-1111-111111111104', 'Multi-Tenant Database Partitioning', 'multi-tenant-db', 'Database', 'Row and schema level tenant data isolation.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('44444444-1111-1111-1111-111111111105', 'Asynchronous Event-Driven Messaging', 'event-driven-messaging', 'Architecture', 'RabbitMQ and Kafka streaming with dead-letter exchanges.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

INSERT INTO learning_paths (id, organization_id, title, slug, description, category, difficulty, estimated_hours, is_published, created_at, updated_at)
VALUES (
  ('55555555-1111-1111-1111-111111111101', '00000000-0000-0000-0000-000000000001', 'Principal AI & Cloud Solutions Architect', 'principal-ai-cloud-architect', 'Comprehensive career track covering enterprise RAG systems, distributed consensus, and microservice scalability.', 'Engineering Leadership', 'ADVANCED', 60, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
) ON CONFLICT (id) DO NOTHING;

INSERT INTO path_courses (id, learning_path_id, course_id, sequence_order, is_mandatory, created_at, updated_at)
VALUES (
  ('66666666-1111-1111-1111-111111111101', '55555555-1111-1111-1111-111111111101', '11111111-1111-1111-1111-111111111111', 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
) ON CONFLICT (id) DO NOTHING;
""")

write("backend/src/main/resources/db/migration/V8__analytics_and_telemetry_views.sql", """
-- V8: Analytical Aggregation Views for Student, Instructor, and Tenant Dashboards

CREATE OR REPLACE VIEW view_course_completion_stats AS
SELECT 
    c.id AS course_id,
    c.title AS course_title,
    c.organization_id,
    COUNT(e.id) AS total_enrollments,
    COUNT(CASE WHEN e.status = 'COMPLETED' THEN 1 END) AS completed_enrollments,
    AVG(e.completion_percentage) AS avg_completion_percentage,
    MAX(e.last_activity_at) AS latest_student_activity
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
GROUP BY c.id, c.title, c.organization_id;

CREATE OR REPLACE VIEW view_student_mastery_overview AS
SELECT 
    u.id AS user_id,
    u.email AS user_email,
    u.organization_id,
    COUNT(DISTINCT e.course_id) AS enrolled_courses_count,
    COUNT(DISTINCT CASE WHEN e.status = 'COMPLETED' THEN e.course_id END) AS completed_courses_count,
    COALESCE(SUM(lp.seconds_spent), 0) AS total_learning_seconds,
    COUNT(DISTINCT cert.id) AS total_certificates_earned
FROM users u
LEFT JOIN enrollments e ON u.id = e.user_id
LEFT JOIN learning_progress lp ON e.id = lp.enrollment_id
LEFT JOIN certificates cert ON u.id = cert.user_id
GROUP BY u.id, u.email, u.organization_id;

CREATE OR REPLACE VIEW view_assessment_performance_distribution AS
SELECT 
    q.id AS quiz_id,
    q.title AS quiz_title,
    q.course_id,
    COUNT(qa.id) AS total_attempts,
    AVG(qa.score_achieved) AS avg_score,
    COUNT(CASE WHEN qa.is_passed = TRUE THEN 1 END) AS passed_attempts_count,
    AVG(qa.time_spent_seconds) AS avg_time_spent_seconds
FROM quizzes q
LEFT JOIN quiz_attempts qa ON q.id = qa.quiz_id
GROUP BY q.id, q.title, q.course_id;
""")

print("Database seeds and views generated.")
