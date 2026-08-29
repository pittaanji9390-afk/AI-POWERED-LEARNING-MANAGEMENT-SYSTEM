import os

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# Events
write("backend/src/main/java/com/ailms/backend/common/event/DomainEvent.java", """
package com.ailms.backend.common.event;

import java.time.Instant;
import java.util.UUID;

public interface DomainEvent {
    UUID getEventId();
    Instant getOccurredAt();
    String getEventType();
    UUID getTenantId();
}
""")

write("backend/src/main/java/com/ailms/backend/common/event/LearningEvent.java", """
package com.ailms.backend.common.event;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;

public class LearningEvent implements DomainEvent {
    private final UUID eventId;
    private final Instant occurredAt;
    private final String eventType;
    private final UUID studentId;
    private final UUID courseId;
    private final UUID lessonId;
    private final UUID tenantId;
    private final Map<String, Object> payload;

    public LearningEvent(String eventType, UUID studentId, UUID courseId, UUID lessonId, UUID tenantId, Map<String, Object> payload) {
        this.eventId = UUID.randomUUID();
        this.occurredAt = Instant.now();
        this.eventType = eventType;
        this.studentId = studentId;
        this.courseId = courseId;
        this.lessonId = lessonId;
        this.tenantId = tenantId;
        this.payload = payload != null ? payload : Map.of();
    }

    @Override public UUID getEventId() { return eventId; }
    @Override public Instant getOccurredAt() { return occurredAt; }
    @Override public String getEventType() { return eventType; }
    @Override public UUID getTenantId() { return tenantId; }
    public UUID getStudentId() { return studentId; }
    public UUID getCourseId() { return courseId; }
    public UUID getLessonId() { return lessonId; }
    public Map<String, Object> getPayload() { return payload; }
}
""")

write("backend/src/main/java/com/ailms/backend/common/event/DomainEventPublisher.java", """
package com.ailms.backend.common.event;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Component;

@Component
public class DomainEventPublisher {
    private static final Logger log = LoggerFactory.getLogger(DomainEventPublisher.class);
    private final ApplicationEventPublisher publisher;

    public DomainEventPublisher(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }

    public void publish(DomainEvent event) {
        log.debug("Publishing domain event: [type={}, id={}]", event.getEventType(), event.getEventId());
        publisher.publishEvent(event);
    }
}
""")

# AI Providers
write("backend/src/main/java/com/ailms/backend/modules/ai/provider/AiModelResponse.java", """
package com.ailms.backend.modules.ai.provider;

import java.util.List;
import java.util.Map;

public record AiModelResponse(
        String content,
        String model,
        int promptTokens,
        int completionTokens,
        int totalTokens,
        double estimatedCostUsd,
        Map<String, Object> metadata,
        List<String> citations
) {}
""")

write("backend/src/main/java/com/ailms/backend/modules/ai/provider/AiProvider.java", """
package com.ailms.backend.modules.ai.provider;

public interface AiProvider {
    String getProviderId();
    boolean isHealthy();
}
""")

write("backend/src/main/java/com/ailms/backend/modules/ai/provider/LlmProvider.java", """
package com.ailms.backend.modules.ai.provider;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

public interface LlmProvider extends AiProvider {
    AiModelResponse generateResponse(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options);
    CompletableFuture<AiModelResponse> generateResponseAsync(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options);
    <T> T generateStructuredOutput(String systemPrompt, String userMessage, Class<T> responseSchema, Map<String, Object> options);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/ai/provider/EmbeddingProvider.java", """
package com.ailms.backend.modules.ai.provider;

import java.util.List;

public interface EmbeddingProvider extends AiProvider {
    List<Float> generateEmbedding(String text);
    List<List<Float>> generateBatchEmbeddings(List<String> texts);
    int getDimension();
}
""")

write("backend/src/main/java/com/ailms/backend/modules/ai/provider/ModerationProvider.java", """
package com.ailms.backend.modules.ai.provider;

import java.util.List;

public interface ModerationProvider extends AiProvider {
    record ModerationResult(boolean isFlagged, List<String> categories, double riskScore, String reason) {}
    ModerationResult checkContent(String content);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/ai/provider/MockAiProvider.java", """
package com.ailms.backend.modules.ai.provider;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.CompletableFuture;

@Service
public class MockAiProvider implements LlmProvider, EmbeddingProvider, ModerationProvider {

    private final ObjectMapper objectMapper;

    public MockAiProvider(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @Override public String getProviderId() { return "mock"; }
    @Override public boolean isHealthy() { return true; }

    @Override
    public AiModelResponse generateResponse(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options) {
        String mockResponse = "Hello! I am your AI Learning Assistant. Based on your course materials, here is a clear explanation: " + userMessage;
        return new AiModelResponse(mockResponse, "mock-v1", 20, 45, 65, 0.0, Map.of("provider", "mock"), List.of("Course Syllabus - Section 1"));
    }

    @Override
    public CompletableFuture<AiModelResponse> generateResponseAsync(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options) {
        return CompletableFuture.completedFuture(generateResponse(systemPrompt, userMessage, chatHistory, options));
    }

    @Override
    public <T> T generateStructuredOutput(String systemPrompt, String userMessage, Class<T> responseSchema, Map<String, Object> options) {
        try {
            return objectMapper.readValue("{}", responseSchema);
        } catch (Exception e) {
            return null;
        }
    }

    @Override
    public List<Float> generateEmbedding(String text) {
        List<Float> embedding = new ArrayList<>(1536);
        for (int i = 0; i < 1536; i++) embedding.add((float) Math.random());
        return embedding;
    }

    @Override
    public List<List<Float>> generateBatchEmbeddings(List<String> texts) {
        return texts.stream().map(this::generateEmbedding).toList();
    }

    @Override public int getDimension() { return 1536; }

    @Override
    public ModerationResult checkContent(String content) {
        return new ModerationResult(false, List.of(), 0.01, "Safe educational content");
    }
}
""")

# Search, Storage, Payment, Notification
write("backend/src/main/java/com/ailms/backend/modules/search/SearchService.java", """
package com.ailms.backend.modules.search;

import java.util.List;
import java.util.Map;
import java.util.UUID;

public interface SearchService {
    record SearchResultItem(UUID id, String title, String snippet, String type, double score, Map<String, Object> metadata) {}
    List<SearchResultItem> searchCatalog(String query, UUID organizationId, Map<String, Object> filters, int page, int size);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/storage/StorageFileMetadata.java", """
package com.ailms.backend.modules.storage;

import java.time.Instant;

public record StorageFileMetadata(
        String storageKey,
        String originalFilename,
        String contentType,
        long sizeInBytes,
        Instant uploadedAt,
        String downloadUrl
) {}
""")

write("backend/src/main/java/com/ailms/backend/modules/storage/ObjectStorageService.java", """
package com.ailms.backend.modules.storage;

import java.io.InputStream;
import java.time.Duration;

public interface ObjectStorageService {
    StorageFileMetadata uploadFile(String path, InputStream inputStream, String contentType, long size);
    String generatePresignedDownloadUrl(String storageKey, Duration expiry);
    String generatePresignedUploadUrl(String path, String contentType, Duration expiry);
    void deleteFile(String storageKey);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/payment/PaymentGatewayProvider.java", """
package com.ailms.backend.modules.payment;

import java.math.BigDecimal;
import java.util.Map;
import java.util.UUID;

public interface PaymentGatewayProvider {
    record PaymentSessionResult(String sessionId, String checkoutUrl, String referenceId) {}
    record WebhookValidationResult(boolean isValid, String eventType, String paymentId, BigDecimal amount, String currency, Map<String, Object> payload) {}

    PaymentSessionResult createCheckoutSession(UUID userId, BigDecimal amount, String currency, String itemType, UUID itemId, String idempotencyKey);
    WebhookValidationResult processWebhook(String payload, String signatureHeader);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/notification/NotificationSender.java", """
package com.ailms.backend.modules.notification;

import java.util.Map;
import java.util.UUID;

public interface NotificationSender {
    void sendInApp(UUID userId, String title, String body, Map<String, Object> data);
    void sendEmail(String recipientEmail, String subject, String templateName, Map<String, Object> variables);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/auth/controller/HealthController.java", """
package com.ailms.backend.modules.auth.controller;

import com.ailms.backend.common.api.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/health")
@Tag(name = "System Health", description = "System probe & health status endpoints")
public class HealthController {

    @GetMapping
    @Operation(summary = "System status check")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getHealth() {
        Map<String, Object> healthInfo = Map.of(
                "status", "UP",
                "service", "ai-lms-backend",
                "version", "1.0.0",
                "timestamp", Instant.now().toString(),
                "aiOrchestration", "READY"
        );
        return ResponseEntity.ok(ApiResponse.success("System is operational", healthInfo));
    }
}
""")

write("backend/src/test/java/com/ailms/backend/LmsApplicationTests.java", """
package com.ailms.backend;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
@ActiveProfiles("dev")
class LmsApplicationTests {

    @Test
    void contextLoads() {
        assertTrue(true, "Application context baseline test passed");
    }
}
""")

print("Backend SPI interfaces and Health controller created.")
