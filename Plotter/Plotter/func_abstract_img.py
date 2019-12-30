#--------------------------------------------------------------------------------------------------
# Module  : func_abstract_img
# Contains: Plot image as lines
# Created : HW Beekhof 2018 http://www.hwbbox.com
#--------------------------------------------------------------------------------------------------
import math
import time
from proj_settings import *
from func_plot import *

from PIL import Image

def printImageToLines(fileName, scale):

    # open image and convert to grayscale, mode L equals 8 bits per pixel
    image = Image.open(fileName).convert('L')
    
    # store dimensions
    imgWidth = image.size[0]
    imgHeight= image.size[1]
    print("filename: %s" % fileName)
    print("scale: %d" % scale)
    print("input image dimentions: %d x %d" % (imgWidth, imgHeight))

    # get the largets dimention
    imgMaxSize=max(imgWidth, imgHeight)
    print("max size: ", imgMaxSize)

    # calculate centering
    xOffset = (41000 - (imgWidth * scale)) >> 1
    print("X offset: ", xOffset)
    if (xOffset<20):
        print("Image in combination with scale factor to large.")
        exit(0)

    inLine=False
    step = 4
    for y in range (0, imgHeight-1, step):
        if (y>4):
            plotter.s_moveTo(0,y*scale)
            if (ps.plotmode==ps.PLOT):
                sc.penDown()
                sc.penUp()
                sc.home_x()

        for x in range (0, imgWidth-1):
            p=image.getpixel((x,y))
            if (p<127):
                if (not inLine):
                    xStart=x
                    inLine=True
                if (inLine):
                    xEnd=x
            else:
                # draw a line when a line is started and the line ends or when the edge is reached
                if (inLine):
                    if (x==imgWidth-1):
                        xEnd=x
                    inLine=False
                    plotter.s_drawLine(xOffset + xStart*scale, y*scale, xOffset + xEnd*scale, y*scale)

        # for faster printing every odd line is printed from right to left after the previous line is printed from left to right
        if (y < imgHeight-2):
            for x in range (imgWidth-1, 0, -1):
                p=image.getpixel((x,y+(step/2)))
                if (p<127):
                    if (not inLine):
                        xStart=x
                        inLine=True
                    if (inLine):
                        xEnd=x
                else:
                    # draw a line when a line is started and the line ends or when the edge is reached
                    if (inLine):
                        if (x==0):
                            xEnd=x
                        inLine=False
                        ypos=int((y+(step/2))*scale)
                        plotter.s_drawLine(xOffset + xStart*scale, ypos, xOffset + xEnd*scale, ypos)    


# main() function
def plot_img_to_lines():

    #imgFile = '..\\..\\img\\starbucks_bw.gif'  # Scale = 100
    imgFile = '..\\..\\img\\Darth_Vader.png'    # Scale = 60

    # set scale dependent on the pen used
    # Pen: Stanger M235: ~1.5mm thick, 70 dots
    scale = 60

    print('generating imgage as set of lines...')
  
    printImageToLines(imgFile, scale)

    if (ps.plotmode==ps.PLOT):
        sc.penUp()
        sc.turnOff()
    else:
        plotter.drawFrame()
        plotter.show_image()


