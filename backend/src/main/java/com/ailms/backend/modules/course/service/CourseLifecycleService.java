package com.ailms.backend.modules.course.service;

import com.ailms.backend.common.exception.BadRequestException;
import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.audit.model.AuditLog;
import com.ailms.backend.modules.audit.repository.AuditLogRepository;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Set;
import java.util.UUID;

@Service
public class CourseLifecycleService {

    private final CourseRepository courseRepository;
    private final AuditLogRepository auditLogRepository;

    public CourseLifecycleService(CourseRepository courseRepository, AuditLogRepository auditLogRepository) {
        this.courseRepository = courseRepository;
        this.auditLogRepository = auditLogRepository;
    }

    public enum CourseState {
        DRAFT, IN_REVIEW, PUBLISHED, UNPUBLISHED, ARCHIVED
    }

    @Transactional
    public Course transitionState(UUID courseId, CourseState targetState, UUID actorId, String reason) {
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new ResourceNotFoundException("Course", "id", courseId));

        CourseState currentState = CourseState.valueOf(course.getStatus());
        validateTransition(currentState, targetState, course);

        course.setStatus(targetState.name());
        Course updated = courseRepository.save(course);

        AuditLog log = new AuditLog();
        log.setActorId(actorId);
        log.setAction("COURSE_STATE_TRANSITION");
        log.setEntityType("Course");
        log.setEntityId(courseId.toString());
        log.setOrganizationId(course.getOrganizationId());
        auditLogRepository.save(log);

        return updated;
    }

    private void validateTransition(CourseState current, CourseState target, Course course) {
        switch (current) {
            case DRAFT -> {
                if (target != CourseState.IN_REVIEW && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("Draft course can only transition to IN_REVIEW or ARCHIVED.");
                }
                if (target == CourseState.IN_REVIEW && course.getSections().isEmpty()) {
                    throw new BadRequestException("Course must contain at least one section before submitting for review.");
                }
            }
            case IN_REVIEW -> {
                if (target != CourseState.PUBLISHED && target != CourseState.DRAFT && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("In-review course can only be PUBLISHED, returned to DRAFT, or ARCHIVED.");
                }
            }
            case PUBLISHED -> {
                if (target != CourseState.UNPUBLISHED && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("Published course can only be UNPUBLISHED or ARCHIVED.");
                }
            }
            case UNPUBLISHED -> {
                if (target != CourseState.PUBLISHED && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("Unpublished course can only be republished or ARCHIVED.");
                }
            }
            case ARCHIVED -> throw new BadRequestException("Archived courses cannot transition to any active state.");
        }
    }
}
