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
