-- V9: Enterprise Question Bank, Assessment Modules, and Question Rubrics

INSERT INTO quizzes (id, course_id, lesson_id, title, description, passing_score, time_limit_minutes, max_attempts, is_active, created_at, updated_at)
VALUES
  ('77777777-1111-1111-1111-111111111101', '11111111-1111-1111-1111-111111111111', '33333333-1111-1111-1111-111111111101', 'Distributed Consensus & Raft Architecture Assessment', 'Evaluates understanding of Raft leader election, split votes, and log compaction.', 80, 20, 3, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('77777777-1111-1111-1111-111111111102', '11111111-1111-1111-1111-111111111111', '33333333-1111-1111-1111-111111111103', 'pgvector & High-Dimensional HNSW Vector Indexing Exam', 'Evaluates cosine distance metric properties, HNSW graph parameters, and RAG retrieval latency.', 75, 15, 3, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Seed Questions for Quiz 1
INSERT INTO questions (id, quiz_id, question_text, question_type, points, difficulty, explanation, sequence_order, is_active, created_at, updated_at)
VALUES
  ('88888888-1111-1111-1111-111111111101', '77777777-1111-1111-1111-111111111101', 'In the Raft consensus protocol, what mechanism prevents two candidates from simultaneously splitting votes indefinitely?', 'MULTIPLE_CHOICE', 10, 'HARD', 'Randomized election timeouts ensure one node times out first and requests votes before competitors.', 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('88888888-1111-1111-1111-111111111102', '77777777-1111-1111-1111-111111111101', 'Under what condition does a Raft leader consider a log entry committed and safe to apply to its state machine?', 'MULTIPLE_CHOICE', 10, 'HARD', 'Once replicated across a strict majority (quorum) of active cluster nodes.', 2, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('88888888-1111-1111-1111-111111111103', '77777777-1111-1111-1111-111111111102', 'Which index type in pgvector requires rebuilding after substantial dataset insertions to maintain high recall?', 'MULTIPLE_CHOICE', 10, 'MEDIUM', 'IVFFlat relies on static centroid clusters, whereas HNSW continuously updates its hierarchical graph.', 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Seed Options for Question 1
INSERT INTO question_options (id, question_id, option_text, is_correct, sequence_order, created_at, updated_at)
VALUES
  ('99999999-1111-1111-1111-111111111101', '88888888-1111-1111-1111-111111111101', 'Randomized election timeouts between 150ms and 300ms', TRUE, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('99999999-1111-1111-1111-111111111102', '88888888-1111-1111-1111-111111111101', 'Fixed round-robin node priority rankings', FALSE, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('99999999-1111-1111-1111-111111111103', '88888888-1111-1111-1111-111111111101', 'Centralized NTP wall-clock timestamp comparisons', FALSE, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('99999999-1111-1111-1111-111111111104', '88888888-1111-1111-1111-111111111101', 'Synchronous two-phase commit lock acquisitions', FALSE, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;
