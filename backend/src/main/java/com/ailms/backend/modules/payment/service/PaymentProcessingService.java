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
