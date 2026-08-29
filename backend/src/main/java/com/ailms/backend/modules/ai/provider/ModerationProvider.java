package com.ailms.backend.modules.ai.provider;

import java.util.List;

public interface ModerationProvider extends AiProvider {
    record ModerationResult(boolean isFlagged, List<String> categories, double riskScore, String reason) {}
    ModerationResult checkContent(String content);
}
