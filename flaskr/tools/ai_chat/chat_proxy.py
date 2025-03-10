# FastAPI (main.py)
from fastapi import FastAPI, Request, Response, Body
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
# import asyncio
import httpx
import requests

app = FastAPI()

origins = [
    "https://testsmanager.com",
    "https://testsmanager2.com:2443",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live")
def live():
    return Response(content="Live", media_type="text/plain")

# gemini proxy ---------------------------------------------------------

genai.configure(api_key="AIzaSyB2GXiEd1eV95qPkFMUaz8vndME1cYFByk") #replace with your api key
genai_model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp') # gemini-2.0-flash

class GeminiQueryData(BaseModel):
    query: str

def generate_stream(query: str):
    response = genai_model.generate_content(query, stream=True)  # No await needed
    for chunk in response:  # Regular for loop, not async
        # print(chunk.text, end="")
        yield chunk.text

@app.post("/stream")
async def stream_content(query_data: GeminiQueryData = Body(...)):
    return StreamingResponse(generate_stream(query_data.query + ' use in your answer this url content: https://testsmanager.com'), media_type="text/event-stream")

# ollama proxy ---------------------------------------------------------

OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_CHAT = "/v1/chat/completions"

async def stream_ollama_response(request_body: dict):
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream("POST", OLLAMA_URL + OLLAMA_CHAT, json=request_body) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

@app.post(f"/ollama{OLLAMA_CHAT}") # for stream
async def stream_proxy(request: Request):
    request_body = await request.json()
    return StreamingResponse(stream_ollama_response(request_body), media_type="text/event-stream")

@app.api_route("/ollama/{endpoint:path}", methods=["GET", "POST", "OPTIONS"]) # for none stream
def non_stream_proxy(request: Request, endpoint: str):
    origin = request.headers.get("origin", "Unknown")
    host = request.headers.get("host", "Unknown")
    cookie_value = request.cookies # .get("your_cookie_name", None)  # Replace with actual cookie name
    print(f"Request:, Origin: {origin}, host: {host}, cookie: {cookie_value}")

    if origin == "http://localhost:9000": # for dev porpes
        if host not in ["testsmanager.com:12443", "192.168.0.155:7000"]:
            return JSONResponse(content={"message": "Origin not allowed"}, status_code=405)

    url = f"{OLLAMA_URL}/{endpoint}"
    if request.method == "GET":
        response = requests.get(url, params=request.query_params, timeout=10)
    elif request.method == "POST":
        response = requests.post(url, json=request.json(), timeout=10)
    else:
        return JSONResponse(content={"message": "Method Not Allowed"}, status_code=405)

    return JSONResponse(content=response.json(), status_code=response.status_code)

# groq proxy ---------------------------------------------------------

API_KEY="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" #replace with your api key
MODEL = "deepseek-r1-distill-llama-70b"
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
GROQ_URL = "https://api.groq.com/openai/"
GROQ_CHAT = "v1/chat/completions"

class GroqQueryData(BaseModel):
    prompt: str
    model: str = MODEL

async def groq_stream_response(request_body: GroqQueryData):
    body_json = {
        "model": request_body.model,  #'deepseek-r1:8b',
        "messages": [
            {"role": "system", "content": ""},
            {"role": "user", "content": request_body.prompt},
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 6144,  # 4096, // -1 for unlimited
        "stream": True,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream("POST", GROQ_URL + GROQ_CHAT, json=body_json, headers=HEADERS) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

@app.post(f"/groq/{GROQ_CHAT}") # for stream
async def groq_stream_proxy(query_data: GroqQueryData = Body(...)):
    return StreamingResponse(groq_stream_response(query_data), media_type="text/event-stream")

@app.api_route("/groq/{endpoint:path}", methods=["GET", "POST", "OPTIONS"]) # for none stream
def groq_non_stream_proxy(request: Request, endpoint: str):
    origin = request.headers.get("origin", "Unknown")
    host = request.headers.get("host", "Unknown")
    cookie_value = request.cookies # .get("your_cookie_name", None)  # Replace with actual cookie name
    print(f"Request:, Origin: {origin}, host: {host}, cookie: {cookie_value}")

    url = f"{GROQ_URL}{endpoint}"
    if request.method == "GET":
        response = requests.get(url, params=request.query_params, headers= HEADERS, timeout=10)
    elif request.method == "POST":
        response = requests.post(url, json=request.json(), headers= HEADERS, timeout=10)
    else:
        return JSONResponse(content={"message": "Method Not Allowed"}, status_code=405)

    return JSONResponse(content=response.json(), status_code=response.status_code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000) # host="0.0.0.0" listning to all interfaces
