package com.ailms.backend.modules.notification;

import java.util.Map;
import java.util.UUID;

public interface NotificationSender {
    void sendInApp(UUID userId, String title, String body, Map<String, Object> data);
    void sendEmail(String recipientEmail, String subject, String templateName, Map<String, Object> variables);
}
