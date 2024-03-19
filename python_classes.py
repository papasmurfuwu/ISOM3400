class Rectangle():
    def __init__(self, length, width):
        self.length = length
        self.width = width 

    def area(self):
        return self.length * self.width 
    
    def perimeter(self):
        return 2 * (self.length + self.width)
    

square1 = Rectangle(10, 10)
square1.area()