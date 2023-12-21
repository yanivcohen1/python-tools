from enum import IntEnum
# class syntax
class Color(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3
    NOT_FOUND = -1

    @classmethod
    def _missing_(cls, value):
        return cls.NOT_FOUND

print(Color.GREEN.name == "GREEN") # True
print(Color.GREEN.value == 2) # True
print(Color(5) == Color.NOT_FOUND) # True
print(Color(5).name == "NOT_FOUND") # True

enum_list = list(map(str, Color))
print(enum_list) # prints ['Color.RED', 'Color.GREEN', 'Color.BLUE', 'Color.NOT_FOUND']

enum_list = list(map(int, Color))
print(enum_list) # prints [1, 2, 3, -1]
