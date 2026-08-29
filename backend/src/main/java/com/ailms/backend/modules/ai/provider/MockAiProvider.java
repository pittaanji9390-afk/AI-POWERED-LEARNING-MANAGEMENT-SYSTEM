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
