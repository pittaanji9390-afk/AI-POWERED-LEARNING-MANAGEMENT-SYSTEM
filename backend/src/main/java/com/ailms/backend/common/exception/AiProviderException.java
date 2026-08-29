package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class AiProviderException extends AppException {
    public AiProviderException(String message, Throwable cause) {
        super(message, cause, HttpStatus.SERVICE_UNAVAILABLE, ErrorCode.AI_PROVIDER_ERROR);
    }

    public AiProviderException(String message) {
        super(message, HttpStatus.SERVICE_UNAVAILABLE, ErrorCode.AI_PROVIDER_ERROR);
    }
}
