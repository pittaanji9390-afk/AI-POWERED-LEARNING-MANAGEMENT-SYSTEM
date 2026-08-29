package com.ailms.backend.modules.mapper;

import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Enterprise entity transformer and DTO converter for Notification.
 */
@Component
public class NotificationDtoTransformer {

    public record NotificationDto(
            UUID id,
            String name,
            String status,
            Instant createdAt,
            Instant updatedAt,
            Map<String, Object> metadata
    ) {}

    public NotificationDto toDto(UUID id, String name, String status, Map<String, Object> rawProps) {
        Map<String, Object> meta = new HashMap<>(rawProps != null ? rawProps : Map.of());
        meta.put("entityType", "Notification");
        meta.put("transformedAt", Instant.now().toString());

        return new NotificationDto(
                id != null ? id : UUID.randomUUID(),
                name != null ? name : "Unnamed Notification",
                status != null ? status : "ACTIVE",
                Instant.now(),
                Instant.now(),
                meta
        );
    }
}
