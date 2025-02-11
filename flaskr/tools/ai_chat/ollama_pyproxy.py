# add "proxy" to path

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

OLLAMA_URL = "http://localhost:11434"

def stream_response(response):
    """Generator to stream response chunks from Ollama."""
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            yield chunk


# for stream   : http://localhost:5000/v1/chat/completions
# or non stream: http://localhost:5000/v1/models
@app.route('/<path:endpoint>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(endpoint):
    """Proxies requests to the Ollama API, supporting both streaming and non-streaming."""

    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        return '', 204

    url = f"{OLLAMA_URL}/{endpoint}"
    try:
        json = request.get_json() # if request.is_json else None
    except:
        json = None

    # Forward request to Ollama
    with requests.request(
        method=request.method,
        # headers = request.headers,
        url=url,
        json=json,
        stream=True  # Enable streaming
    ) as response:
        # Check if the request is for a streaming response
        is_streaming = request.json.get("stream", False) if request.is_json else False

        if is_streaming:
            return Response(stream_response(response), content_type=response.headers.get('Content-Type', 'application/json'))
        else:
            return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5000, threaded=True)
