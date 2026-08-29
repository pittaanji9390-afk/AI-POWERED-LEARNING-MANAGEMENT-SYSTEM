package com.ailms.backend.modules.certificate.service;

import com.ailms.backend.common.exception.ConflictException;
import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.certificate.model.Certificate;
import com.ailms.backend.modules.certificate.repository.CertificateRepository;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.user.model.User;
import com.ailms.backend.modules.user.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.security.MessageDigest;
import java.time.Instant;
import java.util.HexFormat;
import java.util.UUID;

@Service
public class CertificateService {

    private final CertificateRepository certificateRepository;
    private final UserRepository userRepository;
    private final CourseRepository courseRepository;

    public CertificateService(CertificateRepository certificateRepository, UserRepository userRepository, CourseRepository courseRepository) {
        this.certificateRepository = certificateRepository;
        this.userRepository = userRepository;
        this.courseRepository = courseRepository;
    }

    @Transactional
    public Certificate issueCertificate(UUID userId, UUID courseId) {
        if (certificateRepository.findByUserIdAndCourseId(userId, courseId).isPresent()) {
            throw new ConflictException("Certificate already issued for this course and learner.");
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", userId));
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new ResourceNotFoundException("Course", "id", courseId));

        String verificationCode = generateVerificationCode(userId, courseId);

        Certificate cert = new Certificate();
        cert.setUser(user);
        cert.setCourse(course);
        cert.setVerificationCode(verificationCode);
        cert.setIssuedAt(Instant.now());
        cert.setStatus("VALID");
        cert.setCertificateUrl("/api/v1/certificates/verify/" + verificationCode);

        return certificateRepository.save(cert);
    }

    @Transactional(readOnly = true)
    public Certificate verifyCertificate(String verificationCode) {
        return certificateRepository.findByVerificationCode(verificationCode)
                .orElseThrow(() -> new ResourceNotFoundException("Certificate", "verificationCode", verificationCode));
    }

    private String generateVerificationCode(UUID userId, UUID courseId) {
        try {
            String payload = userId.toString() + ":" + courseId.toString() + ":" + System.currentTimeMillis();
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(payload.getBytes());
            return "CERT-" + HexFormat.of().formatHex(hash).substring(0, 16).toUpperCase();
        } catch (Exception e) {
            return "CERT-" + UUID.randomUUID().toString().substring(0, 13).toUpperCase();
        }
    }
}
