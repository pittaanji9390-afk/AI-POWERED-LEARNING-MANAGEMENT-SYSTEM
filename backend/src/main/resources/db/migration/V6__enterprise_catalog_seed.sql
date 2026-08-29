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
