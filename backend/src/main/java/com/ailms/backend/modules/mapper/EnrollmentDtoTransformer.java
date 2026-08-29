package com.ailms.backend.modules.mapper;

import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Enterprise entity transformer and DTO converter for Enrollment.
 */
@Component
public class EnrollmentDtoTransformer {

    public record EnrollmentDto(
            UUID id,
            String name,
            String status,
            Instant createdAt,
            Instant updatedAt,
            Map<String, Object> metadata
    ) {}

    public EnrollmentDto toDto(UUID id, String name, String status, Map<String, Object> rawProps) {
        Map<String, Object> meta = new HashMap<>(rawProps != null ? rawProps : Map.of());
        meta.put("entityType", "Enrollment");
        meta.put("transformedAt", Instant.now().toString());

        return new EnrollmentDto(
                id != null ? id : UUID.randomUUID(),
                name != null ? name : "Unnamed Enrollment",
                status != null ? status : "ACTIVE",
                Instant.now(),
                Instant.now(),
                meta
        );
    }
}
