# 1. Install dependencies
#    pip install -U langgraph langchain-openai langchain-ollama semantic-router
import json
from langchain.tools import Tool
from langchain_ollama.llms import OllamaLLM
# from langchain_community.chat_models import ChatOllama
from langchain_ollama.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from RGA.pdf_vector import ask_PDF

table_name ="alice.pdf"
search_result = ""

# 2. Define your “tools” as Python callables:
def calculator(expr: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Calculation Error: {e}, expr: {expr}"

def weather_tool(city: str, format: str = "Celsius") -> str:
    fake_data = {
        "new york": "15°C, cloudy",
        "london": "10°C, rainy",
        "cairo": "28C, sunny",
        "paris": "12",# °C, windy
        "tokyo": "20°C, clear",
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

def search(query: str) -> str:
    """Evaluate a math expression."""
    response = ""
    try:
        global search_result
        if search_result:
            for res in search_result:
                response += res.page_content
        return response
    except Exception as e:
        return f"Search Error: {e}, query: {search_result}"

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math operations. Input should be a valid Python math expression."
    ),
    Tool(
        name="WeatherInfoJSON",
        func=weather_tool_input_parser,
        description='''Gives current weather for a city.
                        Input should be a JSON string with 'city' and optional 'format' (Celsius).
                        for example: {"city": "london","format": "Celsius"}'''
    ),
    Tool(
        name="DuckDuckGo Search",
        func=search,
        description="Useful for when you need to answer questions to Search info. Input should be a search query.",
    )
]

# 3. Spin up your Ollama‑powered LLM
llm = OllamaLLM(
    model="deepseek-coder-v2:16b", # mistral  gemma3:4b
    # api_key="ollama",
    # base_url="http://localhost:11434/v1",
)

# https://www.promptingguide.ai/techniques/react
# both reasoning traces and task-specific actions
template_reAct = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}] or from {chat_history}, otherwise "I don't know"
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
# agent_scratchpad helps by inserting the history of tool calls, observations, and thoughts back into the prompt.
# Action: the action to take, should be one of [{tool_names}] if possible, otherwise "I don't know"

prompt = PromptTemplate.from_template(template_reAct)

# 4. Bind the tools and build a ReAct agent graph
# llm_with_tools = llm.bind_tools(tools)
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True, # Set to True to see the agent's thought process
    # handle_parsing_errors=True # Helps if the LLM output isn't perfectly formatted
)
# 5. Invoke the agent
chat_history = ""
while True:
    print("\n-------------------------------")
    try:
        # response = agent.invoke("what is a cat and What is the weather in Cairo use WeatherInfo and what's 42 divided by 7 use Calculator?")
        question = input("Ask your question (q to quit): ") # who is Alice?
        if question == "q":
            break
        if question == "":
            question = '''who is Alice, What is the weather in Paris in Celsius and convert it to Fahrenheit?'''
            print("question is: ", question, "\n")
        search_result = ask_PDF(table_name, 5).invoke(question)
        response = agent_executor.invoke({"input": question, "chat_history": chat_history})
        if 'Agent stopped due to iteration limit or time limit' in response['output']:
            continue
        print(response['output'])
        chat_history += question
    except Exception as e:
        continue
    # break
