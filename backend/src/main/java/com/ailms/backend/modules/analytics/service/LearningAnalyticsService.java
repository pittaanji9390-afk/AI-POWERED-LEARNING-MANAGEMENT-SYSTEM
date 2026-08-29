package com.ailms.backend.modules.analytics.service;

import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.UUID;

@Service
public class LearningAnalyticsService {

    public record PlatformStatsDto(
            long totalLearners,
            long activeCourses,
            double averageCompletionRate,
            long aiQueriesProcessedToday,
            double totalRevenueUsd
    ) {}

    public PlatformStatsDto getPlatformOverview(UUID organizationId) {
        return new PlatformStatsDto(
                4270,
                18,
                78.4,
                12840,
                48290.00
        );
    }
}
