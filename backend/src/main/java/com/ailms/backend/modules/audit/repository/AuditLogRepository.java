package com.ailms.backend.modules.audit.repository;

import com.ailms.backend.modules.audit.model.AuditLog;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, UUID> {
    Page<AuditLog> findByOrganizationId(UUID organizationId, Pageable pageable);
    Page<AuditLog> findByActorId(UUID actorId, Pageable pageable);
}
