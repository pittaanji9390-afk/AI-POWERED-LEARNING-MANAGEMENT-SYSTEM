import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# ----------------- MFA & SECURITY SERVICES -----------------
write("backend/src/main/java/com/ailms/backend/modules/auth/service/MfaService.java", """
package com.ailms.backend.modules.auth.service;

import com.ailms.backend.common.exception.BadRequestException;
import org.springframework.stereotype.Service;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.ByteBuffer;
import java.security.SecureRandom;
import java.util.*;

@Service
public class MfaService {

    private static final String BASE32_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    private static final SecureRandom RANDOM = new SecureRandom();

    public String generateMfaSecret() {
        byte[] buffer = new byte[20];
        RANDOM.nextBytes(buffer);
        StringBuilder secret = new StringBuilder(32);
        for (byte b : buffer) {
            secret.append(BASE32_CHARS.charAt((b & 0xFF) % BASE32_CHARS.length()));
        }
        return secret.toString();
    }

    public List<String> generateRecoveryCodes(int count) {
        List<String> codes = new ArrayList<>(count);
        for (int i = 0; i < count; i++) {
            StringBuilder code = new StringBuilder();
            for (int j = 0; j < 10; j++) {
                if (j == 5) code.append("-");
                code.append(Integer.toHexString(RANDOM.nextInt(16)).toUpperCase());
            }
            codes.add(code.toString());
        }
        return codes;
    }

    public boolean verifyTotpCode(String secret, int inputCode) {
        long currentInterval = System.currentTimeMillis() / 1000 / 30;
        // Verify current window +- 1 interval (clock drift tolerance)
        for (int i = -1; i <= 1; i++) {
            if (generateTotp(secret, currentInterval + i) == inputCode) {
                return true;
            }
        }
        return false;
    }

    private int generateTotp(String secret, long timeInterval) {
        try {
            byte[] key = decodeBase32(secret);
            byte[] data = ByteBuffer.allocate(8).putLong(timeInterval).array();
            Mac mac = Mac.getInstance("HmacSHA1");
            mac.init(new SecretKeySpec(key, "HmacSHA1"));
            byte[] hash = mac.doFinal(data);

            int offset = hash[hash.length - 1] & 0x0F;
            int binary = ((hash[offset] & 0x7F) << 24)
                    | ((hash[offset + 1] & 0xFF) << 16)
                    | ((hash[offset + 2] & 0xFF) << 8)
                    | (hash[offset + 3] & 0xFF);

            return binary % 1_000_000;
        } catch (Exception e) {
            throw new BadRequestException("Failed to verify TOTP code: " + e.getMessage());
        }
    }

    private byte[] decodeBase32(String secret) {
        byte[] bytes = new byte[secret.length() * 5 / 8];
        int buffer = 0;
        int bitsLeft = 0;
        int count = 0;

        for (char c : secret.toUpperCase().toCharArray()) {
            int val = BASE32_CHARS.indexOf(c);
            if (val < 0) continue;
            buffer = (buffer << 5) | val;
            bitsLeft += 5;
            if (bitsLeft >= 8) {
                bytes[count++] = (byte) ((buffer >> (bitsLeft - 8)) & 0xFF);
                bitsLeft -= 8;
            }
        }
        return bytes;
    }
}
""")

write("backend/src/main/java/com/ailms/backend/modules/auth/service/PasswordPolicyService.java", """
package com.ailms.backend.modules.auth.service;

import com.ailms.backend.common.exception.BadRequestException;
import org.springframework.stereotype.Service;

import java.util.Set;
import java.util.regex.Pattern;

@Service
public class PasswordPolicyService {

    private static final int MIN_LENGTH = 8;
    private static final int MAX_LENGTH = 128;
    private static final Pattern HAS_UPPERCASE = Pattern.compile("[A-Z]");
    private static final Pattern HAS_LOWERCASE = Pattern.compile("[a-z]");
    private static final Pattern HAS_DIGIT = Pattern.compile("[0-9]");
    private static final Pattern HAS_SPECIAL = Pattern.compile("[!@#$%^&*()_+\\-=\\[\\]{};':\\\"\\\\|,.<>\\/?]");

    private static final Set<String> COMMON_PASSWORDS = Set.of(
            "password", "password123", "admin123", "qwerty123", "letmein123", "welcome123"
    );

    public void validatePassword(String password) {
        if (password == null || password.length() < MIN_LENGTH || password.length() > MAX_LENGTH) {
            throw new BadRequestException(String.format("Password must be between %d and %d characters.", MIN_LENGTH, MAX_LENGTH));
        }
        if (!HAS_UPPERCASE.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one uppercase letter (A-Z).");
        }
        if (!HAS_LOWERCASE.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one lowercase letter (a-z).");
        }
        if (!HAS_DIGIT.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one numerical digit (0-9).");
        }
        if (!HAS_SPECIAL.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one special symbol.");
        }
        if (COMMON_PASSWORDS.contains(password.toLowerCase())) {
            throw new BadRequestException("Password is too common and easily guessed. Please choose a stronger password.");
        }
    }
}
""")

# ----------------- COURSE STATE MACHINE & LIFECYCLE -----------------
write("backend/src/main/java/com/ailms/backend/modules/course/service/CourseLifecycleService.java", """
package com.ailms.backend.modules.course.service;

import com.ailms.backend.common.exception.BadRequestException;
import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.audit.model.AuditLog;
import com.ailms.backend.modules.audit.repository.AuditLogRepository;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Set;
import java.util.UUID;

@Service
public class CourseLifecycleService {

    private final CourseRepository courseRepository;
    private final AuditLogRepository auditLogRepository;

    public CourseLifecycleService(CourseRepository courseRepository, AuditLogRepository auditLogRepository) {
        this.courseRepository = courseRepository;
        this.auditLogRepository = auditLogRepository;
    }

    public enum CourseState {
        DRAFT, IN_REVIEW, PUBLISHED, UNPUBLISHED, ARCHIVED
    }

    @Transactional
    public Course transitionState(UUID courseId, CourseState targetState, UUID actorId, String reason) {
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new ResourceNotFoundException("Course", "id", courseId));

        CourseState currentState = CourseState.valueOf(course.getStatus());
        validateTransition(currentState, targetState, course);

        course.setStatus(targetState.name());
        Course updated = courseRepository.save(course);

        AuditLog log = new AuditLog();
        log.setActorId(actorId);
        log.setAction("COURSE_STATE_TRANSITION");
        log.setEntityType("Course");
        log.setEntityId(courseId.toString());
        log.setOrganizationId(course.getOrganizationId());
        auditLogRepository.save(log);

        return updated;
    }

    private void validateTransition(CourseState current, CourseState target, Course course) {
        switch (current) {
            case DRAFT -> {
                if (target != CourseState.IN_REVIEW && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("Draft course can only transition to IN_REVIEW or ARCHIVED.");
                }
                if (target == CourseState.IN_REVIEW && course.getSections().isEmpty()) {
                    throw new BadRequestException("Course must contain at least one section before submitting for review.");
                }
            }
            case IN_REVIEW -> {
                if (target != CourseState.PUBLISHED && target != CourseState.DRAFT && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("In-review course can only be PUBLISHED, returned to DRAFT, or ARCHIVED.");
                }
            }
            case PUBLISHED -> {
                if (target != CourseState.UNPUBLISHED && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("Published course can only be UNPUBLISHED or ARCHIVED.");
                }
            }
            case UNPUBLISHED -> {
                if (target != CourseState.PUBLISHED && target != CourseState.ARCHIVED) {
                    throw new BadRequestException("Unpublished course can only be republished or ARCHIVED.");
                }
            }
            case ARCHIVED -> throw new BadRequestException("Archived courses cannot transition to any active state.");
        }
    }
}
""")

# ----------------- PROGRESS & LEARNING TELEMETRY -----------------
write("backend/src/main/java/com/ailms/backend/modules/progress/service/ProgressTrackingService.java", """
package com.ailms.backend.modules.progress.service;

import com.ailms.backend.common.event.DomainEventPublisher;
import com.ailms.backend.common.event.LearningEvent;
import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.model.Lesson;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.course.repository.LessonRepository;
import com.ailms.backend.modules.enrollment.model.Enrollment;
import com.ailms.backend.modules.enrollment.model.LearningProgress;
import com.ailms.backend.modules.enrollment.repository.EnrollmentRepository;
import com.ailms.backend.modules.enrollment.repository.LearningProgressRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class ProgressTrackingService {

    private final EnrollmentRepository enrollmentRepository;
    private final LearningProgressRepository progressRepository;
    private final LessonRepository lessonRepository;
    private final CourseRepository courseRepository;
    private final DomainEventPublisher eventPublisher;

    public ProgressTrackingService(
            EnrollmentRepository enrollmentRepository,
            LearningProgressRepository progressRepository,
            LessonRepository lessonRepository,
            CourseRepository courseRepository,
            DomainEventPublisher eventPublisher) {
        this.enrollmentRepository = enrollmentRepository;
        this.progressRepository = progressRepository;
        this.lessonRepository = lessonRepository;
        this.courseRepository = courseRepository;
        this.eventPublisher = eventPublisher;
    }

    @Transactional
    public LearningProgress recordLessonHeartbeat(UUID enrollmentId, UUID lessonId, int secondsSpent, int lastPosition) {
        Enrollment enrollment = enrollmentRepository.findById(enrollmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Enrollment", "id", enrollmentId));

        Lesson lesson = lessonRepository.findById(lessonId)
                .orElseThrow(() -> new ResourceNotFoundException("Lesson", "id", lessonId));

        LearningProgress progress = progressRepository.findByEnrollmentIdAndLessonId(enrollmentId, lessonId)
                .orElseGet(() -> {
                    LearningProgress lp = new LearningProgress();
                    lp.setEnrollment(enrollment);
                    lp.setLesson(lesson);
                    return lp;
                });

        progress.setSecondsSpent(progress.getSecondsSpent() + secondsSpent);
        progress.setLastPositionSeconds(lastPosition);

        int lessonDuration = lesson.getDurationSeconds() > 0 ? lesson.getDurationSeconds() : 600;
        int calculatedPercent = Math.min(100, (int) (((double) lastPosition / lessonDuration) * 100));
        progress.setProgressPercent(Math.max(progress.getProgressPercent(), calculatedPercent));

        if (progress.getProgressPercent() >= 90 && !"COMPLETED".equals(progress.getStatus())) {
            progress.setStatus("COMPLETED");
            progress.setCompletedAt(Instant.now());

            eventPublisher.publish(new LearningEvent(
                    "LESSON_COMPLETED", enrollment.getUser().getId(), enrollment.getCourse().getId(), lessonId, enrollment.getOrganizationId(),
                    Map.of("progress", 100, "durationSeconds", progress.getSecondsSpent())
            ));
        }

        enrollment.setLastActivityAt(Instant.now());
        recalculateCourseProgress(enrollment);

        return progressRepository.save(progress);
    }

    private void recalculateCourseProgress(Enrollment enrollment) {
        Course course = courseRepository.findById(enrollment.getCourse().getId()).orElse(null);
        if (course == null) return;

        int totalLessons = course.getSections().stream().mapToInt(s -> s.getLessons().size()).sum();
        if (totalLessons == 0) return;

        List<LearningProgress> completedList = progressRepository.findByEnrollmentIdAndStatus(enrollment.getId(), "COMPLETED");
        int completionPercent = (int) (((double) completedList.size() / totalLessons) * 100);
        enrollment.setCompletionPercentage(completionPercent);

        if (completionPercent >= 100 && !"COMPLETED".equals(enrollment.getStatus())) {
            enrollment.setStatus("COMPLETED");
            enrollment.setCompletedAt(Instant.now());

            eventPublisher.publish(new LearningEvent(
                    "COURSE_COMPLETED", enrollment.getUser().getId(), enrollment.getCourse().getId(), null, enrollment.getOrganizationId(),
                    Map.of("totalLessons", totalLessons)
            ));
        }
        enrollmentRepository.save(enrollment);
    }
}
""")

# ----------------- REPOSITORIES EXPANSION -----------------
write("backend/src/main/java/com/ailms/backend/modules/enrollment/repository/LearningProgressRepository.java", """
package com.ailms.backend.modules.enrollment.repository;

import com.ailms.backend.modules.enrollment.model.LearningProgress;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface LearningProgressRepository extends JpaRepository<LearningProgress, UUID> {
    Optional<LearningProgress> findByEnrollmentIdAndLessonId(UUID enrollmentId, UUID lessonId);
    List<LearningProgress> findByEnrollmentId(UUID enrollmentId);
    List<LearningProgress> findByEnrollmentIdAndStatus(UUID enrollmentId, String status);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/course/repository/LessonRepository.java", """
package com.ailms.backend.modules.course.repository;

import com.ailms.backend.modules.course.model.Lesson;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface LessonRepository extends JpaRepository<Lesson, UUID> {
}
""")

write("backend/src/main/java/com/ailms/backend/modules/audit/repository/AuditLogRepository.java", """
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
""")

# ----------------- CERTIFICATE SERVICE -----------------
write("backend/src/main/java/com/ailms/backend/modules/certificate/service/CertificateService.java", """
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
""")

write("backend/src/main/java/com/ailms/backend/modules/certificate/repository/CertificateRepository.java", """
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
""")

print("Batch 1 Backend modules generated successfully.")
