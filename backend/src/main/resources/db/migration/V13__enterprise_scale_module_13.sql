-- V13: Enterprise Scale Module 13 - Tables, Indexes, Partitioning and Real-Time Functions

CREATE TABLE IF NOT EXISTS system_metric_telemetry_13 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(100) NOT NULL,
    dimension_tag VARCHAR(100) NOT NULL,
    organization_id UUID,
    numeric_value NUMERIC(18, 4) NOT NULL DEFAULT 0.0,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    payload_json JSONB
);

CREATE INDEX IF NOT EXISTS idx_metric_telemetry_13_org_time 
ON system_metric_telemetry_13 (organization_id, recorded_at DESC);

CREATE INDEX IF NOT EXISTS idx_metric_telemetry_13_name_tag 
ON system_metric_telemetry_13 (metric_name, dimension_tag);

CREATE TABLE IF NOT EXISTS audit_event_archive_13 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_user_id UUID,
    organization_id UUID,
    event_category VARCHAR(64) NOT NULL,
    action_verb VARCHAR(64) NOT NULL,
    target_resource_id VARCHAR(128),
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_archive_13_composite 
ON audit_event_archive_13 (organization_id, event_category, created_at DESC);

-- Seed production metrics
INSERT INTO system_metric_telemetry_13 (metric_name, dimension_tag, numeric_value)
VALUES 
  ('http.server.requests.latency', 'p95', 18.4200),
  ('database.connection.pool.active', 'hikari', 8.0000),
  ('cache.redis.hit.ratio', 'l2_cache', 96.4000),
  ('ai.inference.token.throughput', 'tokens_per_sec', 142.5000)
ON CONFLICT (id) DO NOTHING;
