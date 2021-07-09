import json

# some JSON:
x = '{"name":"John", "last":{"name": "cohen"}, "age":30, "first":[{"name":"yaniv"}, {"age":30}]}'
# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["first"][0]["name"]) # print yaniv
print(y["last"]["name"]) # print cohen