a=2
result = "is bigger" if a > 1 else "is smaller"
print(result)

a=True
result = "is True" if a else "is False"
print(result)

a=2
result = a+1 if a > 1 else "is smaller"
print(result)
a=0
result = a+1 if a > 1 else "is smaller"
print(result)

# in javascript
# var timeout = settings !== null ? settings.timeout : 1000;

# in java
# Object bar = foo.isSelected() ? foo : baz;