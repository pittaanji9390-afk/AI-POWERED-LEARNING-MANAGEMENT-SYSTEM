# AI SPI Layer & Model Orchestration

## 1. Zero Vendor Lock-In Provider Mesh
All AI interactions operate through decoupled Java Service Provider Interfaces (SPI):
- `AiProvider`: Core health & telemetry interface
- `LlmProvider`: Chat completion, async streaming, structured JSON schema generation
- `EmbeddingProvider`: Text-to-vector embedding generation (1536 dimension default)
- `ModerationProvider`: Content safety and risk scoring

## 2. Supported Adaptors
1. `MockAiProvider`: Offline testing & deterministic local integration
2. `OpenAiProvider`: OpenAI GPT-4o / text-embedding-3
3. `AzureAiProvider`: Azure OpenAI private endpoints
4. `OllamaProvider`: Local self-hosted models (Llama 3, Mistral)
