class Robot:

    def __init__(self, name):
        self.name = name

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
