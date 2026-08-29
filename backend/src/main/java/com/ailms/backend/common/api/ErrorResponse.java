package com.ailms.backend.common.api;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.Instant;
import java.util.List;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {
    private final Instant timestamp;
    private final String requestId;
    private final int status;
    private final ErrorCode code;
    private final String message;
    private final List<FieldErrorDetail> fieldErrors;

    public ErrorResponse(int status, ErrorCode code, String message, String requestId, List<FieldErrorDetail> fieldErrors) {
        this.timestamp = Instant.now();
        this.requestId = requestId;
        this.status = status;
        this.code = code;
        this.message = message;
        this.fieldErrors = fieldErrors;
    }

    public static ErrorResponse of(int status, ErrorCode code, String message, String requestId) {
        return new ErrorResponse(status, code, message, requestId, null);
    }

    public static ErrorResponse ofValidation(int status, String message, String requestId, List<FieldErrorDetail> fieldErrors) {
        return new ErrorResponse(status, ErrorCode.VALIDATION_ERROR, message, requestId, fieldErrors);
    }

    public Instant getTimestamp() { return timestamp; }
    public String getRequestId() { return requestId; }
    public int getStatus() { return status; }
    public ErrorCode getCode() { return code; }
    public String getMessage() { return message; }
    public List<FieldErrorDetail> getFieldErrors() { return fieldErrors; }
}
