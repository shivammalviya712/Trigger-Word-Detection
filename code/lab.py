"""All the crazy ideas are 
brought to life, in this file
"""


class Test:
    def __init__(self, a):
        self.a = a
        self.a.a = 4


class A:
    def __init__(self):
        self.a = 2


a = A()
test = Test(a)
print(a.a)
print(test.a.a)


