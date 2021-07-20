thislist = ["banana", "cherry", "apple"]
list2 = thislist.copy()
list2.append(2)
print(list2) # ['banana', 'cherry', 'apple', 2]
thislist.insert(len(thislist), "bif") # insert last element
thislist.append("bif1") # insert last element the same as above
thislist.pop(-1) # remove last element
thislist.pop() # remove last element the same as above
thislist.sort() 
print(thislist) # ['apple', 'banana', 'cherry']
list2.pop()
thislist.extend(list2) # same as zip
for i in range(len(thislist)): print(thislist[i]) # thislist + list2
newlist = [x for x in thislist if "a" in x]
print(newlist) # ['apple', 'banana', 'banana', 'apple']
print(newlist[1:-2]) # ['banana'], remove the first and the 2 lasts resoults 
newlist.remove("apple")
print(newlist) # ['banana', 'banana', 'apple'] remove the first item he find
# filter
print(list(filter(lambda a: a != 'banana', newlist))) # ['apple'] remove all not only first item
print(newlist.index('banana')) # 0, the first he find
# map
print([i for i, x in enumerate(newlist) if x == "banana"]) # [0, 1] find all not only first item
# reduce
from functools import reduce 
print( reduce((lambda x, y: x * y), [1, 2, 3, 4]) ) # print 24 - 1*2*3*4