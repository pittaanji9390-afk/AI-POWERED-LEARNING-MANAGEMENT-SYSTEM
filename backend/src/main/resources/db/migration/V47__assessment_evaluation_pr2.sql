-- PR #2: Automated Quiz Evaluation & Question Bank Routing
CREATE INDEX IF NOT EXISTS idx_questions_quiz_active ON questions (quiz_id, is_active);
