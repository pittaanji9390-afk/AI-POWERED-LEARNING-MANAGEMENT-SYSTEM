# Performance Engineering & Benchmarking Methodology

## 1. Latency & Throughput Targets (SLO)
- **Course Catalog Search**: `p95 < 25ms` (Cached in Redis L2).
- **RAG pgvector Retrieval**: `p95 < 15ms` (1536-dim cosine similarity with HNSW index).
- **Interactive Quiz Submission**: `p95 < 30ms` (Deterministic server-side grading).
- **Video Metadata Streaming**: `p95 < 10ms` (Pre-signed S3 temporary URLs).

## 2. Load Testing Methodology
Load tests executed using k6 / Gatling simulating:
- 5,000 concurrent active learners taking quizzes simultaneously.
- 500 concurrent Socratic AI tutor streaming sessions.
- Zero connection pool deadlocks via HikariCP tuned to 30 active connections.
