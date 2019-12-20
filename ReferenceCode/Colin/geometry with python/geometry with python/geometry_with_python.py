import Circle,Rectangle

radius = input("Enter radius: ")
length = input("Enter length: ")
width = input("Enter width: ")
radius = float(radius)
length = float(length)
width = float(width)

myCircle = Circle.Circle(radius)
myRectangle = Rectangle.Rectangle(length, width)

print("Circumference of circle with radius %.3f is %.3f" %(radius,myCircle.circumference))
print("Area of circle with radius %.3f is %.3f" %(radius,myCircle.area))

print("Perimeter of rectangle with length of %d and width%3d is %d" %(length, width, myRectangle.perimeter))
print("Area of rectangle with length of %d and width%3d is %d" %(length, width, myRectangle.area))