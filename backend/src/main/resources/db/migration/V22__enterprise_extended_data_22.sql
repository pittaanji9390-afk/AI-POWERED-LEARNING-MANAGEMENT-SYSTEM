-- V22: Enterprise Extended Seed Catalog 22 - Skills, Curricula, and Benchmarks

INSERT INTO skills (id, name, slug, category, description, created_at, updated_at)
VALUES
  (gen_random_uuid(), 'Enterprise Architecture Domain 22A', 'ea-domain-22a', 'Architecture', 'Advanced distributed cloud design patterns and resiliency testing.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (gen_random_uuid(), 'AI RAG Security Specialization 22B', 'rag-sec-22b', 'AI Security', 'Evaluating boundary delimiters and output moderation filters.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

INSERT INTO system_metric_telemetry_11 (metric_name, dimension_tag, numeric_value)
VALUES 
  ('telemetry.batch.22.latency', 'ms', 55.0),
  ('telemetry.batch.22.throughput', 'rps', 1100.0)
ON CONFLICT DO NOTHING;
