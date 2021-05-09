try:
    ser = 0/5
except Exception as inst:
    print("Error: " + inst.args[0])
try:
    ser = 5/0
except Exception as inst:
    print("Error: " + inst.args[0])
