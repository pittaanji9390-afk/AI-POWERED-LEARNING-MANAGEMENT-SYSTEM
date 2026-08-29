package com.ailms.backend.modules.course.service;

import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.course.dto.CourseDtos.*;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
public class CourseService {

    private final CourseRepository courseRepository;

    public CourseService(CourseRepository courseRepository) {
        this.courseRepository = courseRepository;
    }

    @Transactional(readOnly = true)
    public Page<CourseSummaryDto> getPublicCatalog(Pageable pageable) {
        return courseRepository.findByStatusAndIsPublicTrue("PUBLISHED", pageable)
                .map(c -> new CourseSummaryDto(
                        c.getId(), c.getTitle(), c.getSlug(), c.getShortDescription(),
                        c.getCategory(), c.getDifficulty(), c.getPrice(), c.getCurrency(),
                        c.getStatus(), c.getInstructorId()));
    }

    @Transactional(readOnly = true)
    public Course getCourseById(UUID id) {
        return courseRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Course", "id", id));
    }

    @Transactional
    public Course createCourse(UUID instructorId, UUID orgId, CreateCourseRequest req) {
        Course course = new Course();
        course.setInstructorId(instructorId);
        course.setOrganizationId(orgId);
        course.setTitle(req.title());
        course.setSlug(req.slug());
        course.setShortDescription(req.shortDescription());
        course.setDescription(req.description());
        course.setThumbnailUrl(req.thumbnailUrl());
        course.setCategory(req.category());
        course.setDifficulty(req.difficulty() != null ? req.difficulty() : "BEGINNER");
        course.setPrice(req.price());
        course.setCurrency(req.currency() != null ? req.currency() : "USD");
        course.setIsPublic(req.isPublic() != null ? req.isPublic() : true);
        course.setStatus("DRAFT");

        return courseRepository.save(course);
    }
}
