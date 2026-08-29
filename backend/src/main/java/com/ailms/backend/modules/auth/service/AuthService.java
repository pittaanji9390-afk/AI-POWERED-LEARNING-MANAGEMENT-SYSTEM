package com.ailms.backend.modules.auth.service;

import com.ailms.backend.common.exception.ConflictException;
import com.ailms.backend.common.exception.UnauthorizedException;
import com.ailms.backend.common.security.JwtTokenProvider;
import com.ailms.backend.common.security.UserRole;
import com.ailms.backend.modules.auth.dto.AuthDtos.*;
import com.ailms.backend.modules.user.model.User;
import com.ailms.backend.modules.user.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Set;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtTokenProvider jwtTokenProvider) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Transactional
    public TokenResponse register(RegisterRequest req) {
        if (userRepository.existsByEmail(req.email())) {
            throw new ConflictException("User with email " + req.email() + " already exists");
        }

        User user = new User();
        user.setEmail(req.email().toLowerCase().trim());
        user.setPasswordHash(passwordEncoder.encode(req.password()));
        user.setFirstName(req.firstName());
        user.setLastName(req.lastName());
        user.setOrganizationId(req.organizationId());
        user.setRoles(Set.of("STUDENT"));
        user.setPermissions(Set.of("course:read", "ai:tutor:access"));

        user = userRepository.save(user);

        UserRole role = UserRole.STUDENT;
        String accessToken = jwtTokenProvider.generateAccessToken(user.getId(), user.getEmail(), user.getOrganizationId(), role, user.getPermissions());
        String refreshToken = jwtTokenProvider.generateRefreshToken(user.getId());

        UserDto userDto = new UserDto(user.getId(), user.getEmail(), user.getFirstName(), user.getLastName(), role.name(), user.getOrganizationId(), user.getPermissions());
        return new TokenResponse(accessToken, refreshToken, "Bearer", 900, userDto);
    }

    @Transactional
    public TokenResponse login(LoginRequest req) {
        User user = userRepository.findByEmail(req.email().toLowerCase().trim())
                .orElseThrow(() -> new UnauthorizedException("Invalid email or password credentials"));

        if (!passwordEncoder.matches(req.password(), user.getPasswordHash())) {
            throw new UnauthorizedException("Invalid email or password credentials");
        }

        user.setLastLoginAt(Instant.now());
        userRepository.save(user);

        String roleStr = user.getRoles().stream().findFirst().orElse("STUDENT");
        UserRole role = UserRole.valueOf(roleStr);

        String accessToken = jwtTokenProvider.generateAccessToken(user.getId(), user.getEmail(), user.getOrganizationId(), role, user.getPermissions());
        String refreshToken = jwtTokenProvider.generateRefreshToken(user.getId());

        UserDto userDto = new UserDto(user.getId(), user.getEmail(), user.getFirstName(), user.getLastName(), role.name(), user.getOrganizationId(), user.getPermissions());
        return new TokenResponse(accessToken, refreshToken, "Bearer", 900, userDto);
    }
}
