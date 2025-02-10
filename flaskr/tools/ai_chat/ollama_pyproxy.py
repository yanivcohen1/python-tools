from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS

OLLAMA_URL = "http://localhost:11434"

@app.route('/v1/<path:endpoint>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(endpoint):
    if request.method == 'OPTIONS':
        return '', 204

    url = f"{OLLAMA_URL}/{endpoint}"
    response = requests.request(request.method, url, json=request.get_json())
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
