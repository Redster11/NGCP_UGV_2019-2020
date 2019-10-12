import math

class Circle(object):
    def __init__(self, r):
        self.radius = abs(r)
        self.diameter = 2 * self.radius
        self.getArea()
        self.getCircumference()

    def getArea(self):
        self.area = math.pi * self.radius * self.radius

    def getCircumference(self):
        self.circumference = 2 * math.pi * self.radius