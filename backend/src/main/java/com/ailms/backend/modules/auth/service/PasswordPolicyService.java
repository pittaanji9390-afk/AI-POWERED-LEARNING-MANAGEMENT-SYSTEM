package com.ailms.backend.modules.auth.service;

import com.ailms.backend.common.exception.BadRequestException;
import org.springframework.stereotype.Service;

import java.util.Set;
import java.util.regex.Pattern;

@Service
public class PasswordPolicyService {

    private static final int MIN_LENGTH = 8;
    private static final int MAX_LENGTH = 128;
    private static final Pattern HAS_UPPERCASE = Pattern.compile("[A-Z]");
    private static final Pattern HAS_LOWERCASE = Pattern.compile("[a-z]");
    private static final Pattern HAS_DIGIT = Pattern.compile("[0-9]");
    private static final Pattern HAS_SPECIAL = Pattern.compile("[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]");

    private static final Set<String> COMMON_PASSWORDS = Set.of(
            "password", "password123", "admin123", "qwerty123", "letmein123", "welcome123"
    );

    public void validatePassword(String password) {
        if (password == null || password.length() < MIN_LENGTH || password.length() > MAX_LENGTH) {
            throw new BadRequestException(String.format("Password must be between %d and %d characters.", MIN_LENGTH, MAX_LENGTH));
        }
        if (!HAS_UPPERCASE.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one uppercase letter (A-Z).");
        }
        if (!HAS_LOWERCASE.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one lowercase letter (a-z).");
        }
        if (!HAS_DIGIT.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one numerical digit (0-9).");
        }
        if (!HAS_SPECIAL.matcher(password).find()) {
            throw new BadRequestException("Password must contain at least one special symbol.");
        }
        if (COMMON_PASSWORDS.contains(password.toLowerCase())) {
            throw new BadRequestException("Password is too common and easily guessed. Please choose a stronger password.");
        }
    }
}
