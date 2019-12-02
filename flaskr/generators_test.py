def generator_function():
    for i in range(10):
        yield i
#not loading the memory like list
for item in generator_function():
    print(item)