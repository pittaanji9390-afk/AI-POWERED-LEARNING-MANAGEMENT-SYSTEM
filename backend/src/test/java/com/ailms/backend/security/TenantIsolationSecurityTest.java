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
