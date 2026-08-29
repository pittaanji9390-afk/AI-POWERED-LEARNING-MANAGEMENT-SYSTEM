-- V8: Analytical Aggregation Views for Student, Instructor, and Tenant Dashboards

CREATE OR REPLACE VIEW view_course_completion_stats AS
SELECT 
    c.id AS course_id,
    c.title AS course_title,
    c.organization_id,
    COUNT(e.id) AS total_enrollments,
    COUNT(CASE WHEN e.status = 'COMPLETED' THEN 1 END) AS completed_enrollments,
    AVG(e.completion_percentage) AS avg_completion_percentage,
    MAX(e.last_activity_at) AS latest_student_activity
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
GROUP BY c.id, c.title, c.organization_id;

CREATE OR REPLACE VIEW view_student_mastery_overview AS
SELECT 
    u.id AS user_id,
    u.email AS user_email,
    u.organization_id,
    COUNT(DISTINCT e.course_id) AS enrolled_courses_count,
    COUNT(DISTINCT CASE WHEN e.status = 'COMPLETED' THEN e.course_id END) AS completed_courses_count,
    COALESCE(SUM(lp.seconds_spent), 0) AS total_learning_seconds,
    COUNT(DISTINCT cert.id) AS total_certificates_earned
FROM users u
LEFT JOIN enrollments e ON u.id = e.user_id
LEFT JOIN learning_progress lp ON e.id = lp.enrollment_id
LEFT JOIN certificates cert ON u.id = cert.user_id
GROUP BY u.id, u.email, u.organization_id;

CREATE OR REPLACE VIEW view_assessment_performance_distribution AS
SELECT 
    q.id AS quiz_id,
    q.title AS quiz_title,
    q.course_id,
    COUNT(qa.id) AS total_attempts,
    AVG(qa.score_achieved) AS avg_score,
    COUNT(CASE WHEN qa.is_passed = TRUE THEN 1 END) AS passed_attempts_count,
    AVG(qa.time_spent_seconds) AS avg_time_spent_seconds
FROM quizzes q
LEFT JOIN quiz_attempts qa ON q.id = qa.quiz_id
GROUP BY q.id, q.title, q.course_id;
