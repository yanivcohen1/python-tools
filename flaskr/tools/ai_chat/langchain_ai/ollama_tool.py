import json
import ollama
from ollama import Tool
from typing import Callable, Dict, Any

model="qwen3:1.7b"

# Define a Python tool function
def get_current_weather(location: str, unit: str) -> dict:
    """
    Fetch current weather data for a given location.
    Replace this stub with an actual API call as needed.
    Parameters:
        location: City name, e.g., 'Tel Aviv'
        unit: Temperature unit, either 'Celsius' or 'Fahrenheit'
    """
    # Stubbed temperature in Celsius
    temp_c = 22.0
    if unit == "Fahrenheit":
        # Convert °C to °F
        temp = round((temp_c * 9/5) + 32, 1)
        temp_str = f"{temp}°F"
    else:
        temp_str = f"{temp_c}°C"

    return {
        "location": location,
        "temperature": temp_str,
        "condition": "Partly Cloudy"
    }

def calculate(expression: str) -> dict:
    """
    Perform a simple arithmetic calculation.
    """
    try:
        result = eval(expression, {'__builtins__': None}, {})
    except Exception as e:
        return {"expression": expression, "error": str(e)}
    return {"expression": expression, "result": result}

# Map tool names to function references
available_functions = {"get_current_weather": get_current_weather,
                        "calculate": calculate
                      }

# JSON schema metadata list for tools
tools_schema = [
  {'type': 'function',
    'function': {
        "name": "get_current_weather",
        "description": "Get the current weather for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name, e.g., Tel Aviv"},
                "unit": {"type": "string", "enum": ["Celsius", "Fahrenheit"], "description": "Temperature unit"}
            },
            "required": ["location", "unit"]
        }
    }},
    {'type': 'function',
    'function': {
        "name": "calculate",
        "description": "Compute a simple arithmetic expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Arithmetic expression, e.g., '15 + 27'"}
            },
            "required": ["expression"]
        }
    }}
]

# 1. Send a user message and register tools with Ollama
query = "What's the weather in Tel Aviv in Fahrenheit and what's 15 + 27?"
initial_response = ollama.chat(
    model=model,  # or your Ollama-pulled model llama3.2
    messages=[{"role": "user", "content": query}],
    tools=tools_schema,  # pass the actual functions
)

# 2. Inspect any tool calls in the model's response
for tool_call in initial_response.message.tool_calls or []: # pylint: disable=no-member
    func_name = tool_call.function.name
    func_args = tool_call.function.arguments

    # Execute the requested tool if available
    if func_name in available_functions:
        print("-" * 20)
        print(f"Executing tool: {func_name} with args: {func_args}")
        result = available_functions[func_name](**func_args)
        print(f"Tool result: {result}")
        print("-" * 20)
    else:
        raise ValueError(f"Requested tool '{func_name}' is not available.")

    # 3. Feed the tool result back into a follow-up chat
    followup_response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": query},
            {"role": "assistant", "content": initial_response.message.content}, # pylint: disable=no-member
            {"role": "tool", "name": func_name, "content": json.dumps(result)},
        ],
    )

    # 4. Final assistant reply incorporating the tool output
    print(followup_response.message.content) # pylint: disable=no-member
    # This will print the final response from the assistant after processing the tool output.
    # 5. Print out the step‑by‑step reasoning and final answer
    # for msg in response["messages"]:
    #    print(msg.content)

print("-" * 20)
print("End of tool execution")
print(initial_response.message.content) # pylint: disable=no-member
print("-" * 20)
