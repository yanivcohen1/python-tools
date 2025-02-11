from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
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
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", OLLAMA_URL + OLLAMA_CHAT, json=request_body) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

@app.post(f"{OLLAMA_CHAT}") # for stream
async def proxy(request: Request):
    request_body = await request.json()
    return StreamingResponse(stream_ollama_response(request_body), media_type="text/event-stream")

@app.api_route("/{endpoint:path}", methods=["GET", "POST", "OPTIONS"]) # for none stream
async def non_stream_proxy(request: Request, endpoint: str):
    url = f"{OLLAMA_URL}/{endpoint}"
    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            response = await client.get(url, params=request.query_params)
        elif request.method == "POST":
            response = await client.post(url, json=await request.json())
        else:
            return JSONResponse(content={"message": "Method Not Allowed"}, status_code=405)

    return JSONResponse(content=response.json(), status_code=response.status_code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000) # host="0.0.0.0"
