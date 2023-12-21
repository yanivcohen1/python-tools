from enum import Enum
# class syntax
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.GREEN.name == "GREEN")
print(Color.GREEN.value == 2)
