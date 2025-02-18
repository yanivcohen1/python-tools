from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import requests
import asyncio

# Start ollama first
# in cmd type "ollama serve"
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434"
OLLAMA_CHAT = "/v1/chat/completions"

async def stream_ollama_response(request_body: dict):
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream("POST", OLLAMA_URL + OLLAMA_CHAT, json=request_body) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

@app.post(f"{OLLAMA_CHAT}") # for stream
async def stream_proxy(request: Request):
    request_body = await request.json()
    return StreamingResponse(stream_ollama_response(request_body), media_type="text/event-stream")

@app.api_route("/{endpoint:path}", methods=["GET", "POST", "OPTIONS"]) # for none stream
def non_stream_proxy(request: Request, endpoint: str):
    url = f"{OLLAMA_URL}/{endpoint}"
    if request.method == "GET":
        response = requests.get(url, params=request.query_params, timeout=10)
    elif request.method == "POST":
        response = requests.post(url, json=request.json(), timeout=10)
    else:
        return JSONResponse(content={"message": "Method Not Allowed"}, status_code=405)

    return JSONResponse(content=response.json(), status_code=response.status_code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000) # host="0.0.0.0"

# for swagger API http://127.0.0.1:8000/docs#/
# for fastAPI http://127.0.0.1:8000/redoc
