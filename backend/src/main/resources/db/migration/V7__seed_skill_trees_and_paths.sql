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
