package com.ailms.backend.modules.assessment.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

public class AssessmentDtos {

    public record CreateQuizRequest(
            @NotBlank String title,
            String description,
            @NotNull UUID courseId,
            UUID lessonId,
            Integer passingScore,
            Integer timeLimitMinutes,
            Integer maxAttempts,
            Boolean shuffleQuestions,
            List<CreateQuestionRequest> questions
    ) {}

    public record CreateQuestionRequest(
            @NotBlank String questionText,
            @NotBlank String questionType,
            String difficulty,
            String topic,
            String explanation,
            Integer points,
            Boolean aiGenerated,
            List<CreateOptionRequest> options
    ) {}

    public record CreateOptionRequest(
            @NotBlank String optionText,
            Boolean isCorrect,
            Integer sequenceOrder
    ) {}

    public record SubmitQuizRequest(
            @NotNull UUID quizId,
            List<SubmitAnswerRequest> answers,
            Integer timeSpentSeconds
    ) {}

    public record SubmitAnswerRequest(
            @NotNull UUID questionId,
            String selectedOptionId,
            String textResponse
    ) {}

    public record QuizResultResponse(
            UUID attemptId,
            BigDecimal scoreAchieved,
            Boolean isPassed,
            Integer correctCount,
            Integer totalQuestions,
            Instant submittedAt,
            List<QuestionFeedbackDto> feedbacks
    ) {}

    public record QuestionFeedbackDto(
            UUID questionId,
            String questionText,
            Boolean isCorrect,
            String explanation,
            String selectedOption,
            String correctOption
    ) {}

    public record CreateAssignmentRequest(
            @NotBlank String title,
            @NotBlank String instructions,
            @NotNull UUID courseId,
            UUID lessonId,
            Instant dueDate,
            BigDecimal maxScore,
            String allowedFileTypes
    ) {}

    public record SubmitAssignmentRequest(
            @NotNull UUID assignmentId,
            String submissionText,
            String fileUrl
    ) {}

    public record GradeSubmissionRequest(
            @NotNull UUID submissionId,
            @NotNull BigDecimal grade,
            String feedback,
            List<RubricCriterionScoreDto> rubricScores
    ) {}

    public record RubricCriterionScoreDto(
            String criterionTitle,
            BigDecimal score,
            String comments
    ) {}
}
