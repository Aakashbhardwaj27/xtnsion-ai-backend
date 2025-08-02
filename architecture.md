# Xtnsion AI System Architecture

This architecture outlines a modular, secure, and scalable system for handling voice and chat interactions in high-volume, multi-tenant healthcare environments like dental clinics. It supports shared memory, extensible tool integration, logging, observability, and compliance-aware design.


## The System Architecture
<img width="1365" height="833" alt="Xtnsion AI System Architecture" src="https://github.com/user-attachments/assets/76fecfcc-27ca-449d-8b5a-8e07b151cb46" />

## The RAG Pipeline
<img width="4464" height="2374" alt="The RAG Pipeline" src="https://github.com/user-attachments/assets/5a5b7dde-c454-4c15-934b-55b5996bbae2" />

---

## Overview
This section outlines the design rationale behind the architecture of Xtnsion AI assistant that supports both voice and chat interfaces. It includes modules for automatic speech recognition (STT), language processing, retrieval-augmented generation (RAG), and text-to-speech (TTS), along with supporting services like observability, session management, and vector storage.

---

## Key Design Principles

### 1. **Modularity and Separation of Concerns**
Each functional block (STT, Agent, TTS, RAG, Vector DB, Orchestration) is encapsulated into distinct microservices that can be independently developed, deployed, and scaled.

### 2. **Resilience and Fault Tolerance**
- Failures in any downstream service (e.g., STT, TTS, RAG) trigger retries with exponential backoff.
- Fallback responses are returned if service degradation persists.
- Circuit breakers and rate limiters are implemented at gateway and orchestrator levels.

### 3. **Observability**
- Centralized logging using Azure Monitor or OpenTelemetry-compatible stacks (e.g., ELK, Prometheus + Grafana).
- Distributed tracing for inter-service calls.
- Custom metrics (latency, error rate, token usage, service-level retries).

---

## Architecture Components

### 1. **Ingress Layer**
- Accepts both WebSocket and HTTP connections.
- Identifies channel (voice/chat) and routes to Orchestrator.

### 2. **Session Layer**
- Maintains unique session IDs and conversation context.
- Stores metadata (user role, auth, timestamp, preferences).
- Isolates sessions per tenant/user.

### 3. **Voice Pipeline**
- Audio is chunked and streamed to STT in real-time.
- STT returns interim/final transcripts with latency < 500ms.
- Transcript sent to Orchestrator → Agent → TTS.
- TTS response streamed back as audio via WebSocket.

### 4. **Chat Pipeline**
- Typed user input sent to Agent directly.
- Agent calls RAG if retrieval is enabled.
- Final output sent to frontend.

### 5. **Agent Layer**
- Stateless LLM orchestrator with plug-and-play capabilities.
- Integrates OpenAI GPT-4o, local models (via vLLM), or Azure OpenAI.
- Supports function calling, streaming, system messages.

### 6. **Retrieval Layer (RAG)**
- Query-embedding generated using OpenAI/Azure/Instructor.
- Vector DB (e.g., Qdrant, pgvector) queried with similarity search.
- Retrieved documents passed back to Agent.

### 7. **Tool Layer**
- Includes external APIs (e.g., calendar, email, document lookup).
- Invoked by Agent using function calling or tool-use architecture.

---

## Compliance, Security, and Data Residency

### Compliance
- GDPR, SOC2, HIPAA-ready foundation using Azure regional services.
- User data is encrypted at rest (AES-256) and in transit (TLS 1.3).
- Audit trails maintained for session metadata and model interactions.

### Data Residency
- All services are containerized and deployed in-region.
- Vector DB and session cache use zonal affinity for low-latency access.
- Option for client-specific tenancy to isolate data per enterprise.

---

## Scalability and Latency Considerations

### Latency Breakdown
| Component | Target P99 Latency |
|----------|---------------------|
| STT      | < 500ms             |
| Agent    | < 1.2s              |
| TTS      | < 700ms             |
| RAG      | < 300ms             |

- Overall roundtrip for voice interaction: ~2.5s max
- Chat-only: ~1.2s with RAG

### Scaling Strategy
- STT/TTS: Stateless inference containers with autoscaling
- Agent: Horizontally scaled LLM gateway with caching + batching
- Vector DB: Sharded and replicated, supports distributed retrieval
- Orchestrator: Queue-based pipeline with worker pools

### Resilience Tactics
- Retry logic with exponential backoff and jitter
- Circuit breakers per external dependency
- Dead-letter queues for failed payloads
- Synthetic monitoring of each layer

---

## Failure Handling Strategies

### STT/TTS Failures
- Retry 3x before fallback to a canned message
- Notify UI of degraded audio mode if necessary

### RAG/Vector DB
- Retry with increased timeout
- Fallback to Agent-only generation if retrieval fails

### Tool/API Failures
- Isolated timeout with cancellation token (e.g., 2s max)
- Agent handles exception and either retries or gracefully continues

---

## Conclusion
This architecture is optimized for real-time interaction, high availability, modular extensibility, and secure data processing—making it suitable for multi-tenant AI platforms serving enterprise workloads over both voice and chat channels.
