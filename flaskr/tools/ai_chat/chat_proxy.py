# FastAPI (main.py)
from fastapi import FastAPI, Request, Response, Body
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
from typing import List, Literal, Optional
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
    return JSONResponse(content={"status": "Live"})

# gemini proxy ---------------------------------------------------------
system_instructions = 'use in your answer this url content: https://testsmanager.com'
genai.configure(api_key="AIzaSyB2GXiEd1eV95qPkFMUaz8vndME1cYFByk") #replace with your api key
# genai_model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp', system_instruction=system_instructions) # gemini-2.0-flash

class Part(BaseModel):
    role: Literal["user", "model"] # assistant
    parts: list[str]

class PromptRequest(BaseModel):
    model: Optional[str] = 'gemini-2.0-flash-thinking-exp' # 'gemini-2.0-flash'
    prompt: list[Part]

def generate_stream(query: str, model_name: str):
    model = genai.GenerativeModel(model_name, system_instruction=system_instructions) # 'gemini-2.0-flash-thinking-exp')
    response = model.generate_content(query, stream=True)  # No await needed
    for chunk in response:  # Regular for loop, not async
        # print(chunk.text, end="")
        yield chunk.text

@app.post("/stream")
async def stream_content(query_data: PromptRequest = Body(...)):
    # Convert to list of dicts
    prompt = [p.model_dump() for p in query_data.prompt]
    return StreamingResponse(generate_stream(prompt, query_data.model), media_type="text/event-stream") # query_data.model

@app.get("/models")
def models():
    models = genai.list_models()
    models_list = []
    for m in models:
        # Check if the model supports the standard 'generateContent' method
        if 'generateContent' in m.supported_generation_methods:
            models_list.append(m.name[7:])
    return JSONResponse(content=models_list)

# ollama proxy ---------------------------------------------------------

OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_CHAT = "/v1/chat/completions"

class PartOpenAI(BaseModel):
    role: Literal["user", "assistant"] # assistant
    content: str

class PromptRequestOpenAI(BaseModel):
    model: Optional[str]
    prompt: list[PartOpenAI]

def stream_ollama_response(request_body: PromptRequestOpenAI):
    prompt = [p.model_dump() for p in request_body.prompt]
    body_json = {
        "model": request_body.model,  #'deepseek-r1:8b',
        "messages": prompt,
        # "temperature": 0.7,
        "top_p": 0.95,
        'max_tokens': -1, # -1 for unlimited  # 4096
        "stream": True,
    }
    with requests.post(OLLAMA_URL + OLLAMA_CHAT, json=body_json, stream=True, timeout=60) as response:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                yield chunk

@app.post(f"/ollama{OLLAMA_CHAT}") # for stream
async def stream_proxy(request_body: PromptRequestOpenAI = Body(...)):
    # request_body = await request.json()
    return StreamingResponse(stream_ollama_response(request_body), media_type="text/event-stream")

@app.api_route("/ollama/{endpoint:path}", methods=["GET", "POST", "OPTIONS"]) # for none stream
def non_stream_proxy(request: Request, endpoint: str):
    origin = request.headers.get("origin", "Unknown")
    host = request.headers.get("host", "Unknown")
    cookie_value = request.cookies # .get("your_cookie_name", None)  # Replace with actual cookie name
    print(f"Request:, Origin: {origin}, host: {host}, cookie: {cookie_value}")

    if origin == "http://localhost:9000": # for dev porpes
        if host not in ["testsmanager.com:12443", "192.168.0.155:7000", "127.0.0.1:7000"]:
            return JSONResponse(content={"message": "Origin not allowed"}, status_code=405)

    url = f"{OLLAMA_URL}/{endpoint}"
    if request.method == "GET":
        response = requests.get(url, params=request.query_params, timeout=10)
    elif request.method == "POST":
        response = requests.post(url, json=request.json(), timeout=10)
    else:
        return JSONResponse(content={"message": "Method Not Allowed"}, status_code=405)

    return JSONResponse(content=response.json(), status_code=response.status_code)

# openrouter proxy ---------------------------------------------------------

API_KEY = "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"
MODEL = "deepseek/deepseek-chat-v3-0324:free"
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
OPENROUTER_URL = "https://openrouter.ai/api/v1/"
OPENROUTER_CHAT = "chat/completions"

async def openrouter_stream_response(request_body: PromptRequestOpenAI):
    prompt = [p.model_dump() for p in request_body.prompt]
    body_json = {
        "model": request_body.model,  #'deepseek-r1:8b',
        "messages": prompt,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 6144,  # 4096, // -1 for unlimited
        "stream": True,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream("POST", OPENROUTER_URL + OPENROUTER_CHAT, json=body_json, headers=HEADERS) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

@app.post(f"/openrouter/{OPENROUTER_CHAT}") # for stream
async def openrouter_stream_proxy(query_data: PromptRequestOpenAI = Body(...)):

    return StreamingResponse(openrouter_stream_response(query_data), media_type="text/event-stream")

@app.api_route("/openrouter/{endpoint:path}", methods=["GET", "POST", "OPTIONS"]) # for none stream
def openrouter_non_stream_proxy(request: Request, endpoint: str):
    origin = request.headers.get("origin", "Unknown")
    host = request.headers.get("host", "Unknown")
    cookie_value = request.cookies # .get("your_cookie_name", None)  # Replace with actual cookie name
    print(f"Request:, Origin: {origin}, host: {host}, cookie: {cookie_value}")

    url = f"{OPENROUTER_URL}{endpoint}"
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
