-- PR #5: Real-Time Notification Drawer & Alert Routing
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications (notification_type, is_read);
