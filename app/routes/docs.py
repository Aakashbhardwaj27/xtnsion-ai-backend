from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import os
import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv
import fitz  # PyMuPDF

load_dotenv()

router = APIRouter()
conn = psycopg.connect("postgresql://rag_user:rag_pass@localhost:5432/rag_db")
register_vector(conn)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY")
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


@router.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    if not file.filename.endswith((".txt", ".pdf")):
        raise HTTPException(status_code=400, detail="Only .txt and .pdf are supported.")

    os.makedirs("temp_uploads", exist_ok=True)
    temp_path = f"temp_uploads/{file.filename}"

    # Save uploaded file to disk
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        if file.filename.endswith(".txt"):
            with open(temp_path, "r", encoding="utf-8") as f:
                text = f.read()

        elif file.filename.endswith(".pdf"):
            doc = fitz.open(temp_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

        # Split into chunks
        text_chunks = text_splitter.create_documents([text])

        with conn.cursor() as cur:
            for chunk in text_chunks:
                text = chunk.page_content
                embedding = embedding_model.embed_query(text)
                cur.execute(
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                    (text, embedding),
                )
            conn.commit()

    finally:
        os.remove(temp_path)

    return {"message": "Document uploaded and embedded successfully."}
