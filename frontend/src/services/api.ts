import { apiClient } from "../lib/axios";
import { Course, AiChatMessage } from "../types";

export const mockCourses: Course[] = [
  {
    id: "c1",
    title: "Advanced Distributed Systems with Java & Spring Boot",
    slug: "advanced-distributed-systems",
    shortDescription: "Architect resilient, high-throughput cloud applications with Kafka, Redis, and Postgres.",
    description: "Master enterprise SaaS engineering, microservices partitioning, and zero-downtime deployments.",
    thumbnailUrl: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop&q=60",
    category: "Software Engineering",
    difficulty: "ADVANCED",
    durationMinutes: 1440,
    price: 99.00,
    currency: "USD",
    instructorName: "Dr. Elena Rostova",
    status: "PUBLISHED",
    rating: 4.9,
    enrolledCount: 1420,
    sectionsCount: 8,
    lessonsCount: 42,
  },
  {
    id: "c2",
    title: "AI-Powered RAG Architecture & Vector Search",
    slug: "ai-rag-vector-search",
    shortDescription: "Build production RAG pipelines with embeddings, hybrid search, and hallucination guardrails.",
    description: "Deep dive into vector databases, semantic caching, token optimization, and LLM orchestration.",
    thumbnailUrl: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&auto=format&fit=crop&q=60",
    category: "Artificial Intelligence",
    difficulty: "INTERMEDIATE",
    durationMinutes: 960,
    price: 129.00,
    currency: "USD",
    instructorName: "Marcus Vance",
    status: "PUBLISHED",
    rating: 4.95,
    enrolledCount: 2850,
    sectionsCount: 6,
    lessonsCount: 30,
  }
];

export const courseService = {
  getCatalog: async (): Promise<Course[]> => {
    return Promise.resolve(mockCourses);
  },
  getCourseById: async (id: string): Promise<Course | undefined> => {
    return Promise.resolve(mockCourses.find(c => c.id === id));
  }
};
