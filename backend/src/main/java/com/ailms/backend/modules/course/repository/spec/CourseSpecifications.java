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
