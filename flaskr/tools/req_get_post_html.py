import requests
import json

headers_json = {"Content-Type": "application/json; charset=utf-8"}

def get(URL_WithParams, headers):
    response = requests.get(URL_WithParams, headers=headers)
    # print("get:", response.text[:7])
    return response.text

def post(URL_WithParams, postdata, headers):
    # postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
    resp = requests.post(URL_WithParams, data=postdata, headers=headers) # post body params
    # print('post:', resp.text[:7])
    return resp.text# return as text

def post_json(URL_WithParams, json, headers):
    # postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
    resp = requests.post(URL_WithParams, json=json, headers=headers) # post body params
    # print('post:', resp.text[:7])
    return resp.json()# return as json


if __name__ == '__main__':
    # get
    url = "http://ip-api.com/json/24.48.0.1"
    headers_json = {"Content-Type": "application/json; charset=utf-8"}
    resp = get(url, headers_json)
    print(resp)
    # post
    postData = {
                "Id": 78912,
                "Customer": "Jason Sweet",
                "Quantity": 1,
                "Price": 18.00
                }
    url = "https://httpbin.org/post"
    resp = post(url, json.dumps(postData), headers_json)
    resp = post_json(url, postData, headers_json)
    # json1 = json.loads(resp["json"])
    print(resp)
