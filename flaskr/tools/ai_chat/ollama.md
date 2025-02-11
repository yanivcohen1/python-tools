## **Solution 1: Use Nginx as a Reverse Proxy**  
If you're running **Ollama** on a server, you can configure **Nginx** to allow CORS.  

### **Steps:**  
1. Install Nginx if you haven’t already:  
   ```sh
   sudo apt update && sudo apt install nginx -y
   ```
2. Edit the Nginx config file:  
   ```sh
   sudo nano /etc/nginx/sites-available/default
   ```
3. Add the following configuration:
   ```nginx
   server {
    listen 81;

    location / {
        proxy_pass http://127.0.0.1:11434;  # Ollama backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Enable CORS
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';

        # Handle OPTIONS requests properly
        if ($request_method = OPTIONS) {
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            return 204;
        }

        # ✅ Enable streaming responses
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';

        # ✅ Ensure WebSockets work (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
  }
   ```
4. Save and exit (`Ctrl + X`, then `Y`, then `Enter`).  
5. Restart Nginx:  
   ```sh
   sudo systemctl restart nginx
   ```

Now, **CORS is enabled**, and you can make requests from other origins. 🎉  
