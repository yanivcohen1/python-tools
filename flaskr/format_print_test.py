import math

hith = 5
radius = 10
volume = int(math.pi * radius * radius * hith)
print(f'The chlinder hith: {hith} and the radius: {radius} = \
so the volume is:{int(math.pi * radius * radius * hith)} \n The End resoult need to be {volume}')

class class1():
    name = 'yaniv cohen'

    def __init__(self, name) -> None:
        self.name = name

    def say_hi(self):
        print(self.name + " takes care of you!")

c1 = class1('yanic')
print(f'\nThe class1 fun and variables: {dir(c1)}')
print(f'\nThe c1 type: {type(c1)}')