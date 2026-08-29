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
