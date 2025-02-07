import ctypes
import json
import os

currentDir = os.path.join(os.path.dirname(__file__))
# Load the shared dll library win
lib = ctypes.CDLL(currentDir + '/jsonprocess.dll')
# Load the shared so library linux
# lib_linux = ctypes.CDLL(currentDir + '/ibjsonprocess.so')

# Define the argument and return types of the C function
lib.process_json.argtypes = [ctypes.c_char_p]
lib.process_json.restype = ctypes.c_char_p

# Example input JSON
input_json = json.dumps({"key": "value"})

# Call the C function
output_json = lib.process_json(input_json.encode('utf-8')).decode('utf-8')

# Print the output JSON
print(output_json)
