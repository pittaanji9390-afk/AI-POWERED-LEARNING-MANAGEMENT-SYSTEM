package com.ailms.backend.modules.auth.controller;

import com.ailms.backend.common.api.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/health")
@Tag(name = "System Health", description = "System probe & health status endpoints")
public class HealthController {

    @GetMapping
    @Operation(summary = "System status check")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getHealth() {
        Map<String, Object> healthInfo = Map.of(
                "status", "UP",
                "service", "ai-lms-backend",
                "version", "1.0.0",
                "timestamp", Instant.now().toString(),
                "aiOrchestration", "READY"
        );
        return ResponseEntity.ok(ApiResponse.success("System is operational", healthInfo));
    }
}
