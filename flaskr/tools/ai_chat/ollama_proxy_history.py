from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import uvicorn
from typing import List, Dict
from fastapi.responses import FileResponse


app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

# Serve a simple HTML client
@app.get("/", response_class=FileResponse)
async def get_client():
    return FileResponse("templates/ollama_proxy_client.html")

# Request model now expects structured messages
class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    messages = request.messages

    # Reconstruct full prompt from messages
    prompt_lines = []
    for msg in messages:
        speaker = 'User' if msg['role'] == 'user' else 'Assistant'
        prompt_lines.append(f"{speaker}: {msg['content']}")
    prompt_lines.append('Assistant:')
    full_prompt = "\n".join(prompt_lines)
    # the full prompt should look like this but in json format:
    # User: Hi!
    # Assistant: Hello, how can I help you today?
    # User: What's the weather like?
    # Assistant:

    # Call Ollama API
    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(OLLAMA_URL, json=payload, timeout=60)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Ollama request failed: {e}")

    data = resp.json()
    assistant_reply = data.get("response")
    if not assistant_reply:
        raise HTTPException(status_code=500, detail="No response from Ollama")

    return ChatResponse(reply=assistant_reply)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
