-- V28: Fast DAG traversal indexes for skill prerequisites
CREATE INDEX IF NOT EXISTS idx_path_courses_composite ON path_courses (learning_path_id, sequence_order ASC);
