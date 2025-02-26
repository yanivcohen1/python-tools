# ollama commands
ollama -v
ollama -h
ollama ps
ollama list
ollama stop deepseek-r1:8b
ollama stop deepseek-coder-v2:16b

# stop all running models
papermill stop_all_modules.ipynb out.ipynb

# stop all running models
chmod +x stop_all_ollama.sh
# covner win to linux text format
sed -i 's/\r$//' stop_all_ollama.sh
# stop all models
./stop_all_ollama.sh
# in windows 

# start
ollama serve &
cd /home/yanivc/py/ollama/
. .venv/bin/activate
# cmd /c start ollama_chat_proxy.html
python ollama_proxy_stream.py

# start py server
python -m http.server 8000
localhost:8000/ollama_chat.html
