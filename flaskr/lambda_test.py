x = lambda a, b, c : a + b + c
# print 6
print(x(1, 2, 3))
#print 5
print( (lambda x, y: x + y)(2, 3) )

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
#print 20
print(mydoubler(10))
#print 10
print(f"mydoubler(5) = {mydoubler(5)}")