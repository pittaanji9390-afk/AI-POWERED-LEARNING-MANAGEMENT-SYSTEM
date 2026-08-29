package com.ailms.backend.modules.enrollment.repository;

import com.ailms.backend.modules.enrollment.model.LearningProgress;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface LearningProgressRepository extends JpaRepository<LearningProgress, UUID> {
    Optional<LearningProgress> findByEnrollmentIdAndLessonId(UUID enrollmentId, UUID lessonId);
    List<LearningProgress> findByEnrollmentId(UUID enrollmentId);
    List<LearningProgress> findByEnrollmentIdAndStatus(UUID enrollmentId, String status);
}
