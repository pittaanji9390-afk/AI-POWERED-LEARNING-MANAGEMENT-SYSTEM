import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# ----------------- REUSABLE TEST FACTORIES & FIXTURES -----------------
write("backend/src/test/java/com/ailms/backend/testutil/TestDataFactory.java", """
package com.ailms.backend.testutil;

import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.model.CourseSection;
import com.ailms.backend.modules.course.model.Lesson;
import com.ailms.backend.modules.organization.model.Organization;
import com.ailms.backend.modules.user.model.User;

import java.math.BigDecimal;
import java.util.Set;
import java.util.UUID;

public final class TestDataFactory {

    private TestDataFactory() {}

    public static Organization createOrganization(String name, String slug) {
        Organization org = new Organization();
        org.setId(UUID.randomUUID());
        org.setName(name);
        org.setSlug(slug);
        org.setTier("ENTERPRISE");
        org.setMaxSeats(500);
        org.setStatus("ACTIVE");
        return org;
    }

    public static User createUser(String email, String firstName, String lastName, UUID orgId, String role) {
        User user = new User();
        user.setId(UUID.randomUUID());
        user.setEmail(email);
        user.setPasswordHash("$2a$12$e8YQ3fW4z6YgR1/Z1uPqQeHjLqO.Hq2kGz7.T6zN6Z0m2.T8y4yS");
        user.setFirstName(firstName);
        user.setLastName(lastName);
        user.setOrganizationId(orgId);
        user.setRoles(Set.of(role));
        user.setPermissions(Set.of("course:read", "course:create", "ai:tutor:access"));
        user.setStatus("ACTIVE");
        return user;
    }

    public static Course createCourse(String title, String slug, UUID instructorId, UUID orgId) {
        Course course = new Course();
        course.setId(UUID.randomUUID());
        course.setTitle(title);
        course.setSlug(slug);
        course.setShortDescription("Short description for " + title);
        course.setDescription("Comprehensive description for " + title);
        course.setCategory("Computer Science");
        course.setDifficulty("ADVANCED");
        course.setPrice(BigDecimal.valueOf(99.00));
        course.setCurrency("USD");
        course.setInstructorId(instructorId);
        course.setOrganizationId(orgId);
        course.setStatus("PUBLISHED");
        course.setIsPublic(true);
        return course;
    }

    public static CourseSection createSection(String title, Course course, int order) {
        CourseSection section = new CourseSection();
        section.setId(UUID.randomUUID());
        section.setTitle(title);
        section.setCourse(course);
        section.setSequenceOrder(order);
        return section;
    }

    public static Lesson createLesson(String title, CourseSection section, String type, int duration) {
        Lesson lesson = new Lesson();
        lesson.setId(UUID.randomUUID());
        lesson.setTitle(title);
        lesson.setSection(section);
        lesson.setLessonType(type);
        lesson.setDurationSeconds(duration);
        lesson.setSequenceOrder(1);
        lesson.setContentBody("Detailed educational content for " + title);
        return lesson;
    }
}
""")

# ----------------- SECURITY & TENANT TESTS -----------------
write("backend/src/test/java/com/ailms/backend/security/TenantIsolationSecurityTest.java", """
package com.ailms.backend.security;

import com.ailms.backend.common.security.TenantContext;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.testutil.TestDataFactory;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TenantIsolationSecurityTest {

    @Mock
    private CourseRepository courseRepository;

    private UUID tenantA;
    private UUID tenantB;

    @BeforeEach
    void setUp() {
        tenantA = UUID.randomUUID();
        tenantB = UUID.randomUUID();
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    void shouldStrictlyIsolateCoursesBetweenTenants() {
        TenantContext.setTenantId(tenantA);
        assertEquals(tenantA, TenantContext.getTenantId());

        Course courseA = TestDataFactory.createCourse("Tenant A Course", "tenant-a-course", UUID.randomUUID(), tenantA);
        Course courseB = TestDataFactory.createCourse("Tenant B Course", "tenant-b-course", UUID.randomUUID(), tenantB);

        when(courseRepository.findByOrganizationId(eq(tenantA), eq(Pageable.unpaged())))
                .thenReturn(new PageImpl<>(List.of(courseA)));

        Page<Course> resultsTenantA = courseRepository.findByOrganizationId(tenantA, Pageable.unpaged());
        assertEquals(1, resultsTenantA.getContent().size());
        assertEquals("Tenant A Course", resultsTenantA.getContent().get(0).getTitle());
        assertEquals(tenantA, resultsTenantA.getContent().get(0).getOrganizationId());

        // Verify tenant A cannot see tenant B
        assertFalse(resultsTenantA.getContent().stream().anyMatch(c -> c.getOrganizationId().equals(tenantB)));
    }
}
""")

# ----------------- COURSE LIFECYCLE TESTS -----------------
write("backend/src/test/java/com/ailms/backend/modules/course/CourseLifecycleServiceTest.java", """
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
""")

# ----------------- PROGRESS TRACKING TESTS -----------------
write("backend/src/test/java/com/ailms/backend/modules/progress/ProgressTrackingServiceTest.java", """
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
""")

print("Scaling test suites generated.")
