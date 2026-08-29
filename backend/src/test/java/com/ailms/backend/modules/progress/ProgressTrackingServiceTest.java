package com.ailms.backend.modules.progress;

import com.ailms.backend.common.event.DomainEventPublisher;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.model.CourseSection;
import com.ailms.backend.modules.course.model.Lesson;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.course.repository.LessonRepository;
import com.ailms.backend.modules.enrollment.model.Enrollment;
import com.ailms.backend.modules.enrollment.model.LearningProgress;
import com.ailms.backend.modules.enrollment.repository.EnrollmentRepository;
import com.ailms.backend.modules.enrollment.repository.LearningProgressRepository;
import com.ailms.backend.modules.progress.service.ProgressTrackingService;
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
class ProgressTrackingServiceTest {

    @Mock private EnrollmentRepository enrollmentRepository;
    @Mock private LearningProgressRepository progressRepository;
    @Mock private LessonRepository lessonRepository;
    @Mock private CourseRepository courseRepository;
    @Mock private DomainEventPublisher eventPublisher;

    private ProgressTrackingService progressService;

    @BeforeEach
    void setUp() {
        progressService = new ProgressTrackingService(
                enrollmentRepository, progressRepository, lessonRepository, courseRepository, eventPublisher
        );
    }

    @Test
    void shouldRecordProgressAndCompleteLessonAt90Percent() {
        UUID enrollmentId = UUID.randomUUID();
        UUID lessonId = UUID.randomUUID();

        Course course = TestDataFactory.createCourse("K8s Fundamentals", "k8s-fund", UUID.randomUUID(), UUID.randomUUID());
        CourseSection sec = TestDataFactory.createSection("Core Pods", course, 1);
        Lesson lesson = TestDataFactory.createLesson("Pod Lifecycle", sec, "VIDEO", 600); // 10 mins

        Enrollment enrollment = new Enrollment();
        enrollment.setId(enrollmentId);
        enrollment.setCourse(course);
        enrollment.setUser(TestDataFactory.createUser("alex@ailms.com", "Alex", "Student", null, "STUDENT"));

        when(enrollmentRepository.findById(enrollmentId)).thenReturn(Optional.of(enrollment));
        when(lessonRepository.findById(lessonId)).thenReturn(Optional.of(lesson));
        when(progressRepository.findByEnrollmentIdAndLessonId(enrollmentId, lessonId)).thenReturn(Optional.empty());
        when(progressRepository.save(any(LearningProgress.class))).thenAnswer(i -> i.getArgument(0));

        // Heartbeat at 550s (91.6% completed)
        LearningProgress result = progressService.recordLessonHeartbeat(enrollmentId, lessonId, 30, 550);

        assertEquals("COMPLETED", result.getStatus());
        assertTrue(result.getProgressPercent() >= 90);
        verify(eventPublisher, times(1)).publish(any());
    }
}
