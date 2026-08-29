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
