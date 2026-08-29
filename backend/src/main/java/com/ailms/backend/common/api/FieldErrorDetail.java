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
