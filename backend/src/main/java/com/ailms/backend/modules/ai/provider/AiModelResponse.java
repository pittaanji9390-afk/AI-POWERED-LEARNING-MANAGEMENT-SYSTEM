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
