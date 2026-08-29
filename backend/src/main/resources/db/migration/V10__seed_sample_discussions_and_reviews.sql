-- V10: Sample Discussions, Community Comments, and Verified Course Reviews

INSERT INTO discussions (id, course_id, author_id, organization_id, title, content, upvotes_count, status, created_at, updated_at)
VALUES
  ('aaaaaaaa-1111-1111-1111-111111111101', '11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000001', 'Best practices for HNSW parameter tuning in high-throughput PostgreSQL workloads', 'When tuning m=16 and ef_construction=64 vs m=32 and ef_construction=128, what memory overhead should we budget per 100k 1536-dimensional vectors?', 18, 'VISIBLE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('aaaaaaaa-1111-1111-1111-111111111102', '11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000001', 'Handling distributed compensations when an external Stripe payment webhook times out', 'If the inventory reservation service succeeds but the payment confirmation webhook fails after retries, how should the compensating saga execute?', 24, 'VISIBLE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;
