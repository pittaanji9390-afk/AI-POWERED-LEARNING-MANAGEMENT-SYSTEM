import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("Generating final push modules...")

# Additional Domain Validators & Mappers in Backend
entities = [
    "Course", "User", "Organization", "Enrollment", "LearningProgress",
    "Quiz", "Question", "Assignment", "AssignmentSubmission", "Certificate",
    "Discussion", "Payment", "Notification", "Skill", "LearningPath"
]

for entity in entities:
    # Validator
    val_code = f"""package com.ailms.backend.modules.validation;

import com.ailms.backend.common.exception.BadRequestException;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Enterprise production validator for {entity} domain invariants.
 */
@Component
public class {entity}DomainValidator {{

    public record ValidationResult(boolean isValid, List<String> errorMessages) {{}}

    public ValidationResult validate(Map<String, Object> attributes) {{
        List<String> errors = new ArrayList<>();

        if (attributes == null || attributes.isEmpty()) {{
            errors.add("{entity} payload cannot be null or empty.");
            return new ValidationResult(false, errors);
        }}

        if (attributes.containsKey("title") && attributes.get("title").toString().trim().length() < 3) {{
            errors.add("Title must contain at least 3 characters.");
        }}

        if (attributes.containsKey("email") && !attributes.get("email").toString().contains("@")) {{
            errors.add("Email address format is invalid.");
        }}

        if (attributes.containsKey("price") && Double.parseDouble(attributes.get("price").toString()) < 0.0) {{
            errors.add("Price amount cannot be negative.");
        }}

        return new ValidationResult(errors.isEmpty(), errors);
    }}

    public void enforceValid(Map<String, Object> attributes) {{
        ValidationResult res = validate(attributes);
        if (!res.isValid()) {{
            throw new BadRequestException("Validation failed for {entity}: " + String.join(", ", res.errorMessages()));
        }}
    }}
}}
"""
    write(f"backend/src/main/java/com/ailms/backend/modules/validation/{entity}DomainValidator.java", val_code)

    # Mapper / DTO Converter
    map_code = f"""package com.ailms.backend.modules.mapper;

import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Enterprise entity transformer and DTO converter for {entity}.
 */
@Component
public class {entity}DtoTransformer {{

    public record {entity}Dto(
            UUID id,
            String name,
            String status,
            Instant createdAt,
            Instant updatedAt,
            Map<String, Object> metadata
    ) {{}}

    public {entity}Dto toDto(UUID id, String name, String status, Map<String, Object> rawProps) {{
        Map<String, Object> meta = new HashMap<>(rawProps != null ? rawProps : Map.of());
        meta.put("entityType", "{entity}");
        meta.put("transformedAt", Instant.now().toString());

        return new {entity}Dto(
                id != null ? id : UUID.randomUUID(),
                name != null ? name : "Unnamed {entity}",
                status != null ? status : "ACTIVE",
                Instant.now(),
                Instant.now(),
                meta
        );
    }}
}}
"""
    write(f"backend/src/main/java/com/ailms/backend/modules/mapper/{entity}DtoTransformer.java", map_code)

# Additional UI Components in Frontend
write("frontend/src/components/ui/tooltip.tsx", """
import React, { useState } from "react";
import { cn } from "../../lib/utils";

export interface TooltipProps {
  content: string;
  children: React.ReactNode;
  position?: "top" | "bottom" | "left" | "right";
}

export const Tooltip: React.FC<TooltipProps> = ({ content, children, position = "top" }) => {
  const [isVisible, setIsVisible] = useState(false);

  const posClasses = {
    top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
    left: "right-full top-1/2 -translate-y-1/2 mr-2",
    right: "left-full top-1/2 -translate-y-1/2 ml-2",
  };

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div
          className={cn(
            "absolute z-50 px-2.5 py-1 text-[11px] font-medium text-slate-200 bg-slate-900 border border-slate-800 rounded-md shadow-lg whitespace-nowrap pointer-events-none",
            posClasses[position]
          )}
        >
          {content}
        </div>
      )}
    </div>
  );
};
""")

write("frontend/src/components/ui/avatar.tsx", """
import React from "react";
import { cn } from "../../lib/utils";

export interface AvatarProps {
  name: string;
  src?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export const Avatar: React.FC<AvatarProps> = ({ name, src, size = "md", className }) => {
  const sizes = {
    sm: "h-8 w-8 text-xs",
    md: "h-10 w-10 text-sm",
    lg: "h-14 w-14 text-lg",
  };

  const initials = name
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();

  if (src) {
    return (
      <img
        src={src}
        alt={name}
        className={cn("rounded-full object-cover border border-slate-800", sizes[size], className)}
      />
    );
  }

  return (
    <div
      className={cn(
        "rounded-full bg-indigo-600/20 text-indigo-400 font-bold flex items-center justify-center border border-indigo-500/30",
        sizes[size],
        className
      )}
    >
      {initials}
    </div>
  );
};
""")

write("frontend/src/components/ui/breadcrumb.tsx", """
import React from "react";
import { Link } from "react-router-dom";
import { ChevronRight, Home } from "lucide-react";

export interface BreadcrumbItem {
  label: string;
  to?: string;
}

export const Breadcrumb: React.FC<{ items: BreadcrumbItem[] }> = ({ items }) => {
  return (
    <nav className="flex items-center gap-2 text-xs text-slate-400">
      <Link to="/" className="hover:text-white flex items-center gap-1">
        <Home className="h-3.5 w-3.5" />
      </Link>
      {items.map((item, idx) => (
        <React.Fragment key={idx}>
          <ChevronRight className="h-3.5 w-3.5 text-slate-600" />
          {item.to ? (
            <Link to={item.to} className="hover:text-white transition-colors">
              {item.label}
            </Link>
          ) : (
            <span className="text-slate-200 font-medium">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
};
""")

print("Final push modules generated.")
