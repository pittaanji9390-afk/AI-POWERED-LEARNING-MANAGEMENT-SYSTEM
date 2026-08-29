package com.ailms.backend.modules.storage;

import java.io.InputStream;
import java.time.Duration;

public interface ObjectStorageService {
    StorageFileMetadata uploadFile(String path, InputStream inputStream, String contentType, long size);
    String generatePresignedDownloadUrl(String storageKey, Duration expiry);
    String generatePresignedUploadUrl(String path, String contentType, Duration expiry);
    void deleteFile(String storageKey);
}
