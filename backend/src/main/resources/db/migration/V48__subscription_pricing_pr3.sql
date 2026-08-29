-- PR #3: Stripe Checkout Integration & Coupon Engine
CREATE INDEX IF NOT EXISTS idx_payments_org_time ON payments (created_at DESC);
