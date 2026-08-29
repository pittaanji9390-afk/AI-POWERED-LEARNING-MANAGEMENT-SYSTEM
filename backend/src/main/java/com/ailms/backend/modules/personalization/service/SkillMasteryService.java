package com.ailms.backend.modules.personalization.service;

import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Service
public class SkillMasteryService {

    public enum MasteryLevel {
        NOT_STARTED, INTRODUCED, PRACTICING, PROFICIENT, MASTERED
    }

    public record SkillProgressDto(UUID skillId, String skillName, MasteryLevel level, BigDecimal scorePercent) {}

    public MasteryLevel calculateMastery(BigDecimal quizScore, int practicalLabsCompleted) {
        double score = quizScore != null ? quizScore.doubleValue() : 0.0;
        if (score >= 90.0 && practicalLabsCompleted >= 3) return MasteryLevel.MASTERED;
        if (score >= 75.0 && practicalLabsCompleted >= 1) return MasteryLevel.PROFICIENT;
        if (score >= 50.0) return MasteryLevel.PRACTICING;
        if (score > 0.0) return MasteryLevel.INTRODUCED;
        return MasteryLevel.NOT_STARTED;
    }
}
