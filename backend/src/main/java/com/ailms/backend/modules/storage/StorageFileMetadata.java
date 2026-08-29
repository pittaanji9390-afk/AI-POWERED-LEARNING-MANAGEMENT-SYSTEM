package com.ailms.backend.modules.storage;

import java.time.Instant;

public record StorageFileMetadata(
        String storageKey,
        String originalFilename,
        String contentType,
        long sizeInBytes,
        Instant uploadedAt,
        String downloadUrl
) {}
