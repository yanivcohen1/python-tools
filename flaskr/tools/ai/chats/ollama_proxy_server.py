from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
import json
import logging

app = Flask(__name__)
CORS(app)

# Configuration
OLLAMA_SERVER_URL = "http://localhost:11434"  # Your Ollama server URL
ALLOWED_ORIGINS = ["http://your-frontend-domain"]  # Your frontend domain(s) or "*" (less secure)
OLLAMA_CHAT = "/v1/chat/completions"

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route(f'/{OLLAMA_CHAT}', methods=['POST'])
def ollama_proxy():
    # origin = request.headers.get('Origin')

    # if origin not in ALLOWED_ORIGINS and ALLOWED_ORIGINS != ["*"]:
    #     logger.warning(f"CORS request from unauthorized origin: {origin}")
    #     return jsonify({"error": "CORS Forbidden"}), 403

    try:
        data = request.get_json()
        logger.debug(f"Received request data: {data}")

        ollama_response = requests.post(
            f"{OLLAMA_SERVER_URL}{OLLAMA_CHAT}",  # Correct Ollama endpoint
            json=data,
            stream=True
        )

        def generate_response():
            for chunk in ollama_response.iter_lines():
                if chunk:
                    try:
                        decoded_chunk = chunk.decode('utf-8')
                        # Check if it's a data line or a keep-alive line
                        if decoded_chunk.startswith("data: "):
                            json_chunk = json.loads(decoded_chunk[6:]) # Remove "data: " prefix
                            yield f"data: {json.dumps(json_chunk)}\n\n"
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON chunk: {e}, Chunk: {decoded_chunk}")
                        yield f"data: {json.dumps({'error': 'Error decoding JSON'})}\n\n"
                        break # Stop sending further chunks
                    except Exception as e: # Catch any other error
                        logger.error(f"An unexpected error occurred: {e}, Chunk: {decoded_chunk}")
                        yield f"data: {json.dumps({'error': 'An unexpected error occurred'})}\n\n"
                        break


        response = make_response(generate_response(), 200)
        response.headers['Content-Type'] = 'text/event-stream'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Connection'] = 'keep-alive'

        response.headers['Access-Control-Allow-Origin'] = "*" # origin if ALLOWED_ORIGINS != ["*"] else "*"
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

        return response

    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Ollama server: {e}")
        return jsonify({"error": "Error communicating with Ollama server"}), 500
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

def handle_options_request(origin): # Helper function for OPTIONS
    response = make_response("", 200)
    add_cors_headers(response, origin)
    return response

def add_cors_headers(response, origin): # Helper function for CORS
    response.headers['Access-Control-Allow-Origin'] = "*" # origin if ALLOWED_ORIGINS != ["*"] else "*"
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Add other methods as needed
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Add other headers as needed

@app.route('/<path:endpoint>', methods=['GET', 'POST', 'OPTIONS'])  # For non-streaming
def ollama_proxy_non_stream(endpoint):
    origin = request.headers.get('Origin')

    # if origin not in ALLOWED_ORIGINS and ALLOWED_ORIGINS != ["*"]:
    #     logger.warning(f"CORS request from unauthorized origin: {origin}")
    #     return jsonify({"error": "CORS Forbidden"}), 403

    try:
        url = f"{OLLAMA_SERVER_URL}/{endpoint}"  # Construct the full URL
        logger.debug(f"Forwarding request to: {url}")

        if request.method == 'POST':
            data = request.get_json()
            ollama_response = requests.post(url, json=data)
        elif request.method == 'GET':
            ollama_response = requests.get(url, params=request.args)  # Forward query params
        else:  # OPTIONS
            return handle_options_request(origin) # Reuse OPTIONS logic

        response = make_response(ollama_response.content, ollama_response.status_code)
        response.headers['Content-Type'] = ollama_response.headers.get('Content-Type')  # Preserve content type

        add_cors_headers(response, origin) # Reuse CORS logic

        return response

    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Ollama server: {e}")
        return jsonify({"error": "Error communicating with Ollama server"}), 500
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
