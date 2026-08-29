import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# =========================================================================
# 1. EXPANDED BACKEND QUERY SPECIFICATIONS & FILTERS
# =========================================================================
write("backend/src/main/java/com/ailms/backend/modules/course/repository/spec/CourseSpecifications.java", """
package com.ailms.backend.modules.course.repository.spec;

import com.ailms.backend.modules.course.model.Course;
import jakarta.persistence.criteria.Predicate;
import org.springframework.data.jpa.domain.Specification;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public final class CourseSpecifications {

    private CourseSpecifications() {}

    public static Specification<Course> withFilter(
            String searchQuery,
            String category,
            String difficulty,
            BigDecimal minPrice,
            BigDecimal maxPrice,
            String status,
            UUID organizationId,
            Boolean isPublic) {
        return (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();

            if (searchQuery != null && !searchQuery.isBlank()) {
                String likePattern = "%" + searchQuery.toLowerCase().trim() + "%";
                Predicate titleMatch = cb.like(cb.lower(root.get("title")), likePattern);
                Predicate descMatch = cb.like(cb.lower(root.get("shortDescription")), likePattern);
                predicates.add(cb.or(titleMatch, descMatch));
            }

            if (category != null && !category.isBlank()) {
                predicates.add(cb.equal(root.get("category"), category));
            }

            if (difficulty != null && !difficulty.isBlank()) {
                predicates.add(cb.equal(root.get("difficulty"), difficulty));
            }

            if (minPrice != null) {
                predicates.add(cb.greaterThanOrEqualTo(root.get("price"), minPrice));
            }

            if (maxPrice != null) {
                predicates.add(cb.lessThanOrEqualTo(root.get("price"), maxPrice));
            }

            if (status != null && !status.isBlank()) {
                predicates.add(cb.equal(root.get("status"), status));
            }

            if (organizationId != null) {
                predicates.add(cb.equal(root.get("organizationId"), organizationId));
            }

            if (isPublic != null) {
                predicates.add(cb.equal(root.get("isPublic"), isPublic));
            }

            return cb.and(predicates.toArray(new Predicate[0]));
        };
    }
}
""")

write("backend/src/main/java/com/ailms/backend/modules/user/repository/spec/UserSpecifications.java", """
package com.ailms.backend.modules.user.repository.spec;

import com.ailms.backend.modules.user.model.User;
import jakarta.persistence.criteria.Predicate;
import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public final class UserSpecifications {

    private UserSpecifications() {}

    public static Specification<User> withFilter(String query, String status, UUID organizationId) {
        return (root, criteriaQuery, cb) -> {
            List<Predicate> predicates = new ArrayList<>();

            if (query != null && !query.isBlank()) {
                String pattern = "%" + query.toLowerCase().trim() + "%";
                Predicate emailMatch = cb.like(cb.lower(root.get("email")), pattern);
                Predicate firstMatch = cb.like(cb.lower(root.get("firstName")), pattern);
                Predicate lastMatch = cb.like(cb.lower(root.get("lastName")), pattern);
                predicates.add(cb.or(emailMatch, firstMatch, lastMatch));
            }

            if (status != null && !status.isBlank()) {
                predicates.add(cb.equal(root.get("status"), status));
            }

            if (organizationId != null) {
                predicates.add(cb.equal(root.get("organizationId"), organizationId));
            }

            return cb.and(predicates.toArray(new Predicate[0]));
        };
    }
}
""")

# =========================================================================
# 2. SEED QUESTION POOLS & DOMAIN CURRICULA (V9 & V10)
# =========================================================================
write("backend/src/main/resources/db/migration/V9__seed_question_bank_and_quizzes.sql", """
-- V9: Enterprise Question Bank, Assessment Modules, and Question Rubrics

INSERT INTO quizzes (id, course_id, lesson_id, title, description, passing_score, time_limit_minutes, max_attempts, is_active, created_at, updated_at)
VALUES
  ('77777777-1111-1111-1111-111111111101', '11111111-1111-1111-1111-111111111111', '33333333-1111-1111-1111-111111111101', 'Distributed Consensus & Raft Architecture Assessment', 'Evaluates understanding of Raft leader election, split votes, and log compaction.', 80, 20, 3, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('77777777-1111-1111-1111-111111111102', '11111111-1111-1111-1111-111111111111', '33333333-1111-1111-1111-111111111103', 'pgvector & High-Dimensional HNSW Vector Indexing Exam', 'Evaluates cosine distance metric properties, HNSW graph parameters, and RAG retrieval latency.', 75, 15, 3, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Seed Questions for Quiz 1
INSERT INTO questions (id, quiz_id, question_text, question_type, points, difficulty, explanation, sequence_order, is_active, created_at, updated_at)
VALUES
  ('88888888-1111-1111-1111-111111111101', '77777777-1111-1111-1111-111111111101', 'In the Raft consensus protocol, what mechanism prevents two candidates from simultaneously splitting votes indefinitely?', 'MULTIPLE_CHOICE', 10, 'HARD', 'Randomized election timeouts ensure one node times out first and requests votes before competitors.', 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('88888888-1111-1111-1111-111111111102', '77777777-1111-1111-1111-111111111101', 'Under what condition does a Raft leader consider a log entry committed and safe to apply to its state machine?', 'MULTIPLE_CHOICE', 10, 'HARD', 'Once replicated across a strict majority (quorum) of active cluster nodes.', 2, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('88888888-1111-1111-1111-111111111103', '77777777-1111-1111-1111-111111111102', 'Which index type in pgvector requires rebuilding after substantial dataset insertions to maintain high recall?', 'MULTIPLE_CHOICE', 10, 'MEDIUM', 'IVFFlat relies on static centroid clusters, whereas HNSW continuously updates its hierarchical graph.', 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Seed Options for Question 1
INSERT INTO question_options (id, question_id, option_text, is_correct, sequence_order, created_at, updated_at)
VALUES
  ('99999999-1111-1111-1111-111111111101', '88888888-1111-1111-1111-111111111101', 'Randomized election timeouts between 150ms and 300ms', TRUE, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('99999999-1111-1111-1111-111111111102', '88888888-1111-1111-1111-111111111101', 'Fixed round-robin node priority rankings', FALSE, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('99999999-1111-1111-1111-111111111103', '88888888-1111-1111-1111-111111111101', 'Centralized NTP wall-clock timestamp comparisons', FALSE, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('99999999-1111-1111-1111-111111111104', '88888888-1111-1111-1111-111111111101', 'Synchronous two-phase commit lock acquisitions', FALSE, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;
""")

write("backend/src/main/resources/db/migration/V10__seed_sample_discussions_and_reviews.sql", """
-- V10: Sample Discussions, Community Comments, and Verified Course Reviews

INSERT INTO discussions (id, course_id, author_id, organization_id, title, content, upvotes_count, status, created_at, updated_at)
VALUES
  ('aaaaaaaa-1111-1111-1111-111111111101', '11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000001', 'Best practices for HNSW parameter tuning in high-throughput PostgreSQL workloads', 'When tuning m=16 and ef_construction=64 vs m=32 and ef_construction=128, what memory overhead should we budget per 100k 1536-dimensional vectors?', 18, 'VISIBLE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('aaaaaaaa-1111-1111-1111-111111111102', '11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000001', 'Handling distributed compensations when an external Stripe payment webhook times out', 'If the inventory reservation service succeeds but the payment confirmation webhook fails after retries, how should the compensating saga execute?', 24, 'VISIBLE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;
""")

print("Part 1 Specifications and Seeds written.")
