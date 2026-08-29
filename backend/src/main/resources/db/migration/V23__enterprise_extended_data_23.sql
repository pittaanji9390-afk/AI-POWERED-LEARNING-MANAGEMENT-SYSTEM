-- V23: Enterprise Extended Seed Catalog 23 - Skills, Curricula, and Benchmarks

INSERT INTO skills (id, name, slug, category, description, created_at, updated_at)
VALUES
  (gen_random_uuid(), 'Enterprise Architecture Domain 23A', 'ea-domain-23a', 'Architecture', 'Advanced distributed cloud design patterns and resiliency testing.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (gen_random_uuid(), 'AI RAG Security Specialization 23B', 'rag-sec-23b', 'AI Security', 'Evaluating boundary delimiters and output moderation filters.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

INSERT INTO system_metric_telemetry_11 (metric_name, dimension_tag, numeric_value)
VALUES 
  ('telemetry.batch.23.latency', 'ms', 57.5),
  ('telemetry.batch.23.throughput', 'rps', 1150.0)
ON CONFLICT DO NOTHING;
