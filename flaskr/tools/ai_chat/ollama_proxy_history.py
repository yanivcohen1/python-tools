from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn
from typing import Dict, List
import uuid

app = FastAPI()

# In-memory storage for user conversation histories
user_histories: Dict[str, List[Dict[str, str]]] = {}

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    user_id: str

@app.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_id = request.user_id
    if not user_id:
        # Generate a new user ID if not provided
        user_id = str(uuid.uuid4())
    user_msg = request.message

    # Check if this is a new user
    is_new_user = user_id not in user_histories
    if is_new_user:
        # Initialize history for new users
        user_histories[user_id] = []

    # Append user message to history
    user_histories[user_id].append({"role": "user", "content": user_msg})

    # Build prompt from history
    prompt_lines = []
    for msg in user_histories[user_id]:
        speaker = "User" if msg["role"] == "user" else "Assistant"
        prompt_lines.append(f"{speaker}: {msg['content']}")
    prompt_lines.append("Assistant:")
    full_prompt = "\n".join(prompt_lines)
    # this is the prompt format for the model
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

    # Append assistant reply to history
    user_histories[user_id].append({"role": "assistant", "content": assistant_reply})

    return ChatResponse(reply=assistant_reply, user_id=user_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
