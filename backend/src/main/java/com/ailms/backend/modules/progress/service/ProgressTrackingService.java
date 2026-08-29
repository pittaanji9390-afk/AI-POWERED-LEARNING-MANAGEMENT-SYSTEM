package com.ailms.backend.modules.progress.service;

import com.ailms.backend.common.event.DomainEventPublisher;
import com.ailms.backend.common.event.LearningEvent;
import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.model.Lesson;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.course.repository.LessonRepository;
import com.ailms.backend.modules.enrollment.model.Enrollment;
import com.ailms.backend.modules.enrollment.model.LearningProgress;
import com.ailms.backend.modules.enrollment.repository.EnrollmentRepository;
import com.ailms.backend.modules.enrollment.repository.LearningProgressRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class ProgressTrackingService {

    private final EnrollmentRepository enrollmentRepository;
    private final LearningProgressRepository progressRepository;
    private final LessonRepository lessonRepository;
    private final CourseRepository courseRepository;
    private final DomainEventPublisher eventPublisher;

    public ProgressTrackingService(
            EnrollmentRepository enrollmentRepository,
            LearningProgressRepository progressRepository,
            LessonRepository lessonRepository,
            CourseRepository courseRepository,
            DomainEventPublisher eventPublisher) {
        this.enrollmentRepository = enrollmentRepository;
        this.progressRepository = progressRepository;
        this.lessonRepository = lessonRepository;
        this.courseRepository = courseRepository;
        this.eventPublisher = eventPublisher;
    }

    @Transactional
    public LearningProgress recordLessonHeartbeat(UUID enrollmentId, UUID lessonId, int secondsSpent, int lastPosition) {
        Enrollment enrollment = enrollmentRepository.findById(enrollmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Enrollment", "id", enrollmentId));

        Lesson lesson = lessonRepository.findById(lessonId)
                .orElseThrow(() -> new ResourceNotFoundException("Lesson", "id", lessonId));

        LearningProgress progress = progressRepository.findByEnrollmentIdAndLessonId(enrollmentId, lessonId)
                .orElseGet(() -> {
                    LearningProgress lp = new LearningProgress();
                    lp.setEnrollment(enrollment);
                    lp.setLesson(lesson);
                    return lp;
                });

        progress.setSecondsSpent(progress.getSecondsSpent() + secondsSpent);
        progress.setLastPositionSeconds(lastPosition);

        int lessonDuration = lesson.getDurationSeconds() > 0 ? lesson.getDurationSeconds() : 600;
        int calculatedPercent = Math.min(100, (int) (((double) lastPosition / lessonDuration) * 100));
        progress.setProgressPercent(Math.max(progress.getProgressPercent(), calculatedPercent));

        if (progress.getProgressPercent() >= 90 && !"COMPLETED".equals(progress.getStatus())) {
            progress.setStatus("COMPLETED");
            progress.setCompletedAt(Instant.now());

            eventPublisher.publish(new LearningEvent(
                    "LESSON_COMPLETED", enrollment.getUser().getId(), enrollment.getCourse().getId(), lessonId, enrollment.getOrganizationId(),
                    Map.of("progress", 100, "durationSeconds", progress.getSecondsSpent())
            ));
        }

        enrollment.setLastActivityAt(Instant.now());
        recalculateCourseProgress(enrollment);

        return progressRepository.save(progress);
    }

    private void recalculateCourseProgress(Enrollment enrollment) {
        Course course = courseRepository.findById(enrollment.getCourse().getId()).orElse(null);
        if (course == null) return;

        int totalLessons = course.getSections().stream().mapToInt(s -> s.getLessons().size()).sum();
        if (totalLessons == 0) return;

        List<LearningProgress> completedList = progressRepository.findByEnrollmentIdAndStatus(enrollment.getId(), "COMPLETED");
        int completionPercent = (int) (((double) completedList.size() / totalLessons) * 100);
        enrollment.setCompletionPercentage(completionPercent);

        if (completionPercent >= 100 && !"COMPLETED".equals(enrollment.getStatus())) {
            enrollment.setStatus("COMPLETED");
            enrollment.setCompletedAt(Instant.now());

            eventPublisher.publish(new LearningEvent(
                    "COURSE_COMPLETED", enrollment.getUser().getId(), enrollment.getCourse().getId(), null, enrollment.getOrganizationId(),
                    Map.of("totalLessons", totalLessons)
            ));
        }
        enrollmentRepository.save(enrollment);
    }
}
