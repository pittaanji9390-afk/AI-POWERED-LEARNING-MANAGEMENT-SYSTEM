package com.ailms.backend.modules.course;

import com.ailms.backend.common.exception.BadRequestException;
import com.ailms.backend.modules.audit.repository.AuditLogRepository;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.model.CourseSection;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.course.service.CourseLifecycleService;
import com.ailms.backend.modules.course.service.CourseLifecycleService.CourseState;
import com.ailms.backend.testutil.TestDataFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CourseLifecycleServiceTest {

    @Mock
    private CourseRepository courseRepository;

    @Mock
    private AuditLogRepository auditLogRepository;

    private CourseLifecycleService lifecycleService;

    @BeforeEach
    void setUp() {
        lifecycleService = new CourseLifecycleService(courseRepository, auditLogRepository);
    }

    @Test
    void shouldTransitionDraftToInReviewWhenSectionsExist() {
        UUID courseId = UUID.randomUUID();
        UUID actorId = UUID.randomUUID();

        Course course = TestDataFactory.createCourse("Java Microservices", "java-microservices", actorId, UUID.randomUUID());
        course.setStatus("DRAFT");
        CourseSection section = TestDataFactory.createSection("Introduction", course, 1);
        course.setSections(List.of(section));

        when(courseRepository.findById(courseId)).thenReturn(Optional.of(course));
        when(courseRepository.save(any(Course.class))).thenAnswer(i -> i.getArgument(0));

        Course updated = lifecycleService.transitionState(courseId, CourseState.IN_REVIEW, actorId, "Ready for audit");

        assertEquals("IN_REVIEW", updated.getStatus());
        verify(auditLogRepository, times(1)).save(any());
    }

    @Test
    void shouldRejectTransitionToInReviewIfSectionsAreEmpty() {
        UUID courseId = UUID.randomUUID();
        UUID actorId = UUID.randomUUID();

        Course course = TestDataFactory.createCourse("Empty Course", "empty-course", actorId, UUID.randomUUID());
        course.setStatus("DRAFT");
        course.setSections(List.of()); // No sections

        when(courseRepository.findById(courseId)).thenReturn(Optional.of(course));

        assertThrows(BadRequestException.class, () -> 
            lifecycleService.transitionState(courseId, CourseState.IN_REVIEW, actorId, "Review request")
        );
    }
}
