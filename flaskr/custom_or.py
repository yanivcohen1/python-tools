class MyData:
    def __init__(self, value):
        self.value = value

    def __or__(self, other: 'MyData'):
        return MyData(self.value + other.value)

    def __repr__(self):
        return f"MyData is {self.value}"

if __name__ == '__main__':
    data1 = MyData(5)
    data2 = MyData(10)
    result = data1 | data2
    print(result)  # Output: MyData is 15
