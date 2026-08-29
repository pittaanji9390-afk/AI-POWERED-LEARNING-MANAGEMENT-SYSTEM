package com.ailms.backend.modules.discussion.repository;

import com.ailms.backend.modules.discussion.model.Discussion;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface DiscussionRepository extends JpaRepository<Discussion, UUID> {
    Page<Discussion> findByCourseIdAndStatus(UUID courseId, String status, Pageable pageable);
}
