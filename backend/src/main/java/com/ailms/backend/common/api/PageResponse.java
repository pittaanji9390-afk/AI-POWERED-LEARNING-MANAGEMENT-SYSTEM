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
