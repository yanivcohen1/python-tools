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

# concatenate dict
dicts = {1: "2"}
dicts |= {3: "4"}
print(dicts)

# concatenate dict in dict
dicts = {1: "2"}
dicts["dict"] = {3: "4"}
print(dicts)

# concatenate tuple
tupl = (1, "2")
tupl += (3, "4")
print(tupl)

# concatenate tuple in tuple
tupl = (1, "2")
tupl = (tupl, 3, "4")
print(tupl)

# concatanet list
lists = [1, "2"]
lists += [3, "4"]
print(lists)

# concatanet list in list
lists = [1, "2"]
lists.extend([3, "4"])
print(lists)

# add index by key
def build_dict(seq, key):
        return dict((d[key], d) for (index, d) in enumerate(seq))

list_to_be_sorted = [{"name": "yan1", "val": 1}, {"name": "yan", "val": 0}, {"name": "yan2", "val": 2}]
newlist = build_dict(list_to_be_sorted, "name")
print(newlist)
print(newlist["yan"])# find in list by key

myDict = {1: "2", 3: "4", 4: "3", 2: "1", 0: "0"}
myKeys = list(myDict.keys())
myKeys.sort()
sorted_dict = {key: myDict[key] for key in myKeys}

print(sorted_dict)

from sortedcontainers import SortedDict
sd = SortedDict({'b': 2, 'c': -3, 'a': 1})
print("print from the start:", sd.peekitem(0)) #  from the start ('a', 1)
print("print from the end:", sd.popitem(index=-1))# from the end ('c', -3)
