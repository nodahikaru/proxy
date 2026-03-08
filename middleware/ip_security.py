from fastapi import Request, HTTPException
from db.ip_repository import is_ip_allowed

def get_real_ip(request: Request):
    return request.client.host

async def ip_security_middleware(request: Request, call_next):
    client_ip = get_real_ip(request)
    if not is_ip_allowed(client_ip):
        raise HTTPException(status_code=403, detail="Forbidden IP")

    return await call_next(request)