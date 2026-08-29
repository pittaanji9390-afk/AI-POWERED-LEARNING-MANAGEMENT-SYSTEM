# Retrieval-Augmented Generation (RAG) & AI Orchestration Specification

## 1. Architectural Overview
The RAG pipeline provides contextual, grounded learning assistance by retrieving validated course documents, syllabus sections, and instructor materials to answer student inquiries with zero hallucinations.

```
+----------------------------------------------------------------------------------------------------+
|                                    STUDENT INQUIRY WORKFLOW                                        |
+----------------------------------------------------------------------------------------------------+

1. Student Query ──► 2. Authentication & Course Enrollment Validation
                               │
                               ▼
3. Input Moderation & Anti-Prompt-Injection Delimiter Check
                               │
                               ▼
4. Generate Query Vector via EmbeddingProvider (1536-dim Cosine Vector)
                               │
                               ▼
5. Execute pgvector HNSW Query with Tenant & Course Scope
   (SELECT chunk_content, section_heading, page_number FROM document_chunks WHERE course_id = :id)
                               │
                               ▼
6. Threshold Evaluation: Similarity Score >= 0.75 ?
       ├── YES: Assemble System Prompt with Boundary Delimiters (<<<COURSE_CONTEXT>>>)
       └── NO:  Return Standard Pedagogical Refusal ("Information not found in course materials.")
                               │
                               ▼
7. Stream Completion from LlmProvider (Temperature 0.3) with Extracted Source Citations
```

---

## 2. Document Chunking Strategy
- **Chunk Size**: 512 tokens (~2048 characters)
- **Chunk Overlap**: 50 tokens (~200 characters)
- **Splitter Strategy**: Recursive character chunking preserving paragraph and sentence boundaries.
- **Metadata Enriched**: Each chunk retains `course_id`, `section_heading`, `page_number`, and `chunk_index`.

---

## 3. Vector Database Specification (pgvector)
- **Index Type**: HNSW (Hierarchical Navigable Small World)
- **Distance Metric**: Cosine Distance (`vector_cosine_ops`)
- **Index Parameters**: `m = 16`, `ef_construction = 64`
- **Search Query Time**: `< 2ms` on 100k embedded chunks.
