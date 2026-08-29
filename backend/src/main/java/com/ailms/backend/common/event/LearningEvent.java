package com.ailms.backend.common.event;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;

public class LearningEvent implements DomainEvent {
    private final UUID eventId;
    private final Instant occurredAt;
    private final String eventType;
    private final UUID studentId;
    private final UUID courseId;
    private final UUID lessonId;
    private final UUID tenantId;
    private final Map<String, Object> payload;

    public LearningEvent(String eventType, UUID studentId, UUID courseId, UUID lessonId, UUID tenantId, Map<String, Object> payload) {
        this.eventId = UUID.randomUUID();
        this.occurredAt = Instant.now();
        this.eventType = eventType;
        this.studentId = studentId;
        this.courseId = courseId;
        this.lessonId = lessonId;
        this.tenantId = tenantId;
        this.payload = payload != null ? payload : Map.of();
    }

    @Override public UUID getEventId() { return eventId; }
    @Override public Instant getOccurredAt() { return occurredAt; }
    @Override public String getEventType() { return eventType; }
    @Override public UUID getTenantId() { return tenantId; }
    public UUID getStudentId() { return studentId; }
    public UUID getCourseId() { return courseId; }
    public UUID getLessonId() { return lessonId; }
    public Map<String, Object> getPayload() { return payload; }
}
