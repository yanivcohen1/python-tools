# python download file script
import requests

session = requests.Session()
url = 'http://google.com/favicon.ico'
cookies = {'cookies_are': 'working'}
myJson = {'somekey': 'somevalue'}
headers={"Content-Type":"json"}
response = session.post(url, allow_redirects=True, headers=headers, cookies=cookies, json = myJson)
open('google.ico', 'wb').write(response.content) # download file
print("print the cookies", session.cookies.get_dict())
print("print the headers", response.headers)
print("json of response", response.json)
print("text of response", response.text)
