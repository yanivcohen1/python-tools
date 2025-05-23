# FastAPI (main.py)
import asyncio
from asyncio import AbstractEventLoop
import threading
from dataclasses import dataclass
# from typing import List, Optional, Dict, Literal, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Body
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from pydantic import BaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    app.state.loop = asyncio.get_event_loop()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan)
shared_queue = asyncio.Queue()
templates = Jinja2Templates(directory="./flaskr/tools/ai_chat")
model_name = ("gemini-2.0-flash-thinking-exp")
chat_loop: AbstractEventLoop = None
@dataclass
class UserQueue:
    queue: asyncio.Queue
    chat_sesion: genai.ChatSession
    chat_loop: AbstractEventLoop


websockets: dict[str, WebSocket] = {}  # Maps user_id to websocket
user_queues: dict[str, UserQueue] = {}  # Maps user_id to asyncio.Queue

origins = [
    "https://testsmanager.com",
    "https://testsmanager2.com:2443",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyB2GXiEd1eV95qPkFMUaz8vndME1cYFByk") #replace with your api key

class PromptRequest(BaseModel):
    user_id: str
    prompt: str
    model: str

# import random

def get_greeting(user_id: str, messsage: str = "Hello") -> str:
    """
    This function returns greeting message

    Args:
        user_id (str): The ID of the user to greet.
        messsage (str): The greeting message to be sent to the user.

    Returns:
        dict: greeting message.
    """
    greetings = [
        "Hello! Hope you're having a great day!",
        "Hi there! Nice to see you!",
        "Hey! How's everything going?",
        "Greetings! Wishing you a wonderful day!",
        "What's up? Hope you're doing well!",
        "Hi! Just wanted to say hello!",
        "Hello! Sending good vibes your way!",
        "Hey there! Hope you're smiling today!",
        "Good to see you! Have a fantastic day!",
        "Hi! Stay awesome!",
        "Hello! Hope you’re feeling amazing!",
        "Hey! Keep up the great work!",
        "Hi there! Stay positive and strong!",
        "Hello! Let's make today amazing!",
        "Hi! Wishing you lots of happiness!",
        "Hey there! You’re doing great!",
        "Hello! Keep shining!",
        "Hi! Hope today brings you joy!",
        "Hey! Don’t forget to smile!",
        "Hi there! Enjoy every moment!",
        "Hello! Hope your day is filled with laughter!",
        "Hey! Sending you some cheer!",
        "Hi! Take care and be kind to yourself!",
        "Hello! Stay confident and bright!",
        "Hi there! You've got this!",
        "Hey! Today is your day!",
        "Hello! Wishing you success in all you do!",
        "Hi! Keep being awesome!",
        "Hey there! You rock!",
        "Hello! Keep moving forward!"
    ]
    # return random.choice(greetings)
    result = call_async_send_message_from_none_async_in_concurncy_way(user_id, messsage)
    return result

tools = [get_greeting] # Using a model expected to support tool use
app.state.model = genai.GenerativeModel(
    model_name=model_name,
    tools=tools,
    system_instruction="befor you run any tool, please ask user for permission, can I run this tool {tool}? with the following parameters: {parameters}?",
)

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("gemini_AI_chat_proxy.html", {"request": request})

# @app.get("/send_message_sync")
def call_async_send_message_from_none_async_in_concurncy_way(user_id: str, msg: str):
    # Use the main loop to run the coroutine thread-safely
    print(f"call_async_send_message_from_none_async_in_concurncy_way: {user_id}, {msg}")
    future = asyncio.run_coroutine_threadsafe(send_message(user_id, msg), app.state.loop)
    result = future.result()  # This blocks until result is ready
    return result

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    websockets[user_id] = websocket
    user_queues[user_id] = UserQueue(queue=asyncio.Queue(), chat_sesion=None, chat_loop=None)
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

@app.get("/send_message")
async def send_message(user_id: str, msg: str = "Hello from FastAPI!"):
    websocket: WebSocket = websockets.get(user_id)
    queue: asyncio.Queue = user_queues.get(user_id).queue
    if websocket and queue:
        await websocket.send_text(msg)
        try:
            # Wait for the next message from the client (with a timeout)
            response = await asyncio.wait_for(queue.get(), timeout=10)
            # print(f"Received response from {user_id}: {response}")
            return {"message": f"Sent '{msg}' to {user_id}, received: {response}"}
        except asyncio.TimeoutError:
            return {"error": f"No response from client {user_id} within timeout"}
    else:
        return {"error": f"No WebSocket client connected for user_id {user_id}"}

async def loop2(user_id, prompt, main_loop: AbstractEventLoop):
    loop2_loop = asyncio.get_running_loop()
    print(f"loop2 is using loop: {id(loop2_loop)}")

    chat_auto = user_queues.get(user_id).chat_sesion
    # stream = await chat_auto.send_message_async("user_id: "+user_id + ", query: "+prompt)
    async for chunk in await chat_auto.send_message_async("user_id: "+user_id + ", query: "+prompt):
        # yield chunk.text
        main_loop.call_soon_threadsafe(shared_queue.put_nowait, chunk.text)
    main_loop.call_soon_threadsafe(shared_queue.put_nowait, None)

def run_stream_loop2_in_thread(user_id, prompt, main_loop):
    global chat_loop
    loop = None
    if chat_loop:
        loop = chat_loop
    else:
        loop = asyncio.new_event_loop()
        chat_loop = loop
    if not user_queues[user_id].chat_sesion: # not hasattr(user_queues[user_id], 'chat_sesion'):
        user_queues[user_id].chat_sesion = app.state.model.start_chat(enable_automatic_function_calling=True)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop2(user_id, prompt, main_loop)) # this event loop is elready running error
    # new_loop.close()

async def generate_stream(user_id: str, prompt: str):
    loop1_loop = asyncio.get_running_loop()
    # print(f"loop1 is using loop: {id(loop1_loop)}")

    # Start producer in a separate thread with its own loop
    t = threading.Thread(target=run_stream_loop2_in_thread, args=(user_id, prompt, loop1_loop))
    t.start()

    while True:
        item = await shared_queue.get()
        if item is None:
            break
        yield item
        # print(f"loop1: received {item}")

    t.join()
    print("loop1: done")

@app.post("/stream")
async def stream_content(query_data: PromptRequest = Body(...)):
    # Convert to list of dicts
    return StreamingResponse(generate_stream( query_data.user_id, query_data.prompt),

                              media_type="text/event-stream")

@app.get("/models")
def get_models():
    models = genai.list_models()
    models_list = []
    for m in models:
        # Check if the model supports the standard 'generateContent' method
        if 'generateContent' in m.supported_generation_methods:
            models_list.append(m.name[7:])
    return JSONResponse(content=models_list)

@app.get("/set_model")
def set_model(module_name: str):
    app.state.model = genai.GenerativeModel(
        model_name=module_name,
        tools=tools,
        # system_instruction="use in your answer this url content: https://testsmanager.com",
    )
    return JSONResponse(content={"model": module_name})

@app.get("/live")
def live():
    return JSONResponse(content={"status": "Live"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=7000) # host="0.0.0.0" listning to all interfaces
