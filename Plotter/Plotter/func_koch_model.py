"""
koch.py

Description:

A program that explores the Koch snowflake and the Thue-Morse sequence.

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import time
import turtle
import math
import sys, argparse

# recursive koch snow flake
def kochSF(x1, y1, x2, y2, t):
    d = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
    r = d/3.0
    h = r*math.sqrt(3)/2.0
    p3 = ((x1 + 2*x2)/3.0, (y1 + 2*y2)/3.0)
    p1 = ((2*x1 + x2)/3.0, (2*y1 + y2)/3.0)
    c = (0.5*(x1+x2), 0.5*(y1+y2))
    n = ((y1-y2)/d, (x2-x1)/d)
    p2 = (c[0]+h*n[0], c[1]+h*n[1])     
    if d > 300:
        # flake #1
        kochSF(x1, y1, p1[0], p1[1], t)
        # flake #2
        kochSF(p1[0], p1[1], p2[0], p2[1], t)
        # flake #3
        kochSF(p2[0], p2[1], p3[0], p3[1], t)
        # flake #4
        kochSF(p3[0], p3[1], x2, y2, t)
    else:
        # draw cone
        t.up()
        t.setpos(p1[0], p1[1])
        t.down()
        t.setpos(p2[0], p2[1])
        t.setpos(p3[0], p3[1])
        # draw sides
        t.up()
        t.setpos(x1, y1)
        t.down()
        t.setpos(p1[0], p1[1])
        t.up()
        t.setpos(p3[0], p3[1])
        t.down()
        t.setpos(x2, y2) 

# draw a koch snowflake
def drawKochSF(x1, y1, x2, y2,t):
    #t = turtle.Turtle()
    t.hideturtle()
    kochSF(x1, y1, x2, y2, t)

def drawKochTriange(x1, y1, length, angle):
    t = turtle.Turtle()
    x2=x1 + length * math.cos(math.radians(angle))
    y2=y1 + length * math.sin(math.radians(angle))
    x3=x2 + length * math.cos(math.radians(angle+240))
    y3=y2 + length * math.sin(math.radians(angle+240))
    t.pencolor("red")
    drawKochSF(x1, y1, x2, y2,t)
    t.pencolor("green")
    drawKochSF(x2, y2, x3, y3,t)
    t.pencolor("blue")
    drawKochSF(x3, y3, x1, y1,t)


# main() function
def main_koch_model():
    print('Exploring the Koch Snowflake...')

    for x in range(0,360,45):
        drawKochTriange(0,0,300,x)
        win = turtle.Screen()
    win.exitonclick()
