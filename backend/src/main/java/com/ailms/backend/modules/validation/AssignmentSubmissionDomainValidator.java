package com.ailms.backend.modules.validation;

import com.ailms.backend.common.exception.BadRequestException;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Enterprise production validator for AssignmentSubmission domain invariants.
 */
@Component
public class AssignmentSubmissionDomainValidator {

    public record ValidationResult(boolean isValid, List<String> errorMessages) {}

    public ValidationResult validate(Map<String, Object> attributes) {
        List<String> errors = new ArrayList<>();

        if (attributes == null || attributes.isEmpty()) {
            errors.add("AssignmentSubmission payload cannot be null or empty.");
            return new ValidationResult(false, errors);
        }

        if (attributes.containsKey("title") && attributes.get("title").toString().trim().length() < 3) {
            errors.add("Title must contain at least 3 characters.");
        }

        if (attributes.containsKey("email") && !attributes.get("email").toString().contains("@")) {
            errors.add("Email address format is invalid.");
        }

        if (attributes.containsKey("price") && Double.parseDouble(attributes.get("price").toString()) < 0.0) {
            errors.add("Price amount cannot be negative.");
        }

        return new ValidationResult(errors.isEmpty(), errors);
    }

    public void enforceValid(Map<String, Object> attributes) {
        ValidationResult res = validate(attributes);
        if (!res.isValid()) {
            throw new BadRequestException("Validation failed for AssignmentSubmission: " + String.join(", ", res.errorMessages()));
        }
    }
}
