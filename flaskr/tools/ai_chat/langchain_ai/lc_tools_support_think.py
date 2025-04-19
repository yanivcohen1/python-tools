import logging
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.tools import Tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

# 1) Silence httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# 2) Simple token‑printer callback
class TokenPrinter(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)

cb_manager = CallbackManager([TokenPrinter()])

# 3) Define tools
def calculator(expr: str) -> str:
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"

def weather(city: str) -> str:
    data = {"cairo": "28°C, sunny", "london": "10°C, rainy", "new york": "15°C, cloudy"}
    return data.get(city.lower(), "Weather data unavailable")

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math operations. Input should be a valid Python expression."
    ),
    Tool(
        name="Weather",
        func=weather,
        description="Gives current weather for a city; input should be the city name."
    ),
]

# 4) Ollama LLM with streaming + our token‑printer
llm = ChatOllama(
    model="mistral",
    # api_key="ollama",
    # base_url="http://localhost:11434/v1",
    # streaming=True,
    # callback_manager=cb_manager,
)

# 5) Build the ReAct agent
agent = create_react_agent(llm.bind_tools(tools), tools)

# 6) Invoke with a system prompt that *forces* ReAct formatting
print("=== Agent reasoning trace ===")
# Replace agent.invoke(...) with agent.stream(...)
for chunk in agent.stream(
    {
        "messages": [
            ("system",
              "You are a ReAct agent. Always think step-by-step and emit lines prefixed with:\n"
              "  Thought: …\n"
              "  Action: …\n"
              "  Action Input: …\n"
              "  Observation: …\n"
              "Then at the end print:\n"
              "  Final Answer: …"
            ),
            ("user", "what is a cat and What's the weather in Cairo city and what's 42 divided by 7 and what is a dog?")
        ]
    },
    stream_mode="messages"   # only get the LLM’s token stream
):
    if chunk[0].content:
        print(chunk[0].content, end="\n")
