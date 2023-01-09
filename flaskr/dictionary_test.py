# filter(key>1) and map(val/10) the result is list: [2.0, 3.0]
dic = {1:10, 2:20, 3:30}
print([dic[key] / 10 for key in dic if key>1]) # [2.0, 3.0]
print({key: dic[key] /10 for key in dic if key>1}) # {2: 2.0, 3: 3.0}
firstKey = next(iter(dic))
print('first key is:', firstKey, ' first val is:', dic[firstKey]) # first key is: 1  first val is: 10

thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "nest": {"inner": "innerval"},
  "arry": [1, 2, 3]
}
if 'brand' in thisdict :
    print("brand: ", thisdict["brand"])
del thisdict['brand'] # del brand
print("brand deleted: ", not ('brand' in thisdict))
print("numbers of items: ",len(thisdict.items()))
print("first of item: "+ list(thisdict.keys())[0] + ': ' +list(thisdict.values())[0] )
print("the nested items: ", thisdict["nest"]["inner"])
print("the arry secend item: ", thisdict["arry"][1])
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
