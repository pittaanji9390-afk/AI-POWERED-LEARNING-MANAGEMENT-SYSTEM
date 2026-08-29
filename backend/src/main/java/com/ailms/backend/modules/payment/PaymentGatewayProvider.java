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
