import asyncio
from asyncio import AbstractEventLoop
import threading
import os
from dataclasses import dataclass
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Body
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
from typing import Literal, Optional, Any
import httpx
import requests

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    app.state.loop = asyncio.get_event_loop()
    app.state.chat_loop = None  # Initialize chat loop
    yield
    # Shutdown code (if needed)

SHOW_DOCS = os.getenv("SHOW_DOCS", "true").lower() == "true"

app = FastAPI(
    lifespan=lifespan,
    title="AI Chat Proxy",
    description="A FastAPI application that serves as a proxy for AI chat models, including Gemini and Ollama.",
    version="1.0.0",
    openapi_url=None if not SHOW_DOCS else "/openapi.json",
    docs_url=None if not SHOW_DOCS else "/docs",
    redoc_url=None if not SHOW_DOCS else "/redoc"
)

@dataclass
class UserQueue:
    queue: asyncio.Queue
    chat_sesion: genai.ChatSession
    # chat_loop: AbstractEventLoop


websockets: dict[str, WebSocket] = {}  # Maps user_id to websocket
user_queues: dict[str, UserQueue] = {}  # Maps user_id to asyncio.Queue
shared_queue: dict[str, asyncio.Queue] = {}

origins = [
    "https://testsmanager.com",
    "wss://testsmanager.com",
    "wss://testsmanager2.com",
    "https://testsmanager2.com:2443",
    "wss://testsmanager2.com:2443",
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
system_instructions_lools = "for all calculations use the tool also befor you run any tool, please ask user for permission, can I run this tool {tool_name}? \
    with the following parameters: {parameters}? (yes or no)"
genai.configure(api_key="AIzaSyB2GXiEd1eV95qPkFMUaz8vndME1cYFByk") #replace with your api key
# genai_model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp', system_instruction=system_instructions) # gemini-2.0-flash

class Part(BaseModel):
    role: Literal["user", "model"] # assistant
    parts: list[str]

class PromptRequest(BaseModel):
    model: Optional[str] = 'gemini-2.0-flash-thinking-exp' # 'gemini-2.0-flash'
    prompt: list[Part]

class ChatPromptRequest(BaseModel):
    user_id: str
    prompt: str
    model: Optional[str] = 'gemini-2.0-flash-thinking-exp'

def greeting(user_id: str, messsage: str = "Hello") -> str:
    """
    This function send greeting message to the user

    Args:
        user_id (str): The ID of the user to greet.
        messsage (str): The greeting message to be sent to the user at least 6 words you generated.

    Returns:
        dict: greeting message.
    """
    # import random
    # return random.choice(greetings)
    result = call_async_send_message_from_none_async_in_concurncy_way(user_id, messsage)
    return result

def send_user(user_id: str, messsage: str = "Hello") -> str:
    """
    This function send massage to the user

    Args:
        user_id (str): The ID of the user to greet.
        messsage (str): The message to be sent to the user.

    Returns:
        dict: message.
    """
    # import random
    # return random.choice(greetings)
    result = call_async_send_message_from_none_async_in_concurncy_way(user_id, messsage)
    return result

def calculator(expr: str) -> str:
    """
    This function calculates a math expression

    Args:
        expr (str): valid Python math expression.

    Returns:
        str: the result.
    """
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Calculation Error: {e}, expr: {expr}"

# list me the tools you have
# calculate 14+4/2 and send the result to the user
tools = [greeting, send_user, calculator] # Using a model expected to support tool use
app.state.model = genai.GenerativeModel(
    model_name=("gemini-2.0-flash-thinking-exp"),
    tools=tools,
    system_instruction=system_instructions_lools,
)

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

@app.get("/set_chat_model")
def set_model(module_name: str):
    app.state.model = genai.GenerativeModel(
        model_name=module_name,
        tools=tools,
        # system_instruction="use in your answer this url content: https://testsmanager.com",
    )
    return JSONResponse(content={"model": module_name})

# gemini chat proxy ---------------------------------------------------------

def call_async_send_message_from_none_async_in_concurncy_way(user_id: str, msg: str):
    # Use the main loop to run the coroutine thread-safely
    print(f"call_async_send_message_from_none_async_in_concurncy_way: {user_id}, {msg}")
    future = asyncio.run_coroutine_threadsafe(send_message(user_id, msg), app.state.loop)
    result = future.result(timeout=10)  # This blocks until result is ready
    return result

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    websockets[user_id] = websocket
    user_queues[user_id] = UserQueue(queue=asyncio.Queue(), chat_sesion=None)
    try:
        while True:
            data = await websocket.receive_text()
            # Put the received data into the user's queue
            await user_queues[user_id].queue.put(data)
            # await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
        websockets.pop(user_id, None)
        user_queues.pop(user_id, None)
        shared_queue.pop(user_id, None)

@app.get("/send_message")
async def send_message(user_id: str, msg: str = "Hello from FastAPI!"):
    websocket: WebSocket = websockets.get(user_id)
    queue: asyncio.Queue = user_queues.get(user_id).queue
    if websocket and queue:
        await websocket.send_text(msg)
        try:
            # Wait for the next message from the client (with a timeout)
            # response = await asyncio.wait_for(queue.get(), timeout=10)
            # print(f"Received response from {user_id}: {response}")
            return {"message": f"Sent '{msg}' to {user_id}"}
        except asyncio.TimeoutError:
            return {"error": f"No response from client {user_id} within timeout"}
    else:
        return {"error": f"No WebSocket client connected for user_id {user_id}"}

def run_stream_loop2_in_thread(user_id, prompt, main_loop: AbstractEventLoop):
    if not user_queues[user_id].chat_sesion: # not hasattr(user_queues[user_id], 'chat_sesion'):
        user_queues[user_id].chat_sesion = app.state.model.start_chat(enable_automatic_function_calling=True)
    msg = user_queues[user_id].chat_sesion.send_message("user_id: "+user_id + ", query: "+prompt)
    main_loop.call_soon_threadsafe(shared_queue[user_id].put_nowait, msg.text)
    main_loop.call_soon_threadsafe(shared_queue[user_id].put_nowait, None)
    # new_loop.close()

async def generate_stream_chat(user_id: str, prompt: str):
    loop1_loop = asyncio.get_running_loop()
    # print(f"loop1 is using loop: {id(loop1_loop)}")
    # if user_id not in shared_queue:
    shared_queue[user_id] = asyncio.Queue()
    # Start producer in a separate thread with its own loop
    t = threading.Thread(target=run_stream_loop2_in_thread, args=(user_id, prompt, loop1_loop))
    t.start()

    while True:
        item = await shared_queue[user_id].get()
        if item is None:
            break
        yield item
        # print(f"loop1: received {item}")

    t.join()
    print("loop1: done")

@app.post("/tools")
async def chat_stream_content(query_data: ChatPromptRequest = Body(...)):
    # Convert to list of dicts
    return StreamingResponse(generate_stream_chat( query_data.user_id, query_data.prompt),

                              media_type="text/event-stream")

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

# for swagger API http://127.0.0.1:7000/docs#/
# in production https://testsmanager.com:12443/docs#/

# for fastAPI http://127.0.0.1:7000/redoc
# in production https://testsmanager.com:12443/redoc

# for schema http://127.0.0.1:7000/openapi.json
# in production https://testsmanager.com:12443/openapi.json
