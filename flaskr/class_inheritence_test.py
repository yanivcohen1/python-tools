class Robot:

    def __init__(self, name):
        self.name = name
        self.__privateField = 1 # this is private field "__"

    def __getitem__(self, __name: str) -> str:
        return __name+"!"

    def say_hi(self):
        print("Hi, I am " + self.name)

    def say_hi2(self):
        print("Hi2, I am " + self.name)
        self.say_hi3()

    def say_hi3(self):
        print("Hi3, I am " + self.name)
        self.say_hi()

    def say_hi4(self):
        print("Hi4, I am " + self.name)

class PhysicianRobot(Robot):

    def say_hi(self):
        print(self.name + " takes care of you!")
        super().say_hi4()

robot = Robot("Marvin")
physicianRobot = PhysicianRobot("James")

print(robot, type(robot))
print(physicianRobot, type(physicianRobot))

physicianRobot.say_hi()
physicianRobot.say_hi2()

print(robot.__dict__) # display obj as dictionary
print(type(robot).__name__) # print Robot
print(robot["yan"])# print yan! from __getItem__
print(robot._Robot__privateField) # how to acsses private fild

