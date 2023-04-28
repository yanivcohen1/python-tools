def inc1(a):
    return a+1

b = None # not must to define it will cereate it enyway

def inc2(a):
    global b
    b = a + 2

print(eval('inc1(2)')) # run one line and return a value
exec("inc2(2)") # run multilines and not return val
print(b)
