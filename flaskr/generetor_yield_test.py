def rev_str(my_str):
    length = len(my_str)
    # reverse the string  range(start_from_end, to 0 include, in step -1)
    for i in range(length - 1, -1, -1): 
        yield my_str[i]


# For loop to reverse the string
for char in rev_str("hello"):
    print(char)

def myGenerator(i1):
    i = 1
    def next():
        nonlocal i
        i += 1
        return i
    return next

next = myGenerator(1)
while (True):
    n = next()
    if (n > 42):
        break
    print(n)
