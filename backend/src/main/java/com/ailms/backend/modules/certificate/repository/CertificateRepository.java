package com.ailms.backend.modules.certificate.repository;

import com.ailms.backend.modules.certificate.model.Certificate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface CertificateRepository extends JpaRepository<Certificate, UUID> {
    Optional<Certificate> findByVerificationCode(String verificationCode);
    Optional<Certificate> findByUserIdAndCourseId(UUID userId, UUID courseId);
}
