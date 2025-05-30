// the service
sudo sh ~/run_ollama_proxy.sh

// restart service 
sudo systemctl restart run_ollama_proxy.service

// service log
journalctl -u run_ollama_proxy.service -f

// connect envirment
cd /home/yanivc/py/ollama_proxy/
. .venv/bin/activate

// pip install
pip install 'uvicorn[standard]'

// create requirements.txt
pip freeze > requirements.txt
