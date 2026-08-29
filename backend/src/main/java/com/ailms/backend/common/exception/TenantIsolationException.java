package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class TenantIsolationException extends AppException {
    public TenantIsolationException(String message) {
        super(message, HttpStatus.FORBIDDEN, ErrorCode.TENANT_ACCESS_DENIED);
    }
}
