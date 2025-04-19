from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_ollama.llms import OllamaLLM

# 1. Create a LangChain-compatible LLM using Ollama
llm = OllamaLLM(model="deepseek-coder-v2:16b")  # mistral you can also use "llama2", "gemma", etc.

# 2. Define tools the agent can use
def simple_calculator(query: str) -> str:
    try:
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def weather_tool(city: str) -> str:
    fake_data = {
        "new york": "15°C, cloudy",
        "london": "10°C, rainy",
        "cairo": "28°C, sunny"
    }
    return fake_data.get(city.lower(), "Weather data not available.")

tools = [
    Tool(
        name="Calculator",
        func=simple_calculator,
        description="Useful for math operations. Input should be a valid Python math expression."
    ),
    Tool(
        name="WeatherInfo",
        func=weather_tool,
        description="Gives current weather for a city. Input should be a city name."
    )
]

# 3. Initialize the agent with tools
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # uses ReAct reasoning pattern
    verbose=True
)

# 4. Ask the agent something
response = agent.invoke("What is the weather in Cairo and what's 42 divided by 7 and what is a dog?")
print(response)
