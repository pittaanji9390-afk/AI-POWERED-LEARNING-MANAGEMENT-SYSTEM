import os

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# BaseEntity
write("backend/src/main/java/com/ailms/backend/common/domain/BaseEntity.java", """
package com.ailms.backend.common.domain;

import jakarta.persistence.*;
import java.io.Serializable;
import java.util.Objects;
import java.util.UUID;

@MappedSuperclass
public abstract class BaseEntity implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    @Version
    @Column(name = "version")
    private Long version;

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public Long getVersion() { return version; }
    public void setVersion(Long version) { this.version = version; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        BaseEntity that = (BaseEntity) o;
        return id != null && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
""")

# AuditableEntity
write("backend/src/main/java/com/ailms/backend/common/domain/AuditableEntity.java", """
package com.ailms.backend.common.domain;

import jakarta.persistence.Column;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.MappedSuperclass;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedBy;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;
import java.util.UUID;

@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class AuditableEntity extends BaseEntity {

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt = Instant.now();

    @CreatedBy
    @Column(name = "created_by")
    private UUID createdBy;

    @LastModifiedBy
    @Column(name = "updated_by")
    private UUID updatedBy;

    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }

    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }

    public UUID getCreatedBy() { return createdBy; }
    public void setCreatedBy(UUID createdBy) { this.createdBy = createdBy; }

    public UUID getUpdatedBy() { return updatedBy; }
    public void setUpdatedBy(UUID updatedBy) { this.updatedBy = updatedBy; }
}
""")

# TenantAwareEntity
write("backend/src/main/java/com/ailms/backend/common/domain/TenantAwareEntity.java", """
package com.ailms.backend.common.domain;

import jakarta.persistence.Column;
import jakarta.persistence.MappedSuperclass;
import java.util.UUID;

@MappedSuperclass
public abstract class TenantAwareEntity extends AuditableEntity {

    @Column(name = "organization_id")
    private UUID organizationId;

    public UUID getOrganizationId() { return organizationId; }
    public void setOrganizationId(UUID organizationId) { this.organizationId = organizationId; }
}
""")

# UserRole
write("backend/src/main/java/com/ailms/backend/common/security/UserRole.java", """
package com.ailms.backend.common.security;

public enum UserRole {
    SUPER_ADMIN,
    PLATFORM_ADMIN,
    ORGANIZATION_ADMIN,
    TEACHER,
    TEACHING_ASSISTANT,
    STUDENT,
    MODERATOR,
    SUPPORT_AGENT
}
""")

# Permission
write("backend/src/main/java/com/ailms/backend/common/security/Permission.java", """
package com.ailms.backend.common.security;

public enum Permission {
    COURSE_CREATE("course:create"),
    COURSE_READ("course:read"),
    COURSE_UPDATE("course:update"),
    COURSE_DELETE("course:delete"),
    COURSE_PUBLISH("course:publish"),
    CONTENT_MANAGE("content:manage"),
    MEDIA_UPLOAD("media:upload"),
    ENROLLMENT_MANAGE("enrollment:manage"),
    PROGRESS_VIEW_ALL("progress:view:all"),
    ASSESSMENT_CREATE("assessment:create"),
    ASSESSMENT_GRADE("assessment:grade"),
    GRADE_OVERRIDE("grade:override"),
    AI_TUTOR_ACCESS("ai:tutor:access"),
    AI_GENERATE_QUIZ("ai:quiz:generate"),
    AI_GENERATE_CONTENT("ai:content:generate"),
    AI_ASSISTED_GRADING("ai:grading:assist"),
    USER_MANAGE("user:manage"),
    ORGANIZATION_MANAGE("organization:manage"),
    MODERATION_MANAGE("moderation:manage"),
    PAYMENT_MANAGE("payment:manage"),
    AUDIT_VIEW("audit:view"),
    SYSTEM_CONFIG("system:config");

    private final String value;
    Permission(String value) { this.value = value; }
    public String getValue() { return value; }
}
""")

# TenantContext
write("backend/src/main/java/com/ailms/backend/common/security/TenantContext.java", """
package com.ailms.backend.common.security;

import java.util.UUID;

public final class TenantContext {
    private static final ThreadLocal<UUID> CURRENT_TENANT = new ThreadLocal<>();
    private TenantContext() {}
    public static void setTenantId(UUID tenantId) { CURRENT_TENANT.set(tenantId); }
    public static UUID getTenantId() { return CURRENT_TENANT.get(); }
    public static void clear() { CURRENT_TENANT.remove(); }
}
""")

# UserPrincipal
write("backend/src/main/java/com/ailms/backend/common/security/UserPrincipal.java", """
package com.ailms.backend.common.security;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

public class UserPrincipal implements UserDetails {

    private final UUID id;
    private final String email;
    private final String password;
    private final UUID organizationId;
    private final UserRole role;
    private final Set<GrantedAuthority> authorities;
    private final boolean active;

    public UserPrincipal(UUID id, String email, String password, UUID organizationId, UserRole role, Set<String> permissions, boolean active) {
        this.id = id;
        this.email = email;
        this.password = password;
        this.organizationId = organizationId;
        this.role = role;
        this.active = active;

        Set<GrantedAuthority> auths = permissions.stream()
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toSet());
        auths.add(new SimpleGrantedAuthority("ROLE_" + role.name()));
        this.authorities = auths;
    }

    public UUID getId() { return id; }
    public UUID getOrganizationId() { return organizationId; }
    public UserRole getRole() { return role; }

    @Override public Collection<? extends GrantedAuthority> getAuthorities() { return authorities; }
    @Override public String getPassword() { return password; }
    @Override public String getUsername() { return email; }
    @Override public boolean isAccountNonExpired() { return true; }
    @Override public boolean isAccountNonLocked() { return active; }
    @Override public boolean isCredentialsNonExpired() { return true; }
    @Override public boolean isEnabled() { return active; }
}
""")

# CurrentUser
write("backend/src/main/java/com/ailms/backend/common/security/CurrentUser.java", """
package com.ailms.backend.common.security;

import org.springframework.security.core.annotation.AuthenticationPrincipal;
import java.lang.annotation.*;

@Target({ElementType.PARAMETER, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@AuthenticationPrincipal
public @interface CurrentUser {
}
""")

# SecurityUtils
write("backend/src/main/java/com/ailms/backend/common/security/SecurityUtils.java", """
package com.ailms.backend.common.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.Optional;
import java.util.UUID;

public final class SecurityUtils {
    private SecurityUtils() {}
    public static Optional<UserPrincipal> getCurrentUserPrincipal() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof UserPrincipal principal) {
            return Optional.of(principal);
        }
        return Optional.empty();
    }
    public static Optional<UUID> getCurrentUserId() {
        return getCurrentUserPrincipal().map(UserPrincipal::getId);
    }
    public static Optional<UUID> getCurrentUserOrgId() {
        return getCurrentUserPrincipal().map(UserPrincipal::getOrganizationId);
    }
}
""")

# JwtTokenProvider
write("backend/src/main/java/com/ailms/backend/common/security/JwtTokenProvider.java", """
package com.ailms.backend.common.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Component
public class JwtTokenProvider {

    private static final Logger log = LoggerFactory.getLogger(JwtTokenProvider.class);

    private final SecretKey key;
    private final long accessTokenExpirationMs;
    private final long refreshTokenExpirationMs;
    private final String issuer;

    public JwtTokenProvider(
            @Value("${app.jwt.secret:enterprise-lms-jwt-secret-key-must-be-at-least-256-bits-long-for-hmac-sha-256-production-use}") String secret,
            @Value("${app.jwt.access-token-expiration-ms:900000}") long accessTokenExpirationMs,
            @Value("${app.jwt.refresh-token-expiration-ms:604800000}") long refreshTokenExpirationMs,
            @Value("${app.jwt.issuer:ai-lms-platform}") String issuer) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.accessTokenExpirationMs = accessTokenExpirationMs;
        this.refreshTokenExpirationMs = refreshTokenExpirationMs;
        this.issuer = issuer;
    }

    public String generateAccessToken(UUID userId, String email, UUID orgId, UserRole role, Set<String> permissions) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + accessTokenExpirationMs);

        return Jwts.builder()
                .issuer(issuer)
                .subject(userId.toString())
                .claim("email", email)
                .claim("orgId", orgId != null ? orgId.toString() : null)
                .claim("role", role.name())
                .claim("permissions", permissions)
                .issuedAt(now)
                .expiration(expiryDate)
                .signWith(key)
                .compact();
    }

    public String generateRefreshToken(UUID userId) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + refreshTokenExpirationMs);

        return Jwts.builder()
                .issuer(issuer)
                .subject(userId.toString())
                .claim("type", "REFRESH")
                .issuedAt(now)
                .expiration(expiryDate)
                .signWith(key)
                .compact();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().verifyWith(key).build().parseSignedClaims(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            log.warn("Invalid JWT token: {}", e.getMessage());
            return false;
        }
    }

    public Claims getClaims(String token) {
        return Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload();
    }
}
""")

# JwtAuthenticationFilter
write("backend/src/main/java/com/ailms/backend/common/security/JwtAuthenticationFilter.java", """
package com.ailms.backend.common.security;

import io.jsonwebtoken.Claims;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.*;

@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(JwtAuthenticationFilter.class);
    private final JwtTokenProvider tokenProvider;

    public JwtAuthenticationFilter(JwtTokenProvider tokenProvider) {
        this.tokenProvider = tokenProvider;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        try {
            String jwt = getJwtFromRequest(request);

            if (StringUtils.hasText(jwt) && tokenProvider.validateToken(jwt)) {
                Claims claims = tokenProvider.getClaims(jwt);
                UUID userId = UUID.fromString(claims.getSubject());
                String email = claims.get("email", String.class);
                String orgIdStr = claims.get("orgId", String.class);
                UUID orgId = orgIdStr != null ? UUID.fromString(orgIdStr) : null;
                String roleStr = claims.get("role", String.class);
                UserRole role = roleStr != null ? UserRole.valueOf(roleStr) : UserRole.STUDENT;

                @SuppressWarnings("unchecked")
                List<String> permissions = claims.get("permissions", List.class);
                Set<String> permissionSet = permissions != null ? new HashSet<>(permissions) : Collections.emptySet();

                UserPrincipal principal = new UserPrincipal(userId, email, "", orgId, role, permissionSet, true);

                UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                        principal, null, principal.getAuthorities());
                auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                SecurityContextHolder.getContext().setAuthentication(auth);

                if (orgId != null) {
                    TenantContext.setTenantId(orgId);
                }
            }
            filterChain.doFilter(request, response);
        } finally {
            TenantContext.clear();
        }
    }

    private String getJwtFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}
""")

print("Backend security & domain classes created.")
