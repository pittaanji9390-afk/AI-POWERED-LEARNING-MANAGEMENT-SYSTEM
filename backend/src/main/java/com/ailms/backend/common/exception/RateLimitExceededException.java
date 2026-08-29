package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class RateLimitExceededException extends AppException {
    public RateLimitExceededException(String message) {
        super(message, HttpStatus.TOO_MANY_REQUESTS, ErrorCode.RATE_LIMIT_EXCEEDED);
    }
}
