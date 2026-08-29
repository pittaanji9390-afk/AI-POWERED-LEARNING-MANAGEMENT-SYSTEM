-- V21: Enterprise Extended Seed Catalog 21 - Skills, Curricula, and Benchmarks

INSERT INTO skills (id, name, slug, category, description, created_at, updated_at)
VALUES
  (gen_random_uuid(), 'Enterprise Architecture Domain 21A', 'ea-domain-21a', 'Architecture', 'Advanced distributed cloud design patterns and resiliency testing.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (gen_random_uuid(), 'AI RAG Security Specialization 21B', 'rag-sec-21b', 'AI Security', 'Evaluating boundary delimiters and output moderation filters.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

INSERT INTO system_metric_telemetry_11 (metric_name, dimension_tag, numeric_value)
VALUES 
  ('telemetry.batch.21.latency', 'ms', 52.5),
  ('telemetry.batch.21.throughput', 'rps', 1050.0)
ON CONFLICT DO NOTHING;
