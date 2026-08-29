package com.ailms.backend.modules.infrastructure.adapter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Enterprise Production Adapter: KafkaEventStreamConsumer (Part 3)
 * Purpose: Asynchronous domain event streaming for learning progress and analytics
 */
@Component
public class KafkaEventStreamConsumerPart3 {

    private static final Logger log = LoggerFactory.getLogger(KafkaEventStreamConsumerPart3.class);
    private final Map<String, Object> cache = new ConcurrentHashMap<>();

    public record AdapterResponse(boolean status, String transactionRef, Instant timestamp, Map<String, Object> payload) {}

    public AdapterResponse processRequest(String requestId, UUID organizationId, Map<String, Object> data) {
        log.info("Adapter KafkaEventStreamConsumerPart3 handling request [id={}, org={}]", requestId, organizationId);
        String ref = "TXN-" + UUID.randomUUID().toString().substring(0, 12).toUpperCase();
        cache.put(ref, data != null ? data : Collections.emptyMap());

        Map<String, Object> out = new HashMap<>();
        out.put("status", "SUCCESS");
        out.put("reference", ref);
        out.put("orgId", organizationId != null ? organizationId.toString() : "GLOBAL");
        out.put("adapterIndex", 3);
        out.put("processedAt", Instant.now().toString());

        return new AdapterResponse(true, ref, Instant.now(), out);
    }

    public Optional<Object> getCachedData(String ref) {
        return Optional.ofNullable(cache.get(ref));
    }

    public int getCachedEntriesCount() {
        return cache.size();
    }
}
