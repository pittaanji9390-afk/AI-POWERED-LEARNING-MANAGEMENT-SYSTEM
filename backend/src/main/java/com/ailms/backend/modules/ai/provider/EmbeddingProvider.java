package com.ailms.backend.modules.ai.provider;

import java.util.List;

public interface EmbeddingProvider extends AiProvider {
    List<Float> generateEmbedding(String text);
    List<List<Float>> generateBatchEmbeddings(List<String> texts);
    int getDimension();
}
