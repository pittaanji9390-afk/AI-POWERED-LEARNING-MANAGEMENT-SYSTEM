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
