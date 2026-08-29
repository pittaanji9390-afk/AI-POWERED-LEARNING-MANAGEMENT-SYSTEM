import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# SkillMasteryService.java
write("backend/src/main/java/com/ailms/backend/modules/personalization/service/SkillMasteryService.java", """
package com.ailms.backend.modules.personalization.service;

import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Service
public class SkillMasteryService {

    public enum MasteryLevel {
        NOT_STARTED, INTRODUCED, PRACTICING, PROFICIENT, MASTERED
    }

    public record SkillProgressDto(UUID skillId, String skillName, MasteryLevel level, BigDecimal scorePercent) {}

    public MasteryLevel calculateMastery(BigDecimal quizScore, int practicalLabsCompleted) {
        double score = quizScore != null ? quizScore.doubleValue() : 0.0;
        if (score >= 90.0 && practicalLabsCompleted >= 3) return MasteryLevel.MASTERED;
        if (score >= 75.0 && practicalLabsCompleted >= 1) return MasteryLevel.PROFICIENT;
        if (score >= 50.0) return MasteryLevel.PRACTICING;
        if (score > 0.0) return MasteryLevel.INTRODUCED;
        return MasteryLevel.NOT_STARTED;
    }
}
""")

# AdaptiveRecommendationEngine.java
write("backend/src/main/java/com/ailms/backend/modules/personalization/service/AdaptiveRecommendationEngine.java", """
package com.ailms.backend.modules.personalization.service;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class AdaptiveRecommendationEngine {

    public record RecommendationItem(String title, String rationale, String targetRoute, int priority) {}

    public List<RecommendationItem> generateRecommendations(UUID studentId) {
        List<RecommendationItem> items = new ArrayList<>();
        items.add(new RecommendationItem(
                "Strengthen RAG Prompt Delimiters",
                "Your recent score on AI Security was 64%. Review boundary sanitization to unlock Distributed Sagas.",
                "/quizzes/rag-sec-1/take",
                1
        ));
        items.add(new RecommendationItem(
                "Interactive Lab: pgvector HNSW Performance Benchmark",
                "You mastered Vector Embeddings. Practice tuning M and efConstruction parameters.",
                "/lab",
                2
        ));
        return items;
    }
}
""")

# LearningAnalyticsService.java
write("backend/src/main/java/com/ailms/backend/modules/analytics/service/LearningAnalyticsService.java", """
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
""")

# PaymentProcessingService.java
write("backend/src/main/java/com/ailms/backend/modules/payment/service/PaymentProcessingService.java", """
package com.ailms.backend.modules.payment.service;

import com.ailms.backend.common.exception.BadRequestException;
import com.ailms.backend.modules.payment.model.Payment;
import com.ailms.backend.modules.payment.repository.PaymentRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.UUID;

@Service
public class PaymentProcessingService {

    private final PaymentRepository paymentRepository;

    public PaymentProcessingService(PaymentRepository paymentRepository) {
        this.paymentRepository = paymentRepository;
    }

    @Transactional
    public Payment executePayment(UUID userId, BigDecimal amount, String currency, String type, String idempotencyKey) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new BadRequestException("Payment amount must be greater than zero.");
        }

        Payment payment = new Payment();
        payment.setAmount(amount);
        payment.setCurrency(currency != null ? currency : "USD");
        payment.setPaymentType(type);
        payment.setProvider("STRIPE");
        payment.setIdempotencyKey(idempotencyKey != null ? idempotencyKey : UUID.randomUUID().toString());
        payment.setProviderTransactionId("txn_" + UUID.randomUUID().toString().substring(0, 16));
        payment.setStatus("SUCCEEDED");

        return paymentRepository.save(payment);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/modules/payment/repository/PaymentRepository.java", """
package com.ailms.backend.modules.payment.repository;

import com.ailms.backend.modules.payment.model.Payment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface PaymentRepository extends JpaRepository<Payment, UUID> {
    Optional<Payment> findByIdempotencyKey(String idempotencyKey);
}
""")

# NotificationDispatcherService.java
write("backend/src/main/java/com/ailms/backend/modules/notification/service/NotificationDispatcherService.java", """
package com.ailms.backend.modules.notification.service;

import com.ailms.backend.modules.notification.model.Notification;
import com.ailms.backend.modules.notification.repository.NotificationRepository;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.UUID;

@Service
public class NotificationDispatcherService {

    private final NotificationRepository notificationRepository;

    public NotificationDispatcherService(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    @Async("eventTaskExecutor")
    public void dispatch(UUID userId, String title, String body, String type, String linkUrl) {
        Notification n = new Notification();
        n.setTitle(title);
        n.setBody(body);
        n.setNotificationType(type);
        n.setLinkUrl(linkUrl);
        n.setIsRead(false);
        n.setCreatedAt(Instant.now());
        notificationRepository.save(n);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/modules/notification/repository/NotificationRepository.java", """
package com.ailms.backend.modules.notification.repository;

import com.ailms.backend.modules.notification.model.Notification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, UUID> {
    List<Notification> findByUserIdAndIsReadFalse(UUID userId);
}
""")

print("Batch 3 Personalization, Analytics, Payment, and Notification services generated successfully.")
