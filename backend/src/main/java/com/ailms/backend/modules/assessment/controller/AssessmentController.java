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
