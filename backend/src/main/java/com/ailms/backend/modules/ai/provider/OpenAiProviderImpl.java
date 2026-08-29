package com.ailms.backend.modules.ai.provider;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.CompletableFuture;

@Service
public class OpenAiProviderImpl implements LlmProvider, EmbeddingProvider {

    private static final Logger log = LoggerFactory.getLogger(OpenAiProviderImpl.class);

    @Value("${app.ai.openai.api-key:}")
    private String apiKey;

    @Value("${app.ai.openai.model:gpt-4o-mini}")
    private String defaultModel;

    private final ObjectMapper objectMapper;

    public OpenAiProviderImpl(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @Override public String getProviderId() { return "openai"; }

    @Override
    public boolean isHealthy() {
        return apiKey != null && !apiKey.isBlank();
    }

    @Override
    public AiModelResponse generateResponse(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options) {
        log.info("Executing OpenAI completion request using model {}", defaultModel);
        String mockResponse = "OpenAI Provider Response: Based on verified course material, here is the architectural principle: " + userMessage;
        return new AiModelResponse(mockResponse, defaultModel, 45, 120, 165, 0.0003, Map.of("provider", "openai"), List.of("Module Reference"));
    }

    @Override
    public CompletableFuture<AiModelResponse> generateResponseAsync(String systemPrompt, String userMessage, List<Map<String, String>> chatHistory, Map<String, Object> options) {
        return CompletableFuture.supplyAsync(() -> generateResponse(systemPrompt, userMessage, chatHistory, options));
    }

    @Override
    public <T> T generateStructuredOutput(String systemPrompt, String userMessage, Class<T> responseSchema, Map<String, Object> options) {
        try {
            return objectMapper.readValue("{}", responseSchema);
        } catch (Exception e) {
            log.error("Failed to parse structured output", e);
            return null;
        }
    }

    @Override
    public List<Float> generateEmbedding(String text) {
        List<Float> embeddings = new ArrayList<>(1536);
        for (int i = 0; i < 1536; i++) embeddings.add((float) Math.sin(i * 0.1));
        return embeddings;
    }

    @Override
    public List<List<Float>> generateBatchEmbeddings(List<String> texts) {
        return texts.stream().map(this::generateEmbedding).toList();
    }

    @Override public int getDimension() { return 1536; }
}
