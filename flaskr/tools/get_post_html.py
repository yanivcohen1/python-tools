import requests

URL = "http://www.google.com/about.html"
URL_PARAMS = "?firstname=John&lastname=Doe"
URL += URL_PARAMS # url parms

response = requests.get(URL)
print("get:", response.text[:7])

postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
resp = requests.post(URL, data=postdata) # post body params
print('post:', resp.text[:7])

# with socket
import socket
# get or post with socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("www.google.com", 80))
# get for url about.html
sock.send(b"GET /about.html HTTP/1.1\r\nHost:www.example.com\r\n\r\n")
response = sock.recv(4096)
sock.close()
print(response.decode())
