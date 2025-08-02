# Conversational Voice & Chat Architecture

This architecture outlines a modular, secure, and scalable system for handling voice and chat interactions in high-volume, multi-tenant healthcare environments like dental clinics. It supports shared memory, extensible tool integration, logging, observability, and compliance-aware design.

---
## The System Architecture
<img width="1365" height="833" alt="Xtnsion AI System Architecture" src="https://github.com/user-attachments/assets/76fecfcc-27ca-449d-8b5a-8e07b151cb46" />

## The RAG Pipeline
<img width="4464" height="2374" alt="The RAG Pipeline" src="https://github.com/user-attachments/assets/5a5b7dde-c454-4c15-934b-55b5996bbae2" />

---

## 🧠 Core Components

### 🗣️ Voice Pipeline (Blue Box)
Handles voice interactions from microphone/WebRTC to intelligent response and voice output:

- **Mic/WebRTC Input**: Captures user audio
- **STT (Deepgram/Whisper)**: Converts audio to text
- **Session Manager**: Tracks per-user session state
- **Agent (NLU + Intent)**: Determines intent and next actions
- **Tool Orchestration / Memory Lookup**: Handles memory/context and invokes tools
- **TTS (PlayHT/ElevenLabs)**: Converts response text to audio
- **Voice Output Stream**: Streams voice back to the user

### 💬 Chat Pipeline (Green Box)
Parallel chat interface for text-based interaction:

- **Web/CLI Input**: Accepts user chat input
- **Chat API**: Handles requests to the agent backend
- **Session Manager**: Maintains session and user state
- **Agent (NLU + Tools + Memory)**: Shared logic with voice agent
- **Response Text**: Returns textual reply to user

### 🧩 Shared Context Layer (Purple Box)
Manages shared memory and retrieval components:

- **Redis (Session State)**: Fast in-memory session store
- **Vector DB (Weaviate/Qdrant/Pinecone)**: Stores embedded knowledge base for RAG
- **Embeddings (OpenAI/HuggingFace)**: Converts user input to vector format for retrieval

### 🛠️ Tool Use Logic (Orange Box)
Integrates with backend services and routes intelligently:

- **Routing (per clinic/tenant)**: Ensures correct clinic context
- **Bookings API**: Mock or real endpoint for appointment handling
- **FAQs API**: Retrieves answers for common patient questions

### 📦 Session Manager (Gray Box)
Central state and access controller:

- **JWT/OAuth2**: Secures session authentication
- **Redis/Memcached**: Stores active session data
- **User-Tenant Mapping**: Maintains tenant boundaries
- **NGINX + Node/Python**: Reverse proxy and API layer

### 📊 Logging & Observability (Yellow Box)
Critical for debugging, reliability, and compliance:

- **ELK/Azure Monitor**: Log aggregation and search
- **Prometheus/Grafana/Sentry**: Metrics and alerting
- **Live Failure Dashboard**: Real-time visibility into issues

---

## 🔁 Data & Log Flow

- Voice and chat inputs are **logged** on entry
- All tools and agent actions generate **logs and metrics**
- Failures in TTS/STT, tools, or memory are sent to **alerts and dashboards**
- **Session events** (start, end, timeout) are tracked centrally

---

## 🔐 Security & Compliance Considerations

| Concern                   | Solution                                    |
|--------------------------|---------------------------------------------|
| Data in Transit          | TLS 1.2+ everywhere                         |
| Data at Rest             | AES-256 (Redis, S3, DBs)                    |
| Authentication           | OAuth 2.0 + JWT                            |
| Authorization            | RBAC, tenant isolation                      |
| PHI Logging              | Disabled or opt-in with redaction           |
| Data Residency           | Regional DBs, geo-routing, pluggable config |

---

## 📈 Scaling & Extensibility

- Shared agent logic enables **modality switching** (voice <-> chat)
- Shared Redis/vector DB layer enables **context continuity**
- Session manager enforces **isolation** between tenants
- Can extend to other verticals (e.g., optometry) with new **tool plugins** and **FAQ datasets**

---
