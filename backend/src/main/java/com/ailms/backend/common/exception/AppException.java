package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class AppException extends RuntimeException {
    private final HttpStatus status;
    private final ErrorCode code;

    public AppException(String message, HttpStatus status, ErrorCode code) {
        super(message);
        this.status = status;
        this.code = code;
    }

    public AppException(String message, Throwable cause, HttpStatus status, ErrorCode code) {
        super(message, cause);
        this.status = status;
        this.code = code;
    }

    public HttpStatus getStatus() { return status; }
    public ErrorCode getCode() { return code; }
}
