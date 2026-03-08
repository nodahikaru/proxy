from sqlalchemy import text
from db.database import engine

def access_log(client_ip: str, theme: int):
    query = text("""
        INSERT INTO logs (ip_address, theme, log_type)
        VALUES (:ip, :theme, 1)
    """)

    with engine.connect() as conn:
        conn.execute(query, {"ip": client_ip, "theme": theme})
        conn.commit()