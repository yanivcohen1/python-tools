class Base:
    pass

class Derive(Base):
    pass

base = Base()
print(type(base))
# <class '__main__.Base'>
derive = Derive()
print(type(derive))
# <class '__main__.Derive'>
print(type(derive) is Derive)
# True
print(type(derive) is Base)
# False
print(isinstance(derive, Derive))
# True
print(isinstance(derive, Base))
# True
print(isinstance(1, int))
# True
print(type(1) is int)
# True
print(isinstance("test", str))
# True
print(type("test") is str)
# True
