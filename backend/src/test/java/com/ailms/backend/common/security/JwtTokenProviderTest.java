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
