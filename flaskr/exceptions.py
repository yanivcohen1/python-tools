try:
    ser = 0/5
except Exception as inst:
    print("Error: " + inst.args[0])
try:
    ser = 5/0
except Exception as err:
    print("Error: " + err.args[0])
    raise Exception(err.args[0])
