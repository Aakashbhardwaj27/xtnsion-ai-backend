import os
import psycopg
from pgvector.psycopg import register_vector
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# DB setup
conn = psycopg.connect("postgresql://rag_user:rag_pass@localhost:5432/rag_db")
register_vector(conn)

# Initialize embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Load your document
document_text = """
OpenAI develops artificial general intelligence (AGI) to benefit humanity.
They provide APIs for natural language, image, and audio understanding.
"""

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_text(document_text)

# Insert into pgvector
with conn.cursor() as cur:
    for chunk in chunks:
        embedding = embedding_model.embed_query(chunk)
        cur.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (chunk, embedding),
        )
    conn.commit()

print("✅ Embedded and stored chunks.")
