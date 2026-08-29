package com.ailms.backend.modules.notification.service;

import com.ailms.backend.modules.notification.model.Notification;
import com.ailms.backend.modules.notification.repository.NotificationRepository;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.UUID;

@Service
public class NotificationDispatcherService {

    private final NotificationRepository notificationRepository;

    public NotificationDispatcherService(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    @Async("eventTaskExecutor")
    public void dispatch(UUID userId, String title, String body, String type, String linkUrl) {
        Notification n = new Notification();
        n.setTitle(title);
        n.setBody(body);
        n.setNotificationType(type);
        n.setLinkUrl(linkUrl);
        n.setIsRead(false);
        n.setCreatedAt(Instant.now());
        notificationRepository.save(n);
    }
}
