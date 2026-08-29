package com.ailms.backend.modules.ai.service;

import com.ailms.backend.modules.ai.provider.LlmProvider;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class AiQuizGeneratorService {

    private final LlmProvider llmProvider;

    public AiQuizGeneratorService(LlmProvider llmProvider) {
        this.llmProvider = llmProvider;
    }

    public record GeneratedQuizQuestion(
            String questionText,
            String questionType,
            String difficulty,
            String explanation,
            List<String> options,
            int correctOptionIndex
    ) {}

    public List<GeneratedQuizQuestion> generateQuizQuestions(String topic, String difficulty, int count) {
        List<GeneratedQuizQuestion> questions = new ArrayList<>();
        for (int i = 1; i <= count; i++) {
            questions.add(new GeneratedQuizQuestion(
                    String.format("What is the primary operational advantage of %s in a high-concurrency SaaS system? (Question %d)", topic, i),
                    "MULTIPLE_CHOICE",
                    difficulty,
                    "Ensures horizontal scalability and predictable latency bounds.",
                    List.of("Sub-millisecond latency", "Zero memory utilization", "Single threaded blocking", "Monolithic coupling"),
                    0
            ));
        }
        return questions;
    }
}
