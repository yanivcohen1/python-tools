rem cmd /c start ollama_serve.bat
cmd /c start cmd /c ollama serve
cmd /c start http://localhost:8000/ollama_chat_all.html
python -m http.server 8000