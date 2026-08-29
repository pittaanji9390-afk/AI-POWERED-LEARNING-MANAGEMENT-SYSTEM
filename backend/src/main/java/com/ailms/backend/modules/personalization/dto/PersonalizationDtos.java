package com.ailms.backend.modules.personalization.dto;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

public class PersonalizationDtos {

    public record SkillNodeResponse(
            UUID id,
            String name,
            String slug,
            String category,
            String masteryLevel,
            BigDecimal scorePercentage,
            List<String> prerequisiteNames,
            String nextRecommendedAction
    ) {}

    public record LearningPathResponse(
            UUID id,
            String title,
            String slug,
            String description,
            String difficulty,
            Integer estimatedHours,
            List<SkillNodeResponse> skills,
            Integer overallProgressPercent
    ) {}
}
