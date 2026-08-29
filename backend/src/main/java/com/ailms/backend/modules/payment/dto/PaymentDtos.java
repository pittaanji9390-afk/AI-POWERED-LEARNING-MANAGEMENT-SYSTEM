package com.ailms.backend.modules.payment.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.util.UUID;

public class PaymentDtos {

    public record CreateCheckoutRequest(
            @NotNull BigDecimal amount,
            String currency,
            @NotBlank String itemType,
            UUID itemId,
            String couponCode,
            String idempotencyKey
    ) {}

    public record CheckoutResponse(
            String sessionId,
            String checkoutUrl,
            String referenceId,
            BigDecimal originalAmount,
            BigDecimal discountedAmount,
            String currency
    ) {}

    public record ValidateCouponRequest(
            @NotBlank String code,
            UUID courseId
    ) {}

    public record CouponValidationResponse(
            boolean valid,
            String code,
            String discountType,
            BigDecimal discountValue,
            String message
    ) {}
}
