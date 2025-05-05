# FastAPI (main.py)
from fastapi import FastAPI, Response, Body
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
# import asyncio
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

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

from typing import List, Literal

class Part(BaseModel):
    role: Literal["user", "model"] # assistant
    parts: List[str]

class PromptRequest(BaseModel):
    model: str
    prompt: List[Part]

class GeminiQueryData(BaseModel):
    model: str
    prompt: List[str] = []

def generate_stream(prompt: List[Part], model_name: str = 'gemini-2.0-flash-thinking-exp'):
    model = genai.GenerativeModel(model_name) # 'gemini-2.0-flash-thinking-exp')
    response = model.generate_content(prompt, stream=True)  # No await needed
    for chunk in response:  # Regular for loop, not async
        # print(chunk.text, end="")
        yield chunk.text

@app.post("/stream")
async def stream_content(query_data: PromptRequest = Body(...)):
    # Convert to list of dicts
    prompt = [p.model_dump() for p in query_data.prompt]
    return StreamingResponse(generate_stream( prompt,
                                  # ' use in your answer this url content: https://testsmanager.com',
                                  query_data.model),
                              media_type="text/event-stream")

@app.get("/models")
def models():
    models = genai.list_models()
    models_list = []
    for m in models:
        # Check if the model supports the standard 'generateContent' method
        if 'generateContent' in m.supported_generation_methods:
            models_list.append(m.name[7:])
    return JSONResponse(content=models_list)

@app.get("/live")
def live():
    return JSONResponse(content={"status": "Live"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000) # host="0.0.0.0" listning to all interfaces
