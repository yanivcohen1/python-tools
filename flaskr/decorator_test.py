from functools import wraps

def my_decorator(f):
     @wraps(f)
     def wrapper(*args, **kwds):
         print('Calling decorated function')
         print(args)
         print(kwds)
         return f(*args, **kwds)
     return wrapper

@my_decorator
def example(inn: int):
     """Docstring"""
     print('Called example function')

example(5)