package com.ailms.backend.modules.ai.rag;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class DocumentChunkingService {

    public record DocumentChunkDto(int chunkIndex, String content, int tokenCount, String sectionHeading) {}

    public List<DocumentChunkDto> chunkDocument(String text, int targetChunkTokens, int overlapTokens) {
        if (text == null || text.isBlank()) return List.of();

        List<DocumentChunkDto> chunks = new ArrayList<>();
        String[] paragraphs = text.split("\n\n+");
        StringBuilder currentChunk = new StringBuilder();
        int chunkIdx = 0;

        for (String para : paragraphs) {
            int estimatedTokens = para.length() / 4;
            if ((currentChunk.length() / 4) + estimatedTokens > targetChunkTokens && currentChunk.length() > 0) {
                chunks.add(new DocumentChunkDto(chunkIdx++, currentChunk.toString().trim(), currentChunk.length() / 4, "Course Section"));
                currentChunk = new StringBuilder();
                if (overlapTokens > 0) {
                    String overlap = para.substring(0, Math.min(para.length(), overlapTokens * 4));
                    currentChunk.append(overlap).append(" ");
                }
            }
            currentChunk.append(para).append("

");
        }

        if (currentChunk.length() > 0) {
            chunks.add(new DocumentChunkDto(chunkIdx, currentChunk.toString().trim(), currentChunk.length() / 4, "Course Section"));
        }

        return chunks;
    }
}
