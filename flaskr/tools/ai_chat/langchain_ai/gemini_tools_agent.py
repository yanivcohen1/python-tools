import os
import google.generativeai as genai
from google.generativeai import types

# --- Configuration ---
# Set your API key as an environment variable or directly here.
# It's recommended to use environment variables for security.
# os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# For this example, let's use a placeholder if the API key is not set.
# In a real application, you MUST provide a valid API key.

try:
    genai.configure(api_key="AIzaSyB2GXiEd1eV95qPkFMUaz8vndME1cYFByk")
    # genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except Exception as e:
    print(f"API Key not found. Please set the GEMINI_API_KEY environment variable. Error: {e}")
    print("Using a placeholder API key for demonstration purposes. This will likely fail to connect to the API.")
    genai.configure(api_key="YOUR_API_KEY_PLACEHOLDER")


# --- 1. Define your functions that the model can call ---

# It's good practice to use type hints and docstrings,
# as the model uses this information to understand the function.

def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """
    Get the current weather in a given location.

    Args:
        location (str): The city and state, e.g., "San Francisco, CA" or a zip code.
        unit (str): The temperature unit, either "celsius" or "fahrenheit". Defaults to "celsius".

    Returns:
        dict: A dictionary containing the location, temperature, unit, and a brief forecast.
    """
    print(f"PYTHON: Called get_current_weather(location='{location}', unit='{unit}')")
    # In a real application, you would call a weather API here.
    # For this example, we'll return mock data.
    if "tokyo" in location.lower():
        return {
            "location": location,
            "temperature": "15",
            "unit": unit,
            "forecast": "Cloudy with a chance of rain.",
        }
    elif "london" in location.lower():
        return {
            "location": location,
            "temperature": "10" if unit == "celsius" else "50",
            "unit": unit,
            "forecast": "Mostly sunny.",
        }
    else:
        return {
            "location": location,
            "temperature": "22" if unit == "celsius" else "72",
            "unit": unit,
            "forecast": "Pleasant weather.",
        }

# --- 2. Initialize the Generative Model with tools ---

# Specify the model you want to use.
# Replace 'gemini-2.0-flash' with the specific model version you intend to use if different.
# As of early 2025, 'gemini-2.0-flash' is a valid model identifier for models supporting tool use.
# Other models like 'gemini-1.5-flash-latest' or specific versions like 'gemini-2.0-flash-001' can also be used.
model_name = "gemini-2.0-flash-thinking-exp" # "gemini-2.0-flash" # Or a more specific version like 'models/gemini-2.0-flash-001'

# Create a list of tools. Each tool is derived from a Python function.
# The SDK inspects the function's name, docstring, parameters, and type annotations.
tools = [get_current_weather]

available_tools = {
    "get_current_weather": get_current_weather,
}
model = genai.GenerativeModel(
    model_name=model_name,
    tools=tools,
    # You can also specify tool_config for more control, e.g.,
    # tool_config=types.ToolConfig(
    #     function_calling_config=types.FunctionCallingConfig(
    #         mode=types.FunctionCallingConfig.Mode.AUTO # or ANY or NONE
    #     )
    # )
)

# --- 3. Start a chat session (optional, but good for conversational context) ---
# Alternatively, you can use model.generate_content() for single-turn interactions.
chat = model.start_chat(enable_automatic_function_calling=False) # Disable automatic calling for manual demonstration

# --- 4. Send a prompt that might trigger a function call ---
prompt = "What's the weather like in Tokyo today and can you give it to me in Fahrenheit?"
print(f"USER: {prompt}")

response = chat.send_message(prompt)
print(f"MODEL (Initial Response Parts): {response.parts}")

# --- 5. Process the model's response for function calls ---

# The loop handles potential multiple function calls or follow-up calls by the model.
while response.candidates[0].content.parts[0].function_call:
    function_call_part = response.candidates[0].content.parts[0]
    fc = function_call_part.function_call
    function_name = fc.name
    function_args = dict(fc.args) if fc.args else {}

    print(f"MODEL: Wants to call function '{function_name}' with arguments: {dict(function_args)}")

    # --- 6. Execute the function if it's one you've defined ---
    if function_name in available_tools:
        tool_function = available_tools[function_name]
    # if function_name == "get_current_weather":
        # Call your Python function
        api_response_data = tool_function(**function_args)
        #    location=function_args['location'],
        #    unit=function_args.get('unit', 'celsius') # Handle optional args
        #)

        # --- 7. Send the function's result back to the model ---
        print(f"PYTHON: Executed function. Result: {api_response_data}")

        # Construct the FunctionResponse part
        function_response_part = {
            "function_response": {
                "name": function_name,
                "response": {"content": api_response_data}  # The API expects the response to be under a 'content' key or be a simple value.
            }
        }

        # Send the function response back to the model
        response = chat.send_message(function_response_part)
        print(f"MODEL (After Function Result Parts): {response.parts}")

    else:
        print(f"ERROR: Model tried to call an unknown function: {function_name}")
        # Handle unknown function call (e.g., send an error message back to the model)
        error_response_part = {
            "function_response": {
                "name": function_name,
                "response": {"error": f"Unknown function: {function_name}"}
            }
        }
        response = chat.send_message(error_response_part)
        print(f"MODEL (After Error Parts): {response.parts}")
        break # Exit loop if function is unknown

# --- 8. Get the final response from the model ---
# After all function calls are resolved (or if no function call was made initially),
# the model will provide a final textual response.
final_response_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
if final_response_text:
    print(f"MODEL (Final Text Response): {final_response_text}")
else:
    print("MODEL: Did not provide a final text response after function calls.")

# Example with automatic function calling (simpler for many cases)
print("\n--- EXAMPLE WITH AUTOMATIC FUNCTION CALLING ---")
chat_auto = model.start_chat(enable_automatic_function_calling=True)
prompt_auto = "What's the weather like in London in Celsius?"
print(f"USER: {prompt_auto}")
response_auto = chat_auto.send_message(prompt_auto)
print(f"MODEL (Final Text Response with Auto FC): {response_auto.text}")
