def greet(name="yaniv", msg="Good morning!"):
    """
    This function greets to
    the person with the
    provided message.

    If the message is not provided,
    it defaults to "Good
    morning!"
    """

    print("Hello", name + ', ' + msg)

greet(msg="How are you?")
greet("Bruce", "How do you do?")

def retXY():
    x1=1
    x2=2
    return x1,x2

x1,x2 = retXY()
print(x1)
print(x2)