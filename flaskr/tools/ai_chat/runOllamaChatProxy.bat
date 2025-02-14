rem cmd /c start ollama_serve.bat
cmd /c start cmd /c ollama serve
cmd /c start ollama_chat_proxy.html
python ollama_proxy_stream.py