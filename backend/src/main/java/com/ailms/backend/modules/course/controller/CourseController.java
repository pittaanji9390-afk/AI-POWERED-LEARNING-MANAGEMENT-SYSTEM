package com.ailms.backend.modules.course.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.common.api.PageResponse;
import com.ailms.backend.common.security.CurrentUser;
import com.ailms.backend.common.security.UserPrincipal;
import com.ailms.backend.modules.course.dto.CourseDtos.*;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.service.CourseService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/courses")
@Tag(name = "Courses", description = "Course catalog, creation, and curriculum management")
public class CourseController {

    private final CourseService courseService;

    public CourseController(CourseService courseService) {
        this.courseService = courseService;
    }

    @GetMapping("/catalog")
    @Operation(summary = "Browse published public courses")
    public ResponseEntity<ApiResponse<PageResponse<CourseSummaryDto>>> getCatalog(Pageable pageable) {
        return ResponseEntity.ok(ApiResponse.success(new PageResponse<>(courseService.getPublicCatalog(pageable))));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get course details by ID")
    public ResponseEntity<ApiResponse<Course>> getCourse(@PathVariable UUID id) {
        return ResponseEntity.ok(ApiResponse.success(courseService.getCourseById(id)));
    }

    @PostMapping
    @PreAuthorize("hasAuthority('course:create') or hasRole('TEACHER') or hasRole('SUPER_ADMIN')")
    @Operation(summary = "Create a new course draft")
    public ResponseEntity<ApiResponse<Course>> createCourse(
            @CurrentUser UserPrincipal user,
            @Valid @RequestBody CreateCourseRequest request) {
        Course course = courseService.createCourse(user.getId(), user.getOrganizationId(), request);
        return ResponseEntity.ok(ApiResponse.created(course));
    }
}
