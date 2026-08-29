-- V24: Enterprise Extended Seed Catalog 24 - Skills, Curricula, and Benchmarks

INSERT INTO skills (id, name, slug, category, description, created_at, updated_at)
VALUES
  (gen_random_uuid(), 'Enterprise Architecture Domain 24A', 'ea-domain-24a', 'Architecture', 'Advanced distributed cloud design patterns and resiliency testing.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (gen_random_uuid(), 'AI RAG Security Specialization 24B', 'rag-sec-24b', 'AI Security', 'Evaluating boundary delimiters and output moderation filters.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

INSERT INTO system_metric_telemetry_11 (metric_name, dimension_tag, numeric_value)
VALUES 
  ('telemetry.batch.24.latency', 'ms', 60.0),
  ('telemetry.batch.24.throughput', 'rps', 1200.0)
ON CONFLICT DO NOTHING;
