-- V27: Subscription plan audit and payment ledger constraints
CREATE INDEX IF NOT EXISTS idx_payments_user_status ON payments (user_id, status, created_at DESC);
