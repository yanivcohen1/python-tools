import json
# python dictionary
z = {"age":30, "last":{"name": "cohen"}, "first":[{"name":"yaniv"}, {"age":30}]}
# python parse to JSON staring
x = json.dumps(z)
print(x) # print '{"age":30, "last":{"name": "cohen"}, "first":[{"name":"yaniv"}, {"age":30}]}'

# python parse x to dictionary:
y = json.loads(x)

# the result is a Python dictionary:
print(y["first"][0]["name"]) # print yaniv
print(y["last"]["name"]) # print cohen

# javascript parse JSON string to JSON
# json = JSON.parse(JsonString)
# javascript pars JSON to JSON string to send it
# JsonString = JSON.stringify(json)