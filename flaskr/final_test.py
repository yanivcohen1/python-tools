from typing import Final # in python 3.8 >=

a: Final = 1.2
b: float = 2
# Executes fine, but mypy will report an error if you run mypy on this:
# a = 2
print(a)
