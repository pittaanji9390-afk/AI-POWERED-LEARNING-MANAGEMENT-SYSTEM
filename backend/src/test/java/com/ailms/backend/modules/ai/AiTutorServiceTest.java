package com.ailms.backend.modules.ai;

import com.ailms.backend.modules.ai.provider.AiModelResponse;
import com.ailms.backend.modules.ai.provider.LlmProvider;
import com.ailms.backend.modules.ai.service.AiTutorService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AiTutorServiceTest {

    @Mock
    private LlmProvider llmProvider;

    private AiTutorService aiTutorService;

    @BeforeEach
    void setUp() {
        aiTutorService = new AiTutorService(llmProvider);
    }

    @Test
    void askTutor_ShouldCallLlmWithSocraticPrompt() {
        UUID courseId = UUID.randomUUID();
        String question = "How does database indexing work?";
        List<Map<String, String>> history = new ArrayList<>();

        AiModelResponse mockResponse = new AiModelResponse(
                "Indexes use B-trees to speed up lookups.", "mock-model", 10, 20, 30, 0.0, Map.of(), List.of("Chapter 4")
        );

        when(llmProvider.generateResponse(anyString(), eq(question), eq(history), anyMap()))
                .thenReturn(mockResponse);

        AiModelResponse response = aiTutorService.askTutor(courseId, question, history);

        assertNotNull(response);
        assertEquals("Indexes use B-trees to speed up lookups.", response.content());
        assertEquals(1, response.citations().size());
        verify(llmProvider, times(1)).generateResponse(anyString(), eq(question), eq(history), anyMap());
    }
}
