import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# JwtTokenProviderTest.java
write("backend/src/test/java/com/ailms/backend/common/security/JwtTokenProviderTest.java", """
package com.ailms.backend.common.security;

import io.jsonwebtoken.Claims;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class JwtTokenProviderTest {

    private JwtTokenProvider jwtTokenProvider;
    private final String testSecret = "test-secret-key-must-be-at-least-256-bits-for-hmac-sha-256-testing-suite";

    @BeforeEach
    void setUp() {
        jwtTokenProvider = new JwtTokenProvider(testSecret, 900000, 604800000, "test-issuer");
    }

    @Test
    void shouldGenerateAndValidateAccessToken() {
        UUID userId = UUID.randomUUID();
        UUID orgId = UUID.randomUUID();
        String email = "learner@ailms.platform";
        UserRole role = UserRole.STUDENT;
        Set<String> permissions = Set.of("course:read", "ai:tutor:access");

        String token = jwtTokenProvider.generateAccessToken(userId, email, orgId, role, permissions);
        assertNotNull(token);
        assertTrue(jwtTokenProvider.validateToken(token));

        Claims claims = jwtTokenProvider.getClaims(token);
        assertEquals(userId.toString(), claims.getSubject());
        assertEquals(email, claims.get("email"));
        assertEquals(orgId.toString(), claims.get("orgId"));
        assertEquals("STUDENT", claims.get("role"));
    }

    @Test
    void shouldRejectInvalidToken() {
        assertFalse(jwtTokenProvider.validateToken("invalid.token.structure"));
    }
}
""")

# AuthServiceTest.java
write("backend/src/test/java/com/ailms/backend/modules/auth/AuthServiceTest.java", """
package com.ailms.backend.modules.auth;

import com.ailms.backend.common.exception.ConflictException;
import com.ailms.backend.common.security.JwtTokenProvider;
import com.ailms.backend.modules.auth.dto.AuthDtos.*;
import com.ailms.backend.modules.auth.service.AuthService;
import com.ailms.backend.modules.user.model.User;
import com.ailms.backend.modules.user.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtTokenProvider jwtTokenProvider;

    private AuthService authService;

    @BeforeEach
    void setUp() {
        authService = new AuthService(userRepository, passwordEncoder, jwtTokenProvider);
    }

    @Test
    void register_ShouldSaveUserAndReturnTokens() {
        RegisterRequest req = new RegisterRequest("new.user@ailms.com", "Password@123", "New", "User", null);

        when(userRepository.existsByEmail("new.user@ailms.com")).thenReturn(false);
        when(passwordEncoder.encode(any())).thenReturn("hashed_pw");

        User savedUser = new User();
        savedUser.setId(UUID.randomUUID());
        savedUser.setEmail(req.email());
        savedUser.setFirstName(req.firstName());
        savedUser.setLastName(req.lastName());

        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        when(jwtTokenProvider.generateAccessToken(any(), any(), any(), any(), any())).thenReturn("mock_jwt");
        when(jwtTokenProvider.generateRefreshToken(any())).thenReturn("mock_refresh");

        TokenResponse res = authService.register(req);

        assertNotNull(res);
        assertEquals("mock_jwt", res.accessToken());
        assertEquals("mock_refresh", res.refreshToken());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    void register_ShouldThrowWhenEmailExists() {
        RegisterRequest req = new RegisterRequest("existing@ailms.com", "Password@123", "Exist", "User", null);
        when(userRepository.existsByEmail("existing@ailms.com")).thenReturn(true);

        assertThrows(ConflictException.class, () -> authService.register(req));
    }
}
""")

# AiTutorServiceTest.java
write("backend/src/test/java/com/ailms/backend/modules/ai/AiTutorServiceTest.java", """
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
""")

print("Automated test suites generated successfully.")
