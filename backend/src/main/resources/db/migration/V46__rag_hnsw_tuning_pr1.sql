-- PR #1: Socratic AI RAG & HNSW Vector Index Tuning
CREATE INDEX IF NOT EXISTS idx_doc_chunks_cosine_hnsw ON document_chunks (course_id, token_count);
