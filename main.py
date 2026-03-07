from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import secrets
from datetime import datetime, timedelta
import logging
import os

app = FastAPI()
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
WHITELIST_IPS = ["216.144.245.174"]

active_tokens = {}
logging.basicConfig(level=logging.INFO, filename="access.log", format="%(asctime)s | %(message)s")

@app.middleware("http")
async def ip_check_and_log(request: Request, call_next):
    #client_ip = request.client.host
    client_ip = request.headers.get("x-forwarded-for")
    logging.info(f"IP {client_ip} requested {request.url.path}")

    # Allow localhost during development
    if DEBUG and client_ip.startswith("127."):
        return await call_next(request)

    if client_ip not in WHITELIST_IPS:
        logging.warning(f"Blocked access from IP: {client_ip}")
        raise HTTPException(status_code=403, detail="Forbidden IP")

    return await call_next(request)

@app.get("/")
async def get():
    return JSONResponse({"msg": "Welcome to proxy"})

@app.get("/get_token")
async def get_token(request: Request):
    client_ip = request.client.host
    token = secrets.token_urlsafe(16)
    expire_time = datetime.utcnow() + timedelta(minutes=5)
    active_tokens[token] = {"ip": client_ip, "expires": expire_time}
    logging.info(f"Issued token {token} to IP {client_ip}")
    return JSONResponse({"token": token, "expires": expire_time.isoformat()})

