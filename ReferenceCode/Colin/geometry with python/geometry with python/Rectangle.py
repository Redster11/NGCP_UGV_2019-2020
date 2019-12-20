class Rectangle(object):
    def __init__(self, l, w):
        self.length = abs(l)
        self.width = abs(w)
        self.getArea()
        self.getPerimeter()

    def getArea(self):
        self.area = self.length * self.width
    
    def getPerimeter(self):
        self.perimeter = 2 * (self.length + self.width)