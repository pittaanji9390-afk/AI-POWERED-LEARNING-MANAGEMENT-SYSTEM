package com.ailms.backend.modules.course.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.model.CourseSection;
import com.ailms.backend.modules.course.model.Lesson;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.course.repository.CourseSectionRepository;
import com.ailms.backend.modules.course.repository.LessonRepository;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/courses/{courseId}/sections")
@Tag(name = "Course Curriculum", description = "Sections and lessons curriculum management")
public class CourseSectionController {

    private final CourseRepository courseRepository;
    private final CourseSectionRepository sectionRepository;
    private final LessonRepository lessonRepository;

    public CourseSectionController(CourseRepository courseRepository, CourseSectionRepository sectionRepository, LessonRepository lessonRepository) {
        this.courseRepository = courseRepository;
        this.sectionRepository = sectionRepository;
        this.lessonRepository = lessonRepository;
    }

    public record CreateSectionRequest(@NotBlank String title, String description, Integer sequenceOrder) {}
    public record CreateLessonRequest(@NotBlank String title, @NotBlank String lessonType, Integer durationSeconds, String contentBody, String videoUrl) {}

    @PostMapping
    @PreAuthorize("hasRole('TEACHER') or hasRole('SUPER_ADMIN')")
    @Operation(summary = "Add section to course curriculum")
    public ResponseEntity<ApiResponse<CourseSection>> addSection(
            @PathVariable UUID courseId,
            @Valid @RequestBody CreateSectionRequest req) {
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new ResourceNotFoundException("Course", "id", courseId));

        CourseSection section = new CourseSection();
        section.setCourse(course);
        section.setTitle(req.title());
        section.setSequenceOrder(req.sequenceOrder() != null ? req.sequenceOrder() : 1);

        return ResponseEntity.ok(ApiResponse.created(sectionRepository.save(section)));
    }

    @PostMapping("/{sectionId}/lessons")
    @PreAuthorize("hasRole('TEACHER') or hasRole('SUPER_ADMIN')")
    @Operation(summary = "Add lesson to curriculum section")
    public ResponseEntity<ApiResponse<Lesson>> addLesson(
            @PathVariable UUID courseId,
            @PathVariable UUID sectionId,
            @Valid @RequestBody CreateLessonRequest req) {
        CourseSection section = sectionRepository.findById(sectionId)
                .orElseThrow(() -> new ResourceNotFoundException("CourseSection", "id", sectionId));

        Lesson lesson = new Lesson();
        lesson.setSection(section);
        lesson.setTitle(req.title());
        lesson.setLessonType(req.lessonType());
        lesson.setDurationSeconds(req.durationSeconds() != null ? req.durationSeconds() : 600);
        lesson.setContentBody(req.contentBody());
        lesson.setVideoUrl(req.videoUrl());
        lesson.setSequenceOrder(section.getLessons().size() + 1);

        return ResponseEntity.ok(ApiResponse.created(lessonRepository.save(lesson)));
    }
}
