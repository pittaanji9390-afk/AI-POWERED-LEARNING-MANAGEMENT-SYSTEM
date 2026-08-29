package com.ailms.backend.modules.mapper;

import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Enterprise entity transformer and DTO converter for Discussion.
 */
@Component
public class DiscussionDtoTransformer {

    public record DiscussionDto(
            UUID id,
            String name,
            String status,
            Instant createdAt,
            Instant updatedAt,
            Map<String, Object> metadata
    ) {}

    public DiscussionDto toDto(UUID id, String name, String status, Map<String, Object> rawProps) {
        Map<String, Object> meta = new HashMap<>(rawProps != null ? rawProps : Map.of());
        meta.put("entityType", "Discussion");
        meta.put("transformedAt", Instant.now().toString());

        return new DiscussionDto(
                id != null ? id : UUID.randomUUID(),
                name != null ? name : "Unnamed Discussion",
                status != null ? status : "ACTIVE",
                Instant.now(),
                Instant.now(),
                meta
        );
    }
}
