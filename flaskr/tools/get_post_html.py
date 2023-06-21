import requests

URL = "http://www.google.com/about.html"
URL_PARAMS = "?firstname=John&lastname=Doe"
URL += URL_PARAMS # url parms

response = requests.get(URL)
print("get:", response.text[:7])

postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
resp = requests.post(URL, data=postdata) # post body params
print('post:', resp.text[:7])
