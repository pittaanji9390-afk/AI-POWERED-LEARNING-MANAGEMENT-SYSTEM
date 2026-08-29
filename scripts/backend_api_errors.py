import os

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# ApiResponse
write("backend/src/main/java/com/ailms/backend/common/api/ApiResponse.java", """
package com.ailms.backend.common.api;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.Instant;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {
    private final boolean success;
    private final String message;
    private final T data;
    private final Instant timestamp;
    private final String requestId;

    private ApiResponse(boolean success, String message, T data, String requestId) {
        this.success = success;
        this.message = message;
        this.data = data;
        this.timestamp = Instant.now();
        this.requestId = requestId;
    }

    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(true, "Operation successful", data, null);
    }

    public static <T> ApiResponse<T> success(String message, T data) {
        return new ApiResponse<>(true, message, data, null);
    }

    public static <T> ApiResponse<T> success(String message, T data, String requestId) {
        return new ApiResponse<>(true, message, data, requestId);
    }

    public static <T> ApiResponse<T> created(T data) {
        return new ApiResponse<>(true, "Resource created successfully", data, null);
    }

    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
    public T getData() { return data; }
    public Instant getTimestamp() { return timestamp; }
    public String getRequestId() { return requestId; }
}
""")

# PageResponse
write("backend/src/main/java/com/ailms/backend/common/api/PageResponse.java", """
package com.ailms.backend.common.api;

import org.springframework.data.domain.Page;
import java.util.List;

public class PageResponse<T> {
    private final List<T> items;
    private final int pageNumber;
    private final int pageSize;
    private final long totalElements;
    private final int totalPages;
    private final boolean isFirst;
    private final boolean isLast;

    public PageResponse(Page<T> page) {
        this.items = page.getContent();
        this.pageNumber = page.getNumber();
        this.pageSize = page.getSize();
        this.totalElements = page.getTotalElements();
        this.totalPages = page.getTotalPages();
        this.isFirst = page.isFirst();
        this.isLast = page.isLast();
    }

    public PageResponse(List<T> items, int pageNumber, int pageSize, long totalElements, int totalPages) {
        this.items = items;
        this.pageNumber = pageNumber;
        this.pageSize = pageSize;
        this.totalElements = totalElements;
        this.totalPages = totalPages;
        this.isFirst = pageNumber == 0;
        this.isLast = pageNumber >= totalPages - 1;
    }

    public List<T> getItems() { return items; }
    public int getPageNumber() { return pageNumber; }
    public int getPageSize() { return pageSize; }
    public long getTotalElements() { return totalElements; }
    public int getTotalPages() { return totalPages; }
    public boolean isFirst() { return isFirst; }
    public boolean isLast() { return isLast; }
}
""")

# FieldErrorDetail
write("backend/src/main/java/com/ailms/backend/common/api/FieldErrorDetail.java", """
package com.ailms.backend.common.api;

public class FieldErrorDetail {
    private final String field;
    private final String message;
    private final Object rejectedValue;

    public FieldErrorDetail(String field, String message, Object rejectedValue) {
        this.field = field;
        this.message = message;
        this.rejectedValue = rejectedValue;
    }

    public String getField() { return field; }
    public String getMessage() { return message; }
    public Object getRejectedValue() { return rejectedValue; }
}
""")

# ErrorCode
write("backend/src/main/java/com/ailms/backend/common/api/ErrorCode.java", """
package com.ailms.backend.common.api;

public enum ErrorCode {
    VALIDATION_ERROR,
    RESOURCE_NOT_FOUND,
    UNAUTHORIZED,
    FORBIDDEN,
    TENANT_ACCESS_DENIED,
    CONFLICT,
    RATE_LIMIT_EXCEEDED,
    AI_PROVIDER_ERROR,
    PAYMENT_FAILED,
    INTERNAL_SERVER_ERROR,
    BAD_REQUEST
}
""")

# ErrorResponse
write("backend/src/main/java/com/ailms/backend/common/api/ErrorResponse.java", """
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
""")

# Exceptions
write("backend/src/main/java/com/ailms/backend/common/exception/AppException.java", """
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
""")

write("backend/src/main/java/com/ailms/backend/common/exception/ResourceNotFoundException.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class ResourceNotFoundException extends AppException {
    public ResourceNotFoundException(String resourceName, String fieldName, Object fieldValue) {
        super(String.format("%s not found with %s: '%s'", resourceName, fieldName, fieldValue),
                HttpStatus.NOT_FOUND, ErrorCode.RESOURCE_NOT_FOUND);
    }

    public ResourceNotFoundException(String message) {
        super(message, HttpStatus.NOT_FOUND, ErrorCode.RESOURCE_NOT_FOUND);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/common/exception/UnauthorizedException.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class UnauthorizedException extends AppException {
    public UnauthorizedException(String message) {
        super(message, HttpStatus.UNAUTHORIZED, ErrorCode.UNAUTHORIZED);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/common/exception/ForbiddenException.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class ForbiddenException extends AppException {
    public ForbiddenException(String message) {
        super(message, HttpStatus.FORBIDDEN, ErrorCode.FORBIDDEN);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/common/exception/TenantIsolationException.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class TenantIsolationException extends AppException {
    public TenantIsolationException(String message) {
        super(message, HttpStatus.FORBIDDEN, ErrorCode.TENANT_ACCESS_DENIED);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/common/exception/BadRequestException.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class BadRequestException extends AppException {
    public BadRequestException(String message) {
        super(message, HttpStatus.BAD_REQUEST, ErrorCode.BAD_REQUEST);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/common/exception/ConflictException.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class ConflictException extends AppException {
    public ConflictException(String message) {
        super(message, HttpStatus.CONFLICT, ErrorCode.CONFLICT);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/common/exception/RateLimitExceededException.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import org.springframework.http.HttpStatus;

public class RateLimitExceededException extends AppException {
    public RateLimitExceededException(String message) {
        super(message, HttpStatus.TOO_MANY_REQUESTS, ErrorCode.RATE_LIMIT_EXCEEDED);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/common/exception/AiProviderException.java", """
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
""")

write("backend/src/main/java/com/ailms/backend/common/exception/GlobalExceptionHandler.java", """
package com.ailms.backend.common.exception;

import com.ailms.backend.common.api.ErrorCode;
import com.ailms.backend.common.api.ErrorResponse;
import com.ailms.backend.common.api.FieldErrorDetail;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(AppException.class)
    public ResponseEntity<ErrorResponse> handleAppException(AppException ex, HttpServletRequest request) {
        String requestId = getOrCreateRequestId(request);
        log.warn("Application exception [{}]: {} on uri {}", ex.getCode(), ex.getMessage(), request.getRequestURI());
        ErrorResponse response = ErrorResponse.of(ex.getStatus().value(), ex.getCode(), ex.getMessage(), requestId);
        return new ResponseEntity<>(response, ex.getStatus());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException ex, HttpServletRequest request) {
        String requestId = getOrCreateRequestId(request);
        List<FieldErrorDetail> fieldErrors = ex.getBindingResult().getFieldErrors().stream()
                .map(err -> new FieldErrorDetail(err.getField(), err.getDefaultMessage(), err.getRejectedValue()))
                .collect(Collectors.toList());

        ErrorResponse response = ErrorResponse.ofValidation(HttpStatus.BAD_REQUEST.value(), "Validation failed", requestId, fieldErrors);
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(AuthenticationException.class)
    public ResponseEntity<ErrorResponse> handleAuthException(AuthenticationException ex, HttpServletRequest request) {
        String requestId = getOrCreateRequestId(request);
        ErrorResponse response = ErrorResponse.of(HttpStatus.UNAUTHORIZED.value(), ErrorCode.UNAUTHORIZED, "Authentication credentials are invalid or missing", requestId);
        return new ResponseEntity<>(response, HttpStatus.UNAUTHORIZED);
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDenied(AccessDeniedException ex, HttpServletRequest request) {
        String requestId = getOrCreateRequestId(request);
        ErrorResponse response = ErrorResponse.of(HttpStatus.FORBIDDEN.value(), ErrorCode.FORBIDDEN, "Access denied: insufficient permissions", requestId);
        return new ResponseEntity<>(response, HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex, HttpServletRequest request) {
        String requestId = getOrCreateRequestId(request);
        log.error("Unhandled internal server error on [{}], RequestId: {}", request.getRequestURI(), requestId, ex);
        ErrorResponse response = ErrorResponse.of(HttpStatus.INTERNAL_SERVER_ERROR.value(), ErrorCode.INTERNAL_SERVER_ERROR, "An internal server error occurred. Please contact support.", requestId);
        return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    private String getOrCreateRequestId(HttpServletRequest request) {
        String reqId = request.getHeader("X-Request-ID");
        return (reqId != null && !reqId.isBlank()) ? reqId : UUID.randomUUID().toString();
    }
}
""")

print("Backend API and Exception classes created.")
