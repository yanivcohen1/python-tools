# start server
cmd /c start ollama serve
cmd /c start http://localhost:8000/ollama_chat.html
python -m http.server 8000

# all this in 
runOllamaChat.bat
