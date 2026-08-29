package com.ailms.backend.modules.ai.service;

import com.ailms.backend.modules.ai.provider.AiModelResponse;
import com.ailms.backend.modules.ai.provider.LlmProvider;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class AiTutorService {

    private final LlmProvider llmProvider;

    public AiTutorService(LlmProvider llmProvider) {
        this.llmProvider = llmProvider;
    }

    public AiModelResponse askTutor(UUID courseId, String studentQuestion, List<Map<String, String>> history) {
        String systemPrompt = "You are Aegis AI Tutor. Answer student questions using Socratic teaching principles. "
                + "Context: Enrolled in Course ID " + courseId + ". Provide concise, helpful explanations.";
        
        return llmProvider.generateResponse(systemPrompt, studentQuestion, history, Map.of("temperature", 0.3));
    }
}
