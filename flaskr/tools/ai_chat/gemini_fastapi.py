# FastAPI (main.py)
from fastapi import FastAPI, Response
# FastAPI (main.py)
from fastapi import FastAPI, Response, Body
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
# import asyncio
from pydantic import BaseModel

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
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp') # gemini-2.0-flash

class QueryData(BaseModel):
    query: str

def generate_stream(query: str):
    response = model.generate_content(query, stream=True)  # No await needed
    for chunk in response:  # Regular for loop, not async
        # print(chunk.text, end="")
        yield chunk.text

@app.post("/stream")
async def stream_content(query_data: QueryData = Body(...)):
    return StreamingResponse(generate_stream(query_data.query), media_type="text/event-stream")

@app.get("/live")
def live():
    return Response(content="Live", media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000) # host="0.0.0.0" listning to all interfaces
