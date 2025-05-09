@echo off

rem cmd /c start ollama_serve.bat
REM cmd /c start cmd /c ollama serve
REM cmd /c start http://localhost:8000/ollama_chat_local.html
REM python -m http.server 8000

:: Start the local HTML page
start "" "http://localhost:8000/ollama_chat_local.html"

:: Start the proxy HTML page
start "" "http://localhost:9000/ollama_chat_linux.html"

:: Start the Python HTTP server on port 9000
py -m http.server 8000

:: Keep the Command Prompt window open
@REM echo The Python HTTP server is running. Press CTRL+C to stop.
@REM pause
