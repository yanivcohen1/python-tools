# single line if else assignment
a=2
result = a+1 if a > 1 else "is smaller"
print(result) # print 3
print('Alarm is ' + ("ON" if a < 1 else "OFF")) # print off

# single line if else statment
print("pass1") if a==2 else print("pass2") # print pass1

# single line if statment
if a==2: print("pass") # print pass

arry = [1, 2, 3, 4, 5]
# filter items and return multiply by 2
filterArry = [2*item for item in arry if item % 2 == 1]
print(filterArry) # print [2, 6, 10]

# in javascript
# var timeout = settings !== null ? settings.timeout : 1000; // single line if else assignment
# (a==2) ? alert("please give me") : alert("then give me a beer") // single line if else statment
# if (a==2) alert("please give me a lemonade") // single line if statment

# in java
# Object bar = foo.isSelected() ? foo : baz; // single line if else assignment
# (a==2) ? alert("please give") : alert("then give me a beer") // single line if else statment
# if (name == null) name = "N/A"; // single line if statment