package com.ailms.backend.modules.course.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

public class CourseDtos {

    public record CreateCourseRequest(
            @NotBlank String title,
            @NotBlank String slug,
            String shortDescription,
            String description,
            String thumbnailUrl,
            @NotBlank String category,
            String difficulty,
            BigDecimal price,
            String currency,
            Boolean isPublic
    ) {}

    public record CourseSummaryDto(
            UUID id,
            String title,
            String slug,
            String shortDescription,
            String category,
            String difficulty,
            BigDecimal price,
            String currency,
            String status,
            UUID instructorId
    ) {}
}
