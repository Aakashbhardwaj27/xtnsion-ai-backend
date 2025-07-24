# 🦷 XtnsionAI Backend

XtnsionAI is an intelligent AI assistant for dental clinics. This backend powers the AI logic, document retrieval, voice transcription, and conversation context management.

---

## 🧠 Features

- 💬 Conversational AI using OpenAI (GPT-4/GPT-4o)
- 📚 Retrieval-Augmented Generation (RAG) with Pinecone + MongoDB
- 🗣️ Voice-based interaction with transcript generation
- ⚙️ REST API for frontend integration
- 📥 PDF/document ingestion and embedding
- ⚡ Redis for caching and queueing
- ✨ Modular codebase with structured routes/controllers

---

## 🏗️ Project Structure

xtnsion-backend/
├── src/
│ ├── controllers/
│ ├── routes/
│ ├── services/
│ ├── embeddings/
│ ├── utils/
│ ├── models/
│ ├── config/
│ └── index.ts / app.ts
├── public/
├── .env
├── package.json
└── README.md

---

## ⚙️ Setup Instructions

### Clone the repo

```bash
git clone https://github.com/your-org/xtnsion-backend.git
cd xtnsion-backend

```
### Setup Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt

docker-compose up -d  # setup pgvector

```

### Run App
```bash
uvicorn app.main:app --reload  
```