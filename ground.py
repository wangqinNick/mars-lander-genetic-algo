import turtle
from plane import Vector


class Ground:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.y1 = y1
        self.x1 = x1
        self.vector0 = Vector(x0, y0)
        self.vector1 = Vector(x1, y1)
        self.is_target = True

    def display(self):
        self.x0 = int(self.x0 / 10)
        self.y0 = int(self.y0 / 10)
        self.x1 = int(self.x1 / 10)
        self.y1 = int(self.y1 / 10)

        turtle.speed(1000)
        turtle.penup()
        turtle.goto(self.x0, self.y0)
        turtle.pendown()
        turtle.pensize(2)
        turtle.goto(self.x1, self.y1)


class SimpleTarget:
    def __init__(self, x0, y0):
        self.x0 = x0
        self.y0 = y0
        self.vector0 = Vector(x0, y0)
        self.is_target = True

    def display(self):
        self.x0 = int(self.x0 / 10)
        self.y0 = int(self.y0 / 10)

        turtle.speed(1000)
        turtle.penup()
        turtle.goto(self.x0, self.y0)
        turtle.pendown()
        turtle.pensize(2)
        turtle.begin_fill()
        turtle.circle(10)
