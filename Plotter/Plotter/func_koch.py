#--------------------------------------------------------------------------------------------------
# Module  : func_koch
# Contains: Draws koch lines
# Source  : Parts of the code originates from Mahesh Venkitachalam, Website: electronut.in
# Created : HW Beekhof 2018 http://www.hwbbox.com
#--------------------------------------------------------------------------------------------------

import time
import turtle
import math
import sys
from proj_settings import *
from func_plot import *

# Recursive koch line
def drawKochSF(x1, y1, x2, y2):
    d = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
    r = d/3.0
    h = r*math.sqrt(3)/2.0
    p3 = ((x1 + 2*x2)/3.0, (y1 + 2*y2)/3.0)
    p1 = ((2*x1 + x2)/3.0, (2*y1 + y2)/3.0)
    c = (0.5*(x1+x2), 0.5*(y1+y2))
    n = ((y1-y2)/d, (x2-x1)/d)
    p2 = (c[0]+h*n[0], c[1]+h*n[1])     
    if d > 3000:
        # Part 1 of the single line
        drawKochSF(x1, y1, p1[0], p1[1])
        # Part 2 of the single line
        drawKochSF(p1[0], p1[1], p2[0], p2[1])
        # Part 3 of the single line
        drawKochSF(p2[0], p2[1], p3[0], p3[1])
        # Part 4 of the single line
        drawKochSF(p3[0], p3[1], x2, y2)
    else:
        # draw cone
        plotter.s_drawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))
        plotter.s_drawLineSegment(int(p3[0]), int(p3[1]))

        # draw sides
        plotter.s_drawLine(int(x1), int(y1), int(p1[0]), int(p1[1]))
        plotter.s_drawLine(int(p3[0]), int(p3[1]), int(x2), int(y2))

def drawKochTriange(x1, y1, length, angle):
    x2=int(x1 + length * math.cos(math.radians(angle)))
    y2=int(y1 + length * math.sin(math.radians(angle)))
    x3=int(x2 + length * math.cos(math.radians(angle+240)))
    y3=int(y2 + length * math.sin(math.radians(angle+240)))
    drawKochSF(x1, y1, x2, y2)
    drawKochSF(x2, y2, x3, y3)
    drawKochSF(x3, y3, x1, y1)

def drawKochTriangeCentered(xc, yc, radius, angle, mode):
    x1=int(xc + radius * math.cos(math.radians(angle)))
    y1=int(yc + radius * math.sin(math.radians(angle)))
    x2=int(xc + radius * math.cos(math.radians(angle+120)))
    y2=int(yc + radius * math.sin(math.radians(angle+120)))
    x3=int(xc + radius * math.cos(math.radians(angle+240)))
    y3=int(yc + radius * math.sin(math.radians(angle+240)))
    if (mode==0):
        drawKochSF(x1, y1, x2, y2)
        drawKochSF(x2, y2, x3, y3)
        drawKochSF(x3, y3, x1, y1)
    else:
        drawKochSF(x2, y2, x1, y1)
        drawKochSF(x1, y1, x3, y3)
        drawKochSF(x3, y3, x2, y2)

def drawKochSquare(x1, y1, length, mode):
    if (mode==0):
        drawKochSF(x1, y1, x1+length, y1)
        drawKochSF(x1+length, y1, x1+length, y1+length)
        drawKochSF(x1+length, y1+length, x1, y1+length)
        drawKochSF(x1, y1+length, x1, y1)
    else:
        drawKochSF(x1, y1, x1, y1+length)
        drawKochSF(x1, y1+length, x1+length, y1+length)
        drawKochSF(x1+length, y1+length, x1+length, y1)
        drawKochSF(x1+length, y1, x1, y1)


# main() function
def print_koch():
    #print('The Koch Curve')

    plotter.drawFrame()

    plotter.setCharSize(80)
    #plotter.s_drawText(17000,7400,"Koch")

    mode = 4

    if (mode==1):
        plotter.s_setPenColor((255,0,0))
        for angle in range(0,360,90):
            for radius in range (16000,18500,1000):
                drawKochTriangeCentered(20000, 20000, radius, angle, 0)
        #drawKochTriangeCentered(20000, 20000, 19000, 0, 1)    
    
    if (mode==2): 
        for i in range(1,8,2):
            drawKochSquare(10000+i*500,10000+i*500,20000-1000*i,1)
            drawKochSquare(10000+i*1000,10000+i*1000,20000-2000*i,0)

    if (mode==3):
        plotter.s_setPenColor((255,0,0))
        for angle in range(0,360,90):
            drawKochTriange(20000,20000,8000,angle)

        plotter.s_setPenColor((0,255,0))
        for angle in range(30,360,90):
            drawKochTriange(20000,20000,8000,angle)
        
        plotter.s_setPenColor((0,0,255))
        for angle in range(60,360,90):
            drawKochTriange(20000,20000,8000,angle)

    if (mode==4):
        plotter.s_setPenColor((255,0,0))
        for angle in range(0,360,45):
            for radius in range (18000,18500,8000):
                drawKochTriangeCentered(20000,20000,radius,angle,0)

        #plotter.s_setPenColor((0,255,0))
        #for angle in range(30,360,90):
        #    drawKochTriange(20000,20000,8000,angle)
        
        #plotter.s_setPenColor((0,0,255))
        #for angle in range(60,360,90):
        #    drawKochTriange(20000,20000,8000,angle)

    if (ps.plotmode==ps.PLOT):
        sc.penUp()
        sc.turnOff()
    else:
        plotter.show_image()