from sqlalchemy import text
from db.database import engine

def get_whitelisted_ips():
    query = text("""
        SELECT ip_address 
        FROM ip_whitelist
        WHERE is_active = TRUE
    """)

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    return [row[0] for row in result]

def is_ip_allowed(client_ip : str):
    query = text("""
        SELECT 1
        FROM ip_whitelist
        WHERE ip_address = :ip
        AND is_active = TRUE
        LIMIT 1
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"ip": client_ip}).fetchone()
    
    return result is not None

