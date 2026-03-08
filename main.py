from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import secrets
from datetime import datetime, timedelta
import logging
from middleware.ip_security import ip_security_middleware
from db.log_repository import access_log
app = FastAPI()

app.middleware("http")(ip_security_middleware)

active_tokens = {}

@app.get("/")
async def check_ip(request: Request):
    client_ip = request.client.host
    token = secrets.token_urlsafe(16)
    expire_time = datetime.utcnow() + timedelta(minutes=5)
    active_tokens[token] = {"ip": client_ip, "expires": expire_time}
    logging.info(f"Issued token {token} to IP {client_ip}")
    return JSONResponse({"token": token, "expires": expire_time.isoformat()})

@app.post("/do_log")
async def do_log(request: Request):
    # access log: client ip, theme, timestamp
    client_ip = request.client.host
    data = await request.json()
    access_log(client_ip=client_ip, theme=data["theme"])
    return JSONResponse({"status": True, "msg": ""})
    