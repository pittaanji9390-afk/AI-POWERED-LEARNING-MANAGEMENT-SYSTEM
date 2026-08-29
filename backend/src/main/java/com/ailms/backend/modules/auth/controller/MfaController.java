package com.ailms.backend.modules.auth.controller;

import com.ailms.backend.common.api.ApiResponse;
import com.ailms.backend.common.security.CurrentUser;
import com.ailms.backend.common.security.UserPrincipal;
import com.ailms.backend.modules.auth.service.MfaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/auth/mfa")
@Tag(name = "MFA Security", description = "Multi-factor TOTP configuration and verification")
public class MfaController {

    private final MfaService mfaService;

    public MfaController(MfaService mfaService) {
        this.mfaService = mfaService;
    }

    public record MfaSetupResponse(String secretKey, String qrCodeUri, List<String> recoveryCodes) {}
    public record MfaVerifyRequest(String secretKey, int totpCode) {}

    @PostMapping("/setup")
    @Operation(summary = "Initialize TOTP 2FA secret and recovery codes")
    public ResponseEntity<ApiResponse<MfaSetupResponse>> setupMfa(@CurrentUser UserPrincipal user) {
        String secret = mfaService.generateMfaSecret();
        List<String> recoveryCodes = mfaService.generateRecoveryCodes(8);
        String qrUri = "otpauth://totp/AegisLMS:" + user.getUsername() + "?secret=" + secret + "&issuer=AegisLMS";
        return ResponseEntity.ok(ApiResponse.success("MFA initialized", new MfaSetupResponse(secret, qrUri, recoveryCodes)));
    }

    @PostMapping("/verify")
    @Operation(summary = "Verify TOTP code and activate MFA on account")
    public ResponseEntity<ApiResponse<Boolean>> verifyMfa(
            @CurrentUser UserPrincipal user,
            @RequestBody MfaVerifyRequest request) {
        boolean valid = mfaService.verifyTotpCode(request.secretKey(), request.totpCode());
        return ResponseEntity.ok(ApiResponse.success(valid ? "MFA verified and activated" : "Invalid TOTP verification code", valid));
    }
}
