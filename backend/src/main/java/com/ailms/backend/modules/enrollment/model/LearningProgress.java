package com.ailms.backend.modules.enrollment.model;

import com.ailms.backend.common.domain.AuditableEntity;
import com.ailms.backend.modules.course.model.Lesson;
import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "learning_progress", uniqueConstraints = @UniqueConstraint(columnNames = {"enrollment_id", "lesson_id"}))
public class LearningProgress extends AuditableEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "enrollment_id", nullable = false)
    private Enrollment enrollment;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "lesson_id", nullable = false)
    private Lesson lesson;

    @Column(name = "status")
    private String status = "IN_PROGRESS";

    @Column(name = "progress_percent")
    private Integer progressPercent = 0;

    @Column(name = "seconds_spent")
    private Integer secondsSpent = 0;

    @Column(name = "last_position_seconds")
    private Integer lastPositionSeconds = 0;

    @Column(name = "completed_at")
    private Instant completedAt;

    public Enrollment getEnrollment() { return enrollment; }
    public void setEnrollment(Enrollment enrollment) { this.enrollment = enrollment; }
    public Lesson getLesson() { return lesson; }
    public void setLesson(Lesson lesson) { this.lesson = lesson; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public Integer getProgressPercent() { return progressPercent; }
    public void setProgressPercent(Integer progressPercent) { this.progressPercent = progressPercent; }
    public Integer getSecondsSpent() { return secondsSpent; }
    public void setSecondsSpent(Integer secondsSpent) { this.secondsSpent = secondsSpent; }
    public Integer getLastPositionSeconds() { return lastPositionSeconds; }
    public void setLastPositionSeconds(Integer lastPositionSeconds) { this.lastPositionSeconds = lastPositionSeconds; }
    public Instant getCompletedAt() { return completedAt; }
    public void setCompletedAt(Instant completedAt) { this.completedAt = completedAt; }
}
