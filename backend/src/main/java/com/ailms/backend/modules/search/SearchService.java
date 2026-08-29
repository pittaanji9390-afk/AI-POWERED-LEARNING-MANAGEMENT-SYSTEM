package com.ailms.backend.modules.search;

import java.util.List;
import java.util.Map;
import java.util.UUID;

public interface SearchService {
    record SearchResultItem(UUID id, String title, String snippet, String type, double score, Map<String, Object> metadata) {}
    List<SearchResultItem> searchCatalog(String query, UUID organizationId, Map<String, Object> filters, int page, int size);
}
