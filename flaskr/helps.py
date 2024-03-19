# How to see the list of methods attached to an objects?
name='Michaela'
print(dir(name)) # gives the list of methods attached to the variable "name"
print(help(str)) # gives explanations about all the methods of the object "str" (string)
print(help(str.lower)) # gives explanations about the method "lower"

# print all evleble models
help('modules')
import os
print("-------------str------------------")
str(os.path)
print("-------------fun help------------------")
help(os.path)
print("-------------module help------------------")
help(os)
# help(module.funName)
# help(class.funName)
# obj = class()
# str(obj)
