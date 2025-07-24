import psycopg
from pgvector.psycopg import register_vector

conn = psycopg.connect("postgresql://rag_user:rag_pass@localhost:5432/rag_db")
register_vector(conn)

with conn.cursor() as cur:
    cur.execute(
        """
       CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)
);

    """
    )
    conn.commit()

print("✅ Table created.")
