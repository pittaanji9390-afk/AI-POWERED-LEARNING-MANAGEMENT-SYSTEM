package com.ailms.backend.modules.assessment.model;

import com.ailms.backend.common.domain.AuditableEntity;
import com.ailms.backend.modules.user.model.User;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "assignment_submissions")
public class AssignmentSubmission extends AuditableEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "assignment_id", nullable = false)
    private Assignment assignment;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "student_id", nullable = false)
    private User student;

    @Column(name = "submission_text", columnDefinition = "TEXT")
    private String submissionText;

    @Column(name = "file_url")
    private String fileUrl;

    @Column(name = "grade", precision = 5, scale = 2)
    private BigDecimal grade;

    @Column(name = "feedback", columnDefinition = "TEXT")
    private String feedback;

    @Column(name = "graded_by")
    private UUID gradedBy;

    @Column(name = "ai_suggested_grade", precision = 5, scale = 2)
    private BigDecimal aiSuggestedGrade;

    @Column(name = "ai_grading_rationale", columnDefinition = "TEXT")
    private String aiGradingRationale;

    @Column(name = "status")
    private String status = "SUBMITTED";

    @Column(name = "submitted_at", nullable = false)
    private Instant submittedAt = Instant.now();

    @Column(name = "graded_at")
    private Instant gradedAt;

    public Assignment getAssignment() { return assignment; }
    public void setAssignment(Assignment assignment) { this.assignment = assignment; }
    public User getStudent() { return student; }
    public void setStudent(User student) { this.student = student; }
    public String getSubmissionText() { return submissionText; }
    public void setSubmissionText(String submissionText) { this.submissionText = submissionText; }
    public String getFileUrl() { return fileUrl; }
    public void setFileUrl(String fileUrl) { this.fileUrl = fileUrl; }
    public BigDecimal getGrade() { return grade; }
    public void setGrade(BigDecimal grade) { this.grade = grade; }
    public String getFeedback() { return feedback; }
    public void setFeedback(String feedback) { this.feedback = feedback; }
    public UUID getGradedBy() { return gradedBy; }
    public void setGradedBy(UUID gradedBy) { this.gradedBy = gradedBy; }
    public BigDecimal getAiSuggestedGrade() { return aiSuggestedGrade; }
    public void setAiSuggestedGrade(BigDecimal aiSuggestedGrade) { this.aiSuggestedGrade = aiSuggestedGrade; }
    public String getAiGradingRationale() { return aiGradingRationale; }
    public void setAiGradingRationale(String aiGradingRationale) { this.aiGradingRationale = aiGradingRationale; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public Instant getSubmittedAt() { return submittedAt; }
    public void setSubmittedAt(Instant submittedAt) { this.submittedAt = submittedAt; }
    public Instant getGradedAt() { return gradedAt; }
    public void setGradedAt(Instant gradedAt) { this.gradedAt = gradedAt; }
}
