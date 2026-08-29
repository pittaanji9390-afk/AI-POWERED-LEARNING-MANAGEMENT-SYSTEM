-- V34: Enterprise Subsystem Partition Table & Indices 34

CREATE TABLE IF NOT EXISTS enterprise_subsystem_event_log_34 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID,
    user_id UUID,
    event_name VARCHAR(128) NOT NULL,
    subsystem_code VARCHAR(64) NOT NULL,
    severity_level VARCHAR(32) DEFAULT 'INFO',
    payload_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_subsystem_event_log_34_composite 
ON enterprise_subsystem_event_log_34 (organization_id, subsystem_code, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_subsystem_event_log_34_user 
ON enterprise_subsystem_event_log_34 (user_id, created_at DESC);

INSERT INTO enterprise_subsystem_event_log_34 (event_name, subsystem_code, severity_level, payload_data)
VALUES 
  ('SYSTEM_INITIALIZATION', 'CORE_FRAMEWORK_34', 'INFO', '{"status": "INITIALIZED", "variant": 34}'),
  ('HEALTH_CHECK_PROBE', 'TELEMETRY_34', 'INFO', '{"status": "UP", "latencyMs": 1.45}')
ON CONFLICT (id) DO NOTHING;
