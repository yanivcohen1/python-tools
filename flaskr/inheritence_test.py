class Robot:
    
    def __init__(self, name):
        self.name = name
        
    def say_hi(self):
        print("Hi, I am " + self.name)

    def say_hi2(self):
        print("Hi2, I am " + self.name)
        
class PhysicianRobot(Robot):

    def say_hi(self):
        print(self.name + " takes care of you!")
        super().say_hi()

robot = Robot("Marvin")
physicianRobot = PhysicianRobot("James")

print(robot, type(robot))
print(physicianRobot, type(physicianRobot))

physicianRobot.say_hi()
physicianRobot.say_hi2()