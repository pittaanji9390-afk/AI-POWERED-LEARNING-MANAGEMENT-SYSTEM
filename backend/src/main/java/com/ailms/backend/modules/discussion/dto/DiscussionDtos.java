package com.ailms.backend.modules.discussion.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.Instant;
import java.util.UUID;

public class DiscussionDtos {

    public record CreateDiscussionRequest(
            @NotBlank String title,
            @NotBlank String content,
            @NotNull UUID courseId,
            UUID lessonId,
            String tag
    ) {}

    public record AddCommentRequest(
            @NotBlank String content,
            @NotNull UUID discussionId,
            UUID parentCommentId
    ) {}

    public record CreateReviewRequest(
            @NotNull UUID courseId,
            @NotNull Integer rating,
            String reviewTitle,
            String reviewText
    ) {}

    public record CreateReportRequest(
            @NotBlank String targetEntityType,
            @NotNull UUID targetEntityId,
            @NotBlank String reason,
            String details
    ) {}
}
