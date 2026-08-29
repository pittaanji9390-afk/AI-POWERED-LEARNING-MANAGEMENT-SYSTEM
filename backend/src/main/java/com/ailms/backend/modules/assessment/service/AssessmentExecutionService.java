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
