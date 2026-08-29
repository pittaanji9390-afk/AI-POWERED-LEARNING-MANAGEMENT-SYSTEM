package com.ailms.backend.modules.ai.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.modules.ai.provider.AiModelResponse;
import com.ailms.backend.modules.ai.service.AiTutorService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/ai")
@Tag(name = "AI Orchestration", description = "AI Tutor, RAG query, Quiz generation and AI grading")
public class AiController {

    private final AiTutorService aiTutorService;

    public AiController(AiTutorService aiTutorService) {
        this.aiTutorService = aiTutorService;
    }

    public record TutorRequest(UUID courseId, String question, List<Map<String, String>> history) {}

    @PostMapping("/tutor/ask")
    @PreAuthorize("hasAuthority('ai:tutor:access') or hasRole('STUDENT') or hasRole('TEACHER')")
    @Operation(summary = "Query the AI Course Tutor with Socratic RAG")
    public ResponseEntity<ApiResponse<AiModelResponse>> askTutor(@RequestBody TutorRequest request) {
        AiModelResponse response = aiTutorService.askTutor(
                request.courseId(),
                request.question(),
                request.history() != null ? request.history() : List.of()
        );
        return ResponseEntity.ok(ApiResponse.success("AI Tutor response generated", response));
    }
}
