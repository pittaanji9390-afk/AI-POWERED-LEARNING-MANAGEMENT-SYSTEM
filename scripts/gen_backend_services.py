import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# Repositories
write("backend/src/main/java/com/ailms/backend/modules/user/repository/UserRepository.java", """
package com.ailms.backend.modules.user.repository;

import com.ailms.backend.modules.user.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserRepository extends JpaRepository<User, UUID> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/organization/repository/OrganizationRepository.java", """
package com.ailms.backend.modules.organization.repository;

import com.ailms.backend.modules.organization.model.Organization;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface OrganizationRepository extends JpaRepository<Organization, UUID> {
    Optional<Organization> findBySlug(String slug);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/course/repository/CourseRepository.java", """
package com.ailms.backend.modules.course.repository;

import com.ailms.backend.modules.course.model.Course;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CourseRepository extends JpaRepository<Course, UUID> {
    Optional<Course> findBySlug(String slug);
    Page<Course> findByStatusAndIsPublicTrue(String status, Pageable pageable);
    Page<Course> findByOrganizationId(UUID organizationId, Pageable pageable);
}
""")

write("backend/src/main/java/com/ailms/backend/modules/enrollment/repository/EnrollmentRepository.java", """
package com.ailms.backend.modules.enrollment.repository;

import com.ailms.backend.modules.enrollment.model.Enrollment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface EnrollmentRepository extends JpaRepository<Enrollment, UUID> {
    Optional<Enrollment> findByUserIdAndCourseId(UUID userId, UUID courseId);
    List<Enrollment> findByUserId(UUID userId);
    boolean existsByUserIdAndCourseId(UUID userId, UUID courseId);
}
""")

# DTOs
write("backend/src/main/java/com/ailms/backend/modules/auth/dto/AuthDtos.java", """
package com.ailms.backend.modules.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.util.Set;
import java.util.UUID;

public class AuthDtos {

    public record LoginRequest(
            @NotBlank @Email String email,
            @NotBlank String password
    ) {}

    public record RegisterRequest(
            @NotBlank @Email String email,
            @NotBlank @Size(min = 8, message = "Password must be at least 8 characters") String password,
            @NotBlank String firstName,
            @NotBlank String lastName,
            UUID organizationId
    ) {}

    public record TokenResponse(
            String accessToken,
            String refreshToken,
            String tokenType,
            long expiresInSeconds,
            UserDto user
    ) {}

    public record UserDto(
            UUID id,
            String email,
            String firstName,
            String lastName,
            String role,
            UUID organizationId,
            Set<String> permissions
    ) {}
}
""")

write("backend/src/main/java/com/ailms/backend/modules/course/dto/CourseDtos.java", """
package com.ailms.backend.modules.course.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

public class CourseDtos {

    public record CreateCourseRequest(
            @NotBlank String title,
            @NotBlank String slug,
            String shortDescription,
            String description,
            String thumbnailUrl,
            @NotBlank String category,
            String difficulty,
            BigDecimal price,
            String currency,
            Boolean isPublic
    ) {}

    public record CourseSummaryDto(
            UUID id,
            String title,
            String slug,
            String shortDescription,
            String category,
            String difficulty,
            BigDecimal price,
            String currency,
            String status,
            UUID instructorId
    ) {}
}
""")

# Auth Service & Controller
write("backend/src/main/java/com/ailms/backend/modules/auth/service/AuthService.java", """
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
""")

write("backend/src/main/java/com/ailms/backend/modules/auth/controller/AuthController.java", """
package com.ailms.backend.modules.auth.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.modules.auth.dto.AuthDtos.*;
import com.ailms.backend.modules.auth.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auth")
@Tag(name = "Authentication", description = "Authentication and token lifecycle endpoints")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    @Operation(summary = "Register new learner account")
    public ResponseEntity<ApiResponse<TokenResponse>> register(@Valid @RequestBody RegisterRequest request) {
        TokenResponse response = authService.register(request);
        return ResponseEntity.ok(ApiResponse.created(response));
    }

    @PostMapping("/login")
    @Operation(summary = "Authenticate user with email and password")
    public ResponseEntity<ApiResponse<TokenResponse>> login(@Valid @RequestBody LoginRequest request) {
        TokenResponse response = authService.login(request);
        return ResponseEntity.ok(ApiResponse.success("Authentication successful", response));
    }
}
""")

# Course Service & Controller
write("backend/src/main/java/com/ailms/backend/modules/course/service/CourseService.java", """
package com.ailms.backend.modules.course.service;

import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.course.dto.CourseDtos.*;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
public class CourseService {

    private final CourseRepository courseRepository;

    public CourseService(CourseRepository courseRepository) {
        this.courseRepository = courseRepository;
    }

    @Transactional(readOnly = true)
    public Page<CourseSummaryDto> getPublicCatalog(Pageable pageable) {
        return courseRepository.findByStatusAndIsPublicTrue("PUBLISHED", pageable)
                .map(c -> new CourseSummaryDto(
                        c.getId(), c.getTitle(), c.getSlug(), c.getShortDescription(),
                        c.getCategory(), c.getDifficulty(), c.getPrice(), c.getCurrency(),
                        c.getStatus(), c.getInstructorId()));
    }

    @Transactional(readOnly = true)
    public Course getCourseById(UUID id) {
        return courseRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Course", "id", id));
    }

    @Transactional
    public Course createCourse(UUID instructorId, UUID orgId, CreateCourseRequest req) {
        Course course = new Course();
        course.setInstructorId(instructorId);
        course.setOrganizationId(orgId);
        course.setTitle(req.title());
        course.setSlug(req.slug());
        course.setShortDescription(req.shortDescription());
        course.setDescription(req.description());
        course.setThumbnailUrl(req.thumbnailUrl());
        course.setCategory(req.category());
        course.setDifficulty(req.difficulty() != null ? req.difficulty() : "BEGINNER");
        course.setPrice(req.price());
        course.setCurrency(req.currency() != null ? req.currency() : "USD");
        course.setIsPublic(req.isPublic() != null ? req.isPublic() : true);
        course.setStatus("DRAFT");

        return courseRepository.save(course);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/modules/course/controller/CourseController.java", """
package com.ailms.backend.modules.course.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.common.api.PageResponse;
import com.ailms.backend.common.security.CurrentUser;
import com.ailms.backend.common.security.UserPrincipal;
import com.ailms.backend.modules.course.dto.CourseDtos.*;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.service.CourseService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/courses")
@Tag(name = "Courses", description = "Course catalog, creation, and curriculum management")
public class CourseController {

    private final CourseService courseService;

    public CourseController(CourseService courseService) {
        this.courseService = courseService;
    }

    @GetMapping("/catalog")
    @Operation(summary = "Browse published public courses")
    public ResponseEntity<ApiResponse<PageResponse<CourseSummaryDto>>> getCatalog(Pageable pageable) {
        return ResponseEntity.ok(ApiResponse.success(new PageResponse<>(courseService.getPublicCatalog(pageable))));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get course details by ID")
    public ResponseEntity<ApiResponse<Course>> getCourse(@PathVariable UUID id) {
        return ResponseEntity.ok(ApiResponse.success(courseService.getCourseById(id)));
    }

    @PostMapping
    @PreAuthorize("hasAuthority('course:create') or hasRole('TEACHER') or hasRole('SUPER_ADMIN')")
    @Operation(summary = "Create a new course draft")
    public ResponseEntity<ApiResponse<Course>> createCourse(
            @CurrentUser UserPrincipal user,
            @Valid @RequestBody CreateCourseRequest request) {
        Course course = courseService.createCourse(user.getId(), user.getOrganizationId(), request);
        return ResponseEntity.ok(ApiResponse.created(course));
    }
}
""")

# AI Tutor & Generation Service & Controller
write("backend/src/main/java/com/ailms/backend/modules/ai/service/AiTutorService.java", """
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
""")

write("backend/src/main/java/com/ailms/backend/modules/ai/controller/AiController.java", """
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
""")

print("Repositories, DTOs, Services, and REST Controllers generated.")
