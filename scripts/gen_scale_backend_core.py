import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("Writing extended backend domain packages...")

# Auth Controllers & Detailed Endpoints
write("backend/src/main/java/com/ailms/backend/modules/auth/controller/MfaController.java", """
package com.ailms.backend.modules.auth.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.common.security.CurrentUser;
import com.ailms.backend.common.security.UserPrincipal;
import com.ailms.backend.modules.auth.service.MfaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/auth/mfa")
@Tag(name = "MFA Security", description = "Multi-factor TOTP configuration and verification")
public class MfaController {

    private final MfaService mfaService;

    public MfaController(MfaService mfaService) {
        this.mfaService = mfaService;
    }

    public record MfaSetupResponse(String secretKey, String qrCodeUri, List<String> recoveryCodes) {}
    public record MfaVerifyRequest(String secretKey, int totpCode) {}

    @PostMapping("/setup")
    @Operation(summary = "Initialize TOTP 2FA secret and recovery codes")
    public ResponseEntity<ApiResponse<MfaSetupResponse>> setupMfa(@CurrentUser UserPrincipal user) {
        String secret = mfaService.generateMfaSecret();
        List<String> recoveryCodes = mfaService.generateRecoveryCodes(8);
        String qrUri = "otpauth://totp/AegisLMS:" + user.getUsername() + "?secret=" + secret + "&issuer=AegisLMS";
        return ResponseEntity.ok(ApiResponse.success("MFA initialized", new MfaSetupResponse(secret, qrUri, recoveryCodes)));
    }

    @PostMapping("/verify")
    @Operation(summary = "Verify TOTP code and activate MFA on account")
    public ResponseEntity<ApiResponse<Boolean>> verifyMfa(
            @CurrentUser UserPrincipal user,
            @RequestBody MfaVerifyRequest request) {
        boolean valid = mfaService.verifyTotpCode(request.secretKey(), request.totpCode());
        return ResponseEntity.ok(ApiResponse.success(valid ? "MFA verified and activated" : "Invalid TOTP verification code", valid));
    }
}
""")

# Extended Course Services & Controllers
write("backend/src/main/java/com/ailms/backend/modules/course/controller/CourseSectionController.java", """
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
""")

write("backend/src/main/java/com/ailms/backend/modules/course/repository/CourseSectionRepository.java", """
package com.ailms.backend.modules.course.repository;

import com.ailms.backend.modules.course.model.CourseSection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface CourseSectionRepository extends JpaRepository<CourseSection, UUID> {
}
""")

# Assessment Controllers
write("backend/src/main/java/com/ailms/backend/modules/assessment/controller/AssessmentController.java", """
package com.ailms.backend.modules.assessment.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.common.security.CurrentUser;
import com.ailms.backend.common.security.UserPrincipal;
import com.ailms.backend.modules.assessment.dto.AssessmentDtos.*;
import com.ailms.backend.modules.assessment.service.AssessmentExecutionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/assessments")
@Tag(name = "Assessments & Grading", description = "Quiz creation, attempt execution, grading, and rubric evaluation")
public class AssessmentController {

    private final AssessmentExecutionService assessmentService;

    public AssessmentController(AssessmentExecutionService assessmentService) {
        this.assessmentService = assessmentService;
    }

    @PostMapping("/quizzes/{quizId}/submit")
    @PreAuthorize("hasRole('STUDENT') or hasRole('TEACHER')")
    @Operation(summary = "Submit quiz answers and evaluate score")
    public ResponseEntity<ApiResponse<QuizResultResponse>> submitQuiz(
            @PathVariable UUID quizId,
            @CurrentUser UserPrincipal user,
            @Valid @RequestBody SubmitQuizRequest request) {
        QuizResultResponse result = assessmentService.evaluateQuizAttempt(user.getId(), quizId, request);
        return ResponseEntity.ok(ApiResponse.success("Assessment evaluated successfully", result));
    }

    @PostMapping("/assignments/{assignmentId}/submit")
    @PreAuthorize("hasRole('STUDENT') or hasRole('TEACHER')")
    @Operation(summary = "Submit assignment writeup or file attachment")
    public ResponseEntity<ApiResponse<Boolean>> submitAssignment(
            @PathVariable UUID assignmentId,
            @CurrentUser UserPrincipal user,
            @Valid @RequestBody SubmitAssignmentRequest request) {
        assessmentService.recordAssignmentSubmission(user.getId(), assignmentId, request);
        return ResponseEntity.ok(ApiResponse.success("Assignment submitted successfully", true));
    }
}
""")

# Assessment Execution Service
write("backend/src/main/java/com/ailms/backend/modules/assessment/service/AssessmentExecutionService.java", """
package com.ailms.backend.modules.assessment.service;

import com.ailms.backend.common.event.DomainEventPublisher;
import com.ailms.backend.common.event.LearningEvent;
import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.assessment.dto.AssessmentDtos.*;
import com.ailms.backend.modules.assessment.model.*;
import com.ailms.backend.modules.assessment.repository.*;
import com.ailms.backend.modules.user.model.User;
import com.ailms.backend.modules.user.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.*;

@Service
public class AssessmentExecutionService {

    private final QuizRepository quizRepository;
    private final QuizAttemptRepository attemptRepository;
    private final AssignmentRepository assignmentRepository;
    private final AssignmentSubmissionRepository submissionRepository;
    private final UserRepository userRepository;
    private final DomainEventPublisher eventPublisher;

    public AssessmentExecutionService(
            QuizRepository quizRepository,
            QuizAttemptRepository attemptRepository,
            AssignmentRepository assignmentRepository,
            AssignmentSubmissionRepository submissionRepository,
            UserRepository userRepository,
            DomainEventPublisher eventPublisher) {
        this.quizRepository = quizRepository;
        this.attemptRepository = attemptRepository;
        this.assignmentRepository = assignmentRepository;
        this.submissionRepository = submissionRepository;
        this.userRepository = userRepository;
        this.eventPublisher = eventPublisher;
    }

    @Transactional
    public QuizResultResponse evaluateQuizAttempt(UUID userId, UUID quizId, SubmitQuizRequest req) {
        Quiz quiz = quizRepository.findById(quizId)
                .orElseThrow(() -> new ResourceNotFoundException("Quiz", "id", quizId));
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", userId));

        int total = quiz.getQuestions().isEmpty() ? 3 : quiz.getQuestions().size();
        int correct = 0;
        List<QuestionFeedbackDto> feedbacks = new ArrayList<>();

        for (Question q : quiz.getQuestions()) {
            Optional<SubmitAnswerRequest> ans = req.answers().stream()
                    .filter(a -> a.questionId().equals(q.getId()))
                    .findFirst();

            boolean isCorrect = false;
            String correctOptionText = "";
            for (QuestionOption opt : q.getOptions()) {
                if (Boolean.TRUE.equals(opt.getIsCorrect())) {
                    correctOptionText = opt.getOptionText();
                    if (ans.isPresent() && opt.getId().toString().equals(ans.get().selectedOptionId())) {
                        isCorrect = true;
                    }
                }
            }
            if (isCorrect) correct++;

            feedbacks.add(new QuestionFeedbackDto(
                    q.getId(), q.getQuestionText(), isCorrect, q.getExplanation(),
                    ans.map(SubmitAnswerRequest::selectedOptionId).orElse("None"),
                    correctOptionText
            ));
        }

        if (quiz.getQuestions().isEmpty()) {
            correct = req.answers().size();
            total = Math.max(req.answers().size(), 1);
        }

        BigDecimal percentage = BigDecimal.valueOf(((double) correct / total) * 100);
        boolean passed = percentage.compareTo(BigDecimal.valueOf(quiz.getPassingScore() != null ? quiz.getPassingScore() : 70)) >= 0;

        QuizAttempt attempt = new QuizAttempt();
        attempt.setQuiz(quiz);
        attempt.setUser(user);
        attempt.setScoreAchieved(percentage);
        attempt.setIsPassed(passed);
        attempt.setTimeSpentSeconds(req.timeSpentSeconds() != null ? req.timeSpentSeconds() : 180);
        attempt.setSubmittedAt(Instant.now());
        attemptRepository.save(attempt);

        eventPublisher.publish(new LearningEvent(
                "QUIZ_COMPLETED", userId, quiz.getCourse().getId(), null, user.getOrganizationId(),
                Map.of("score", percentage, "passed", passed)
        ));

        return new QuizResultResponse(attempt.getId(), percentage, passed, correct, total, attempt.getSubmittedAt(), feedbacks);
    }

    @Transactional
    public void recordAssignmentSubmission(UUID userId, UUID assignmentId, SubmitAssignmentRequest req) {
        Assignment assignment = assignmentRepository.findById(assignmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Assignment", "id", assignmentId));
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", userId));

        AssignmentSubmission submission = new AssignmentSubmission();
        submission.setAssignment(assignment);
        submission.setUser(user);
        submission.setSubmissionText(req.submissionText());
        submission.setFileUrl(req.fileUrl());
        submission.setStatus("SUBMITTED");
        submission.setSubmittedAt(Instant.now());
        submissionRepository.save(submission);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/modules/assessment/repository/QuizRepository.java", """
package com.ailms.backend.modules.assessment.repository;

import com.ailms.backend.modules.assessment.model.Quiz;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface QuizRepository extends JpaRepository<Quiz, UUID> {
}
""")

write("backend/src/main/java/com/ailms/backend/modules/assessment/repository/QuizAttemptRepository.java", """
package com.ailms.backend.modules.assessment.repository;

import com.ailms.backend.modules.assessment.model.QuizAttempt;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface QuizAttemptRepository extends JpaRepository<QuizAttempt, UUID> {
}
""")

write("backend/src/main/java/com/ailms/backend/modules/assessment/repository/AssignmentRepository.java", """
package com.ailms.backend.modules.assessment.repository;

import com.ailms.backend.modules.assessment.model.Assignment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface AssignmentRepository extends JpaRepository<Assignment, UUID> {
}
""")

write("backend/src/main/java/com/ailms/backend/modules/assessment/repository/AssignmentSubmissionRepository.java", """
package com.ailms.backend.modules.assessment.repository;

import com.ailms.backend.modules.assessment.model.AssignmentSubmission;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface AssignmentSubmissionRepository extends JpaRepository<AssignmentSubmission, UUID> {
}
""")

print("Backend core extension written.")
