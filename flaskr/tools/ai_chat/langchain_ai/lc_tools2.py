# 1. Install dependencies
#    pip install -U langgraph langchain-openai langchain-ollama semantic-router

from langchain.tools import Tool
# from langchain_ollama.llms import OllamaLLM
# from langchain_community.chat_models import ChatOllama
from langchain_ollama.chat_models import ChatOllama
from langgraph.prebuilt import create_react_agent

# 2. Define your “tools” as Python callables:
def calculator(expr: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Calculation error: {e}"

def weather(city: str) -> str:
    """Return fake weather info for demo purposes."""
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

# 3. Spin up your Ollama‑powered LLM
llm = ChatOllama(
    model="mistral", #  gemma3:4b deepseek-coder-v2:16b
    # api_key="ollama",
    # base_url="http://localhost:11434/v1",
)

# 4. Bind the tools and build a ReAct agent graph
llm_with_tools = llm.bind_tools(tools)
agent = create_react_agent(llm_with_tools, tools)

# 5. Invoke the agent
for chunk in agent.stream({
    "messages": [("user", "What's the weather in Cairo and what's 42 divided by 7?")]
}, stream_mode="messages"):
    if chunk[0].content:
        print(chunk[1]["langgraph_node"],':', chunk[0].content, end="\n")

# 6. Print out the step‑by‑step reasoning and final answer
#for msg in response["messages"]:
#    print(msg.content)
