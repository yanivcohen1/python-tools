import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="./flaskr/tools/fast_api/templates")
websockets = {}  # Maps user_id to websocket
user_queues = {}  # Maps user_id to asyncio.Queue

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    websockets[user_id] = websocket
    user_queues[user_id] = asyncio.Queue()
    try:
        while True:
            data = await websocket.receive_text()
            # Put the received data into the user's queue
            await user_queues[user_id].put(data)
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
        websockets.pop(user_id, None)
        user_queues.pop(user_id, None)

@app.get("/send_message")
async def send_message(user_id: str, msg: str = "Hello from FastAPI!"):
    websocket = websockets.get(user_id)
    queue = user_queues.get(user_id)
    if websocket and queue:
        await websocket.send_text(msg)
        try:
            # Wait for the next message from the client (with a timeout)
            response = await asyncio.wait_for(queue.get(), timeout=10)
            return {"message": f"Sent '{msg}' to {user_id}, received: {response}"}
        except asyncio.TimeoutError:
            return {"error": f"No response from client {user_id} within timeout"}
    else:
        return {"error": f"No WebSocket client connected for user_id {user_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=7000) # host="0.0.0.0"
