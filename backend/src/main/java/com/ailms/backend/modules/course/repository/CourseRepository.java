package com.ailms.backend.modules.course.repository;

import com.ailms.backend.modules.course.model.Course;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CourseRepository extends JpaRepository<Course, UUID> {
    Optional<Course> findBySlug(String slug);
    Page<Course> findByStatusAndIsPublicTrue(String status, Pageable pageable);
    Page<Course> findByOrganizationId(UUID organizationId, Pageable pageable);
}
