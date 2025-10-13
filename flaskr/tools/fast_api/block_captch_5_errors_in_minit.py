from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Redis (adjust for your setup)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await r.close()

app = FastAPI(lifespan=lifespan)

# Configure password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Example user credentials (in real apps use DB with pre-hashed passwords)
# This is bcrypt hash for "secret123"
USER_DB = {"alice": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK1O6Be1S"}

# Configuration
MAX_FAILED_ATTEMPTS = 5
BLOCK_WINDOW_SECONDS = 60


async def record_failed_login(ip: str) -> int:
    """Increment failed attempts counter for this IP."""
    key = f"fail:{ip}"
    val = await r.incr(key)
    if val == 1:
        await r.expire(key, BLOCK_WINDOW_SECONDS)
    return val


async def clear_failed_login(ip: str):
    """Reset counter for this IP."""
    await r.delete(f"fail:{ip}")


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    ip = request.client.host
    key = f"fail:{ip}"

    # Check if IP is already blocked
    attempts = await r.get(key)
    if attempts and int(attempts) >= MAX_FAILED_ATTEMPTS:
        if request.headers.get("captcha") == "solved":  # captcha solved by client
            await clear_failed_login(ip)
        else:
          # this error in the client show the captcha
          raise HTTPException(
              status_code=status.HTTP_429_TOO_MANY_REQUESTS,
              detail=f"Too many failed attempts. Try again after {BLOCK_WINDOW_SECONDS} seconds.",
          )

    # Verify credentials
    user_hash = USER_DB.get(username)
    if not user_hash or not pwd_context.verify(password, user_hash):
        count = await record_failed_login(ip)
        remaining = max(0, MAX_FAILED_ATTEMPTS - count)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "Invalid credentials.",
                "remaining_attempts": remaining,
                "blocked_after": BLOCK_WINDOW_SECONDS,
            },
        )

    # Successful login: clear failures
    await clear_failed_login(ip)
    return {"message": f"Welcome, {username}!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000, host="0.0.0.0") # host="0.0.0.0"
