import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def run_query(sql: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cur.description:  # SELECT query
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return [dict(zip(columns, row)) for row in rows]
            else:  # INSERT/UPDATE/DELETE
                conn.commit()
                return [{"status": "success"}]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()
