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
