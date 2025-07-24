import os
import psycopg
from pgvector.psycopg import register_vector
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect("postgresql://rag_user:rag_pass@localhost:5432/rag_db")
register_vector(conn)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY")
)


def retrieve_relevant_chunks(query, k=3):
    query_embedding = embedding_model.embed_query(query)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT content
            FROM documents
            ORDER BY embedding <-> %s::vector
            LIMIT %s
            """,
            (query_embedding, k),
        )
        return [row[0] for row in cur.fetchall()]
