import json
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_ollama.llms import OllamaLLM

# 1. Create a LangChain-compatible LLM using Ollama
llm = OllamaLLM(model="deepseek-coder-v2:16b")  # mistral you can also use "llama2", "gemma", etc.

# 2. Define tools the agent can use
def simple_calculator(expr: str) -> str:
    try:
        result = eval(expr)
        return str(result)
    except Exception as e:
        return f"Error: {e}, expr: {expr}"

def weather_tool(city: str, format: str = "Celsius") -> str:
    fake_data = {
        "new york": "15°C, cloudy",
        "london": "10°C, rainy",
        "cairo": "28°C, sunny"
    }
    return fake_data.get(city.lower(), "Weather data not available.")

def weather_tool_input_parser(json_str: str) -> str:
    try:
        data = json.loads(json_str)
        city = data.get("city")
        format = data.get("format", "Celsius")
        return weather_tool(city, format)
    except Exception as e:
        return f"Invalid input format. Please provide JSON like {{'city': 'Paris', 'format': 'Fahrenheit'}}. Error: {e}, json is {json_str}"

tools = [
    Tool(
        name="Calculator",
        func=simple_calculator,
        description="Useful for math operations. Input should be a valid Python math expression."
    ),
    # Tool(
    #     name="WeatherInfo",
    #     func=weather_tool,
    #     description="Gives current weather for a city in Celsius. Input should be a city name."
    # ),
    Tool(
        name="WeatherInfoJSON",
        func=weather_tool_input_parser,
        description="Gives current weather for a city. Input should be a JSON string with 'city' and optional 'format' (Celsius or Fahrenheit)."
    )
]

# 3. Initialize the agent with tools
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # uses ReAct reasoning pattern
    verbose=True,
    # handle_parsing_errors=True
)

# 4. Ask the agent something
while True:
    print("\n-------------------------------")
    try:
        # response = agent.invoke("what is a cat and What is the weather in Cairo use WeatherInfo and what's 42 divided by 7 use Calculator?")
        response = agent.invoke("what is a cat and What is the weather in Cairo in Celsius and convert it to Fahrenheit?") # what's 42 divided by 7
        print(response['output'])
    except Exception as e:
        continue
    break
