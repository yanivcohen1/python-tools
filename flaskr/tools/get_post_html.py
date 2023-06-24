import requests

URL = "http://www.google.com/about.html"
URL_PARAMS = "?firstname=John&lastname=Doe"
URL += URL_PARAMS # url parms

response = requests.get(URL)
print("get:", response.text[:7])

postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
resp = requests.post(URL, data=postdata) # post body params
print('post:', resp.text[:7])

# get or post with socket
import socket

# get http://ip-api.com/json/24.48.0.1
HOST = "ip-api.com"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 80))
# get for url about.html
PATH = "json/24.48.0.1"
URL = "GET /"+PATH+" HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n"
# sock.send(b"GET /about.html HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n")
sock.send(URL.encode())
response = sock.recv(4096)
print(response.decode())
sock.close()
