package com.ailms.backend.modules.analytics.dto;

import java.util.List;
import java.util.Map;

public class AnalyticsDtos {

    public record StudentAnalyticsSummary(
            int enrolledCoursesCount,
            int completedLessonsCount,
            int totalHoursLearned,
            double averageQuizScore,
            int certificatesEarned,
            List<DailyActivityDto> recentActivity
    ) {}

    public record TeacherAnalyticsSummary(
            int totalPublishedCourses,
            int totalActiveLearners,
            int pendingGradingCount,
            double averageCourseRating,
            double completionRatePercent,
            List<CoursePerformanceDto> courses
    ) {}

    public record DailyActivityDto(String date, int minutesLearned, int lessonsCompleted) {}
    public record CoursePerformanceDto(String courseTitle, int enrolledCount, double avgScore, double completionRate) {}
}
