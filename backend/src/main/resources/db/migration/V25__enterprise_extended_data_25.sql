-- V25: Enterprise Extended Seed Catalog 25 - Skills, Curricula, and Benchmarks

INSERT INTO skills (id, name, slug, category, description, created_at, updated_at)
VALUES
  (gen_random_uuid(), 'Enterprise Architecture Domain 25A', 'ea-domain-25a', 'Architecture', 'Advanced distributed cloud design patterns and resiliency testing.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (gen_random_uuid(), 'AI RAG Security Specialization 25B', 'rag-sec-25b', 'AI Security', 'Evaluating boundary delimiters and output moderation filters.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

INSERT INTO system_metric_telemetry_11 (metric_name, dimension_tag, numeric_value)
VALUES 
  ('telemetry.batch.25.latency', 'ms', 62.5),
  ('telemetry.batch.25.throughput', 'rps', 1250.0)
ON CONFLICT DO NOTHING;
