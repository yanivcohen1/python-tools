thislist = ["apple", "cherry", "banana"]
list2 = thislist.copy()
list2.append(2)
print(list2) # ['apple', 'cherry', 'banana', 2]
thislist.insert(len(thislist), "bif") # insert last element
thislist.append("bif1") # insert last element the same as above
thislist.pop(-1) # remove last element
thislist.pop() # remove last element the same as above
thislist.sort() 
print(thislist) # ['apple', 'banana', 'cherry']
list2.pop()
thislist.extend(list2)
for i in range(len(thislist)): print(thislist[i]) # thislist + list2
newlist = [x for x in thislist if "a" in x]
print(newlist) # ['apple', 'banana', 'apple', 'banana']
print(newlist[1:-2]) # ['banana'], remove the first and the 2 lasts resoults 
newlist.remove("banana")
print(newlist) # ['apple', 'apple', 'banana']
