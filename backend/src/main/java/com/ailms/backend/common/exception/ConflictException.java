package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class ConflictException extends AppException {
    public ConflictException(String message) {
        super(message, HttpStatus.CONFLICT, ErrorCode.CONFLICT);
    }
}
