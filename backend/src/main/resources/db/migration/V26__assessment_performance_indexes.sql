-- V26: High performance assessment attempt indexing
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_quiz ON quiz_attempts (user_id, quiz_id, score_achieved DESC);
