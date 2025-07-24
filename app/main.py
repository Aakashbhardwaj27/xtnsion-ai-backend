from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.docs import router as docs_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG Chatbot")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(docs_router, prefix="/api/docs")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to RAG Chatbot using FastAPI, Azure OpenAI and pgvector"
    }
