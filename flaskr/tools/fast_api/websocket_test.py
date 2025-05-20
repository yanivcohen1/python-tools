from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

templates_dir = "./flaskr/tools/fast_api/templates"
templates = Jinja2Templates(directory=templates_dir)
websockets = {}  # Maps user_id to websocke


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    websockets[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
        websockets.pop(user_id, None)


@app.get("/send_message")
async def send_message(request: Request, user_id: str, msg: str = "Hello from FastAPI!"):
    websocket: WebSocket = websockets.get(user_id)
    if websocket:
        await websocket.send_text(msg)
        data = await websocket.receive_text()
        print(f"Received from client {user_id}: {data}")
        return {"message": f"Message '{msg}' sent to WebSocket client {user_id}"}
    else:
        return {"error": f"No WebSocket client connected for user_id {user_id}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=7000)  # host="0.0.0.0"
