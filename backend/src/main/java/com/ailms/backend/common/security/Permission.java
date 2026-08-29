package com.ailms.backend.common.security;

public enum Permission {
    COURSE_CREATE("course:create"),
    COURSE_READ("course:read"),
    COURSE_UPDATE("course:update"),
    COURSE_DELETE("course:delete"),
    COURSE_PUBLISH("course:publish"),
    CONTENT_MANAGE("content:manage"),
    MEDIA_UPLOAD("media:upload"),
    ENROLLMENT_MANAGE("enrollment:manage"),
    PROGRESS_VIEW_ALL("progress:view:all"),
    ASSESSMENT_CREATE("assessment:create"),
    ASSESSMENT_GRADE("assessment:grade"),
    GRADE_OVERRIDE("grade:override"),
    AI_TUTOR_ACCESS("ai:tutor:access"),
    AI_GENERATE_QUIZ("ai:quiz:generate"),
    AI_GENERATE_CONTENT("ai:content:generate"),
    AI_ASSISTED_GRADING("ai:grading:assist"),
    USER_MANAGE("user:manage"),
    ORGANIZATION_MANAGE("organization:manage"),
    MODERATION_MANAGE("moderation:manage"),
    PAYMENT_MANAGE("payment:manage"),
    AUDIT_VIEW("audit:view"),
    SYSTEM_CONFIG("system:config");

    private final String value;
    Permission(String value) { this.value = value; }
    public String getValue() { return value; }
}
