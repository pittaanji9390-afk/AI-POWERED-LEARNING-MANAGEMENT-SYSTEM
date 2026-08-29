package com.ailms.backend.modules.ai.provider;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

public interface LlmProvider extends AiProvider {
    AiModelResponse generateResponse(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options);
    CompletableFuture<AiModelResponse> generateResponseAsync(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options);
    <T> T generateStructuredOutput(String systemPrompt, String userMessage, Class<T> responseSchema, Map<String, Object> options);
}
