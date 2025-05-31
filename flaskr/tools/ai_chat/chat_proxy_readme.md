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

// docs
# in production swagger https://testsmanager.com:12443/docs#
# in dev swagger http://127.0.0.1:7000/docs#

# in production fastAPI https://testsmanager.com:12443/redoc
# in dev http://127.0.0.1:7000/redoc

# in production schema https://testsmanager.com:12443/openapi.json
# in dev schema http://127.0.0.1:7000/openapi.json
