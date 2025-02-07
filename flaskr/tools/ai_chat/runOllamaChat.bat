cmd /c start ollama_serve.bat
cmd /c start http://localhost:8000/ollama_chat.html
python -m http.server 8000