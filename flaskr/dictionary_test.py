thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
if 'brand' in thisdict :
    print("brand: ", thisdict["brand"])
print("numbers of items: ",len(thisdict.items()))
print("first of item: "+ list(thisdict.keys())[0] + ': ' +list(thisdict.values())[0] )
# loop by order
for key in thisdict:
  print(key, ':', thisdict[key])
# loop by values
for val in thisdict.values():
  print('val: ', val)
# loop by keys
for key in thisdict.keys():
  print('key: ', key)
# loop by key value
for key, val in thisdict.items():
  print(key, ':', val)