package com.ailms.backend.modules.mapper;

import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Enterprise entity transformer and DTO converter for LearningProgress.
 */
@Component
public class LearningProgressDtoTransformer {

    public record LearningProgressDto(
            UUID id,
            String name,
            String status,
            Instant createdAt,
            Instant updatedAt,
            Map<String, Object> metadata
    ) {}

    public LearningProgressDto toDto(UUID id, String name, String status, Map<String, Object> rawProps) {
        Map<String, Object> meta = new HashMap<>(rawProps != null ? rawProps : Map.of());
        meta.put("entityType", "LearningProgress");
        meta.put("transformedAt", Instant.now().toString());

        return new LearningProgressDto(
                id != null ? id : UUID.randomUUID(),
                name != null ? name : "Unnamed LearningProgress",
                status != null ? status : "ACTIVE",
                Instant.now(),
                Instant.now(),
                meta
        );
    }
}
