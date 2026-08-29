# Retrieval-Augmented Generation (RAG) Architecture

## 1. Document Ingestion Pipeline
```
Document Upload (PDF/Doc) 
  --> MIME Validation 
  --> Text Extraction (Apache Tika) 
  --> Recursive Token Chunking (512 tokens, 50 overlap) 
  --> Embedding Generation 
  --> pgvector Storage (HNSW Cosine Index)
```

## 2. Hallucination Control & Prompt Injection Defense
- RAG queries enforce `organization_id` and `course_id` permission checks BEFORE vector search.
- Prompts use explicit boundary delimiters (`<<<COURSE_CONTEXT>>>`) to prevent user documents from overriding system directives.
- If similarity score is below confidence threshold (0.75), tutor triggers refusal behavior: *"The course material does not provide sufficient information."*
