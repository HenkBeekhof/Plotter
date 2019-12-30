#--------------------------------------------------------------------------------------------------
# Module  : func_plot
# Contains: Functions to simulate the plotter and present a graphical view
# Created : HW Beekhof 2018 http://www.hwbbox.com
#--------------------------------------------------------------------------------------------------
from PIL import Image
from func_communication import *
from proj_settings import *

img=None
mf=49
delta_x=3
delta_y=3

class Plot:
    # Current position
    cx=0
    cy=0
    pen_color=(0,0,0)

    # Scale factor
    # Plotter resolution: 41000x41000 steps. 41000 steps in X is 838mm. 1mm ~ 49 steps
    # scale_factor=32: 41000/32=1282
    # scale factor shift is 5 (x>>5 is equal to x/32)
    sfs=5

    def __init__(self):
        self.set_current_pos(0,0)
        
        # Setup the image: 8 bits pixes, size=(width,height), background
        global img
        #img = Image.new( 'L', ((41000>>self.sfs)+1,(41000>>self.sfs)+1), "white")
        img = Image.new( 'RGB', ((41000>>self.sfs)+1,(41000>>self.sfs)+1), (255,255,255))

    def set_current_pos(self,x,y):
        'Set the current postion to coordinate (x,y)'
        cx=x
        cy=y

    def show_image(self):
        img.show()

    #--------------------------------------------------------------------------------------------------
    # drawFrame: Create a border around the plot area
    #--------------------------------------------------------------------------------------------------
    def drawFrame(self):
        for i in range(img.size[0]):
            # Draw line in X axis direction, for y=0, y=1, y=ymax, y=ymax-1
            img.putpixel((i,0),60)
            img.putpixel((i,1),60)
            img.putpixel((i,img.size[1]-2),60)
            img.putpixel((i,img.size[1]-1),60)
        for i in range(img.size[1]):
            # Draw line in Y axis direction, for x=0, x=1, x=xmax, x=xmax-1
            img.putpixel((0,i),60)
            img.putpixel((1,i),60)
            img.putpixel((img.size[0]-2,i),60)
            img.putpixel((img.size[0]-1,i),60)   

    #--------------------------------------------------------------------------------------------------
    # setPenColor: set the RGB pen color
    #--------------------------------------------------------------------------------------------------
    def s_setPenColor(self,c):
        self.pen_color=c

    #--------------------------------------------------------------------------------------------------
    # setPixel: set pixel at coordinate (x,y) Define pixel color based on existing pixel value
    #--------------------------------------------------------------------------------------------------
    def s_setPixel(self,x,y):
        p=img.getpixel((x,y))
        #if (p>0):
        #    img.putpixel((x,y),p-64)
        #img.putpixel((x,y),0)
        img.putpixel((x,y),self.pen_color)

    #--------------------------------------------------------------------------------------------------
    # moveToXY: Move to (x1,y1)
    #--------------------------------------------------------------------------------------------------
    def s_moveTo(self,x1, y1):
        global cx,cy
        cx=x1
        cy=y1
        if (ps.plotmode==ps.PLOT):
            sc.moveTo(x1,y1)

    #--------------------------------------------------------------------------------------------------
    # drawLine: Draw from (x0,y0) to (x1,y1)
    #--------------------------------------------------------------------------------------------------
    def s_drawLine(self,ix0, iy0, ix1, iy1):
        "Bresenham's line algorithm"
        if (ps.plotmode==ps.SIMU):
            x0=int(ix0)>>self.sfs
            y0=int(iy0)>>self.sfs
            x1=int(ix1)>>self.sfs
            y1=int(iy1)>>self.sfs
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            x, y = x0, y0
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            if dx > dy:
                err = dx / 2.0
                while x != x1:
                    self.s_setPixel(x,y)
                    err -= dy
                    if err < 0:
                        y += sy
                        err += dx
                    x += sx
            else:
                err = dy / 2.0
                while y != y1:
                    self.s_setPixel(x,y)
                    err -= dx
                    if err < 0:
                        x += sx
                        err += dy
                    y += sy        
            self.s_setPixel(x,y)
        
        global cx,cy
        cx=ix1
        cy=iy1

        if (ps.plotmode==ps.PLOT):
            sc.drawLine(ix0, iy0, ix1, iy1)

    #--------------------------------------------------------------------------------------------------
    # drawLineSegment: Draw from current position to (x1,y1)
    #--------------------------------------------------------------------------------------------------
    def s_drawLineSegment(self,x1, y1):
        if (cx!=x1) | (cy!=y1):
            self.s_drawLine(cx,cy,x1,y1)
    
    #--------------------------------------------------------------------------------------------------
    # drawRect: Draw rectangle from (x,y) with sides dx and dy
    #--------------------------------------------------------------------------------------------------
    def s_drawRect(self,x, y, dx, dy):
        self.s_drawLine(x,y,x+dx,y)
        self.s_drawLine(x+dx,y,x+dx,y+dy)
        self.s_drawLine(x+dx,y+dy,x,y+dy)
        self.s_drawLine(x,y+dy,x,y)

    #--------------------------------------------------------------------------------------------------
    # drawCircle: Draw circle from center (x,y) with radius
    #--------------------------------------------------------------------------------------------------
    def s_drawCircle(self,ix0, iy0, iradius):
        x0=ix0>>self.sfs
        y0=iy0>>self.sfs
        radius=iradius>>self.sfs
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        self.s_setPixel(x0, y0 + radius)
        self.s_setPixel(x0, y0 - radius)
        self.s_setPixel(x0 + radius, y0)
        self.s_setPixel(x0 - radius, y0)
 
        while x < y:
            if f >= 0: 
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x   
            self.s_setPixel(x0 + y, y0 - x)        #q1
            self.s_setPixel(x0 + x, y0 - y)        #q2
            self.s_setPixel(x0 - x, y0 - y)        #q3
            self.s_setPixel(x0 - y, y0 - x)        #q4
            self.s_setPixel(x0 - y, y0 + x)        #q5
            self.s_setPixel(x0 - x, y0 + y)        #q6
            self.s_setPixel(x0 + x, y0 + y)        #q7
            self.s_setPixel(x0 + y, y0 + x)        #q8
    
    #--------------------------------------------------------------------------------------------------
    # setCharSize: 
    #--------------------------------------------------------------------------------------------------
    def setCharSize(self,size):  
        global mf
        mf=size

    #--------------------------------------------------------------------------------------------------
    # getCharSize: 
    #--------------------------------------------------------------------------------------------------
    def getCharSize(self): 
        global mf
        return mf

    #--------------------------------------------------------------------------------------------------
    # setCharSpacing: 
    #--------------------------------------------------------------------------------------------------
    def setCharSpacing(self,spacing):  
        global delta_x
        delta_x=spacing
      
    #--------------------------------------------------------------------------------------------------
    # getCharSpacing: 
    #--------------------------------------------------------------------------------------------------
    def getCharSpacing(self):  
        global delta_x
        return delta_x   

    #--------------------------------------------------------------------------------------------------
    # setLineSpacing: 
    #--------------------------------------------------------------------------------------------------
    def setLineSpacing(self,spacing):  
        global delta_y
        delta_y=spacing

    #--------------------------------------------------------------------------------------------------
    # getLineSpacing: 
    #--------------------------------------------------------------------------------------------------
    def getLineSpacing(self):  
        global delta_y
        return delta_y

    #--------------------------------------------------------------------------------------------------
    # getCharOffset: 
    #--------------------------------------------------------------------------------------------------
    def getCharOffset(self):  
        return ((17 + self.getCharSpacing()) * self.getCharSize())

    #--------------------------------------------------------------------------------------------------
    # getLineOffset: 
    #--------------------------------------------------------------------------------------------------
    def getLineOffset(self):  
        return ((30 + self.getLineSpacing()) * self.getCharSize())

    #--------------------------------------------------------------------------------------------------
    # getCharsPerLine: 
    #--------------------------------------------------------------------------------------------------
    def getCharsPerLine(self):  
        return (41000 / self.getCharOffset())

    #--------------------------------------------------------------------------------------------------
    # getLinesPerSheet: 
    #--------------------------------------------------------------------------------------------------
    def getLinesPerSheet(self):  
        return (41000 / self.getLineOffset())

    #--------------------------------------------------------------------------------------------------
    # drawText: Draw a text string from (x,y)
    #--------------------------------------------------------------------------------------------------
    def s_drawText(self,x, y, txt):
        d=self.getCharOffset()
        self.s_moveTo(x,y)
        for ch in txt:
            self.s_drawChar(x,y,ch)
            x+=d

    #--------------------------------------------------------------------------------------------------
    # drawChar: Draw character from (x,y)
    #--------------------------------------------------------------------------------------------------
    def s_drawChar(self,x, y, ch):
        
        if (ch==' '):
            return
        if (ch=='a'):
            self.s_drawLine(x+mf*  3,y+mf*  8,x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 13)
            self.s_drawLineSegment(x+mf* 17,y+mf* 13)
            return
        if (ch=='b'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf* 0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf*  8)
            return
        if (ch=='c'):
            self.s_drawLine(x+mf* 17,y+mf*  8,x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='d'):
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            return
        if (ch=='e'):
            self.s_drawLine(x+mf*  0,y+mf* 16,x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 14,y+mf* 21)
            return
        if (ch=='f'):
            self.s_drawLine(x+mf* 10,y+mf*  0,x+mf*  5,y+mf*  0)
            self.s_drawLineSegment(x+mf*  5,y+mf* 21)
            self.s_drawLine(x+mf*  1,y+mf* 13,x+mf*  9,y+mf* 13)
            return
        if (ch=='g'):
            self.s_drawLine(x+mf*  5,y+mf* 30,x+mf* 17,y+mf* 30)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='h'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLine(x+mf*  0,y+mf*  8,x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='i'):
            self.s_drawLine(x+mf*  5,y+mf*  4,x+mf*  5,y+mf*  5)
            self.s_drawLine(x+mf*  5,y+mf*  8,x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 10,y+mf* 21) 
            return
        if (ch=='j'):
            self.s_drawLine(x+mf* 10,y+mf*  4,x+mf* 10,y+mf*  5)
            self.s_drawLine(x+mf* 10,y+mf*  8,x+mf* 10,y+mf* 30)
            self.s_drawLineSegment(x+mf*  5,y+mf* 30) 
            return
        if (ch=='k'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLine(x+mf*  0,y+mf* 15,x+mf* 17,y+mf*  8)
            self.s_drawLine(x+mf* 17,y+mf* 21,x+mf*  6,y+mf* 13) 
            return
        if (ch=='l'):
            self.s_drawLine(x+mf*  5,y+mf*  0,x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 10,y+mf* 21)
            return
        if (ch=='m'):
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLine(x+mf*  9,y+mf* 13,x+mf*  9,y+mf*  8)
            return
        if (ch=='n'):
            self.s_drawLine(x+mf*  2,y+mf* 21,x+mf*  2,y+mf*  8)
            self.s_drawLineSegment(x+mf* 15,y+mf*  8)
            self.s_drawLineSegment(x+mf* 15,y+mf* 21)
            return
        if (ch=='o'):
            self.s_drawLine(x+mf*  0,y+mf* 8,x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf*  8)
            return
        if (ch=='p'):
            self.s_drawLine(x+mf*  0,y+mf* 30,x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
        if (ch=='q'):
            self.s_drawLine(x+mf* 17,y+mf* 30,x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='r'):
            self.s_drawLine(x+mf*  5,y+mf* 21,x+mf*  5,y+mf*  8)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            return
        if (ch=='s'):
            self.s_drawLine(x+mf* 17,y+mf* 8,x+mf*  0,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf* 13)
            self.s_drawLineSegment(x+mf* 17,y+mf* 13)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            return
        if (ch=='t'):
            self.s_drawLine(x+mf*  5,y+mf*  0,x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 10,y+mf* 21)
            self.s_drawLine(x+mf*  1,y+mf* 13,x+mf*  9,y+mf* 13) 
            return
        if (ch=='u'):
            self.s_drawLine(x+mf*  0,y+mf*  8,x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            return    
        if (ch=='v'):
            self.s_drawLine(x+mf*  2,y+mf* 8,x+mf*  8,y+mf* 21)
            self.s_drawLineSegment(x+mf* 14,y+mf*  8)
            return 
        if (ch=='w'):
            self.s_drawLine(x+mf*  0,y+mf*  8,x+mf*  6,y+mf* 21)
            self.s_drawLineSegment(x+mf*  9,y+mf* 15)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            return    
        if (ch=='x'):
            self.s_drawLine(x+mf*  0,y+mf*  8,x+mf* 17,y+mf* 21)
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf* 17,y+mf*  8)
            return
        if (ch=='y'):
            self.s_drawLine(x+mf*  0,y+mf*  8,x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLine(x+mf* 17,y+mf*  8,x+mf* 17,y+mf* 30)
            self.s_drawLineSegment(x+mf*  0,y+mf* 30)
            return
        if (ch=='z'):
            self.s_drawLine(x+mf*  0,y+mf*  8,x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='A'):
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf*  9,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLine(x+mf*  4,y+mf* 13,x+mf* 14,y+mf* 13)
            return
        if (ch=='B'):
            self.s_drawLine(x+mf* 11,y+mf*  8,x+mf* 11,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  8)
            self.s_drawLineSegment(x+mf*  0,y+mf*  8)
            return
        if (ch=='C'):
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='D'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 17,y+mf*  5)
            self.s_drawLineSegment(x+mf* 12,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf*  0)
            return
        if (ch=='E'):
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLine(x+mf*  0,y+mf* 11,x+mf* 10,y+mf* 11)
            return
        if (ch=='F'):
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLine(x+mf*  0,y+mf* 11,x+mf* 10,y+mf* 11)
            return
        if (ch=='G'):
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 16)
            self.s_drawLineSegment(x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLineSegment(x+mf* 10,y+mf* 11)
            return
        if (ch=='H'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf* 17,y+mf* 21)
            self.s_drawLine(x+mf*  0,y+mf* 11,x+mf* 17,y+mf* 11)
            return
        if (ch=='I'):
            self.s_drawLine(x+mf*  2,y+mf*  0,x+mf* 14,y+mf*  0)
            self.s_drawLine(x+mf*  8,y+mf*  0,x+mf*  8,y+mf* 21)
            self.s_drawLine(x+mf*  2,y+mf* 21,x+mf* 14,y+mf* 21)
            return
        if (ch=='J'):
            self.s_drawLine(x+mf*  2,y+mf*  0,x+mf* 11,y+mf*  0)
            self.s_drawLineSegment(x+mf* 11,y+mf* 16)
            self.s_drawLineSegment(x+mf*  6,y+mf* 21)
            self.s_drawLineSegment(x+mf*  1,y+mf* 16)
            return
        if (ch=='K'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='L'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='M'):
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  9,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='N'):
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            return
        if (ch=='O'):
            self.s_drawLine(x+mf*  5,y+mf*  0,x+mf*  0,y+mf*  5)
            self.s_drawLineSegment(x+mf*  0,y+mf* 16)
            self.s_drawLineSegment(x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 17,y+mf*  5)
            self.s_drawLineSegment(x+mf* 12,y+mf*  0)
            self.s_drawLineSegment(x+mf*  5,y+mf*  0)
            return
        if (ch=='P'):
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLineSegment(x+mf*  0,y+mf* 11)
            return
        if (ch=='Q'):
            self.s_drawLine(x+mf*  5,y+mf*  0,x+mf*  0,y+mf*  5)
            self.s_drawLineSegment(x+mf*  0,y+mf* 16)
            self.s_drawLineSegment(x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 17,y+mf*  5)
            self.s_drawLineSegment(x+mf* 12,y+mf*  0)
            self.s_drawLineSegment(x+mf*  5,y+mf*  0)
            self.s_drawLine(x+mf*  6,y+mf* 18,x+mf* 12,y+mf* 24)
            return
        if (ch=='R'):
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLineSegment(x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='S'):
            self.s_drawLine(x+mf* 17,y+mf*  5,x+mf* 12,y+mf*  0)
            self.s_drawLineSegment(x+mf*  5,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf*  5)
            self.s_drawLineSegment(x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 16)
            return
        if (ch=='T'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf* 17,y+mf*  0)
            self.s_drawLine(x+mf*  9,y+mf* 21,x+mf*  9,y+mf*  0)
            return
        if (ch=='U'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 16)
            self.s_drawLineSegment(x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            return
        if (ch=='V'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  9,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            return
        if (ch=='W'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  6,y+mf* 21)
            self.s_drawLineSegment(x+mf*  9,y+mf* 14)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            return
        if (ch=='X'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf* 17,y+mf* 21)
            self.s_drawLine(x+mf*  0,y+mf* 21,x+mf* 17,y+mf*  0)
            return
        if (ch=='Y'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  9,y+mf* 11)
            self.s_drawLine(x+mf*  9,y+mf* 21,x+mf*  9,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            return
        if (ch=='Z'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='1'):
            self.s_drawLine(x+mf*  4,y+mf*  5,x+mf*  9,y+mf*  0)
            self.s_drawLineSegment(x+mf*  9,y+mf* 21)
            self.s_drawLine(x+mf*  1,y+mf* 21,x+mf* 17,y+mf* 21)
            return
        if (ch=='2'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLineSegment(x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='3'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLine(x+mf*  9,y+mf* 11,x+mf* 17,y+mf* 11)
            return
        if (ch=='4'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf* 17,y+mf* 21)
            return
        if (ch=='5'):
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf* 12,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            return
        if (ch=='6'):
            self.s_drawLine(x+mf* 17,y+mf*  0,x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLineSegment(x+mf*  0,y+mf* 11)
            return
        if (ch=='7'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf*  9,y+mf* 21)
            return
        if (ch=='8'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf*  0)
            self.s_drawLine(x+mf*  0,y+mf* 11,x+mf* 17,y+mf* 11)
            return
        if (ch=='9'):
            self.s_drawLine(x+mf* 17,y+mf* 11,x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf*  0,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 0,y+mf* 21)
            return
        if (ch=='0'):
            self.s_drawLine(x+mf*  0,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf*  0)
            self.s_drawLineSegment(x+mf*  0,y+mf*  0)
            return
        if (ch=='$'):
            self.s_drawLine(x+mf* 17,y+mf*  7,x+mf* 12,y+mf*  2)
            self.s_drawLineSegment(x+mf*  5,y+mf*  2)
            self.s_drawLineSegment(x+mf*  0,y+mf*  7)
            self.s_drawLineSegment(x+mf*  0,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 11)
            self.s_drawLineSegment(x+mf* 17,y+mf* 14)
            self.s_drawLineSegment(x+mf* 12,y+mf* 19)
            self.s_drawLineSegment(x+mf*  5,y+mf* 19)
            self.s_drawLineSegment(x+mf*  0,y+mf* 14)
            self.s_drawLine(x+mf*  7,y+mf*  0,x+mf*  7,y+mf* 21)
            self.s_drawLine(x+mf* 11,y+mf* 21,x+mf* 11,y+mf*  0)
            return
        if (ch=='/'):
            self.s_drawLine(x+mf*  5,y+mf* 21,x+mf* 12,y+mf*  0)
            return
        if (ch=='\\'):
            self.s_drawLine(x+mf*  5,y+mf*  0,x+mf* 12,y+mf* 21)
            return
        if (ch=='|'):
            self.s_drawLine(x+mf*  9,y+mf*  0,x+mf*  9,y+mf* 21)
            return
        if (ch=='('):
            self.s_drawLine(x+mf* 14,y+mf*  0,x+mf*  9,y+mf*  5)
            self.s_drawLineSegment(x+mf*  9,y+mf* 16)
            self.s_drawLineSegment(x+mf*  14,y+mf* 21)
            return
        if (ch==')'):
            self.s_drawLine(x+mf* 4,y+mf*  0,x+mf*  9,y+mf*  5)
            self.s_drawLineSegment(x+mf*  9,y+mf* 16)
            self.s_drawLineSegment(x+mf*  4,y+mf* 21)
            return
        if (ch=='['):
            self.s_drawLine(x+mf* 14,y+mf*  0,x+mf*  9,y+mf*  0)
            self.s_drawLineSegment(x+mf*  9,y+mf* 21)
            self.s_drawLineSegment(x+mf* 14,y+mf* 21)
            return
        if (ch==']'):
            self.s_drawLine(x+mf*  4,y+mf*  0,x+mf*  9,y+mf*  0)
            self.s_drawLineSegment(x+mf*  9,y+mf* 21)
            self.s_drawLineSegment(x+mf*  4,y+mf* 21)
            return
        if (ch=='_'):
            self.s_drawLine(x+mf*  2,y+mf* 23,x+mf* 15,y+mf* 23)
            return
        if (ch=='<'):
            self.s_drawLine(x+mf* 12,y+mf* 4,x+mf* 5,y+mf* 11)
            self.s_drawLineSegment(x+mf* 12,y+mf* 18)
            return
        if (ch=='>'):
            self.s_drawLine(x+mf* 5,y+mf* 4,x+mf* 12,y+mf* 11)
            self.s_drawLineSegment(x+mf*  4,y+mf* 18)
            return
        if (ch=='?'):
            self.s_drawLine(x+mf*  0,y+mf*  5,x+mf*  5,y+mf*  0)
            self.s_drawLineSegment(x+mf* 12,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf*  5)
            self.s_drawLineSegment(x+mf*  9,y+mf* 12)
            self.s_drawLineSegment(x+mf*  9,y+mf* 17)
            self.s_drawLine(x+mf*  9,y+mf* 20,x+mf*  9,y+mf* 21)
            return
        if (ch=='!'):
            self.s_drawLine(x+mf*  9,y+mf*  0,x+mf*  9,y+mf* 17)
            self.s_drawLine(x+mf*  9,y+mf* 20,x+mf*  9,y+mf* 21)
            return
        if (ch=='~'):
            self.s_drawLine(x+mf*  0,y+mf* 11,x+mf*  4,y+mf* 6)
            self.s_drawLineSegment(x+mf*  6,y+mf*  6)
            self.s_drawLineSegment(x+mf* 11,y+mf* 15)
            self.s_drawLineSegment(x+mf* 13,y+mf* 15)
            self.s_drawLineSegment(x+mf* 15,y+mf* 11)
            return
        if (ch=='&'):
            self.s_drawLine(x+mf* 17,y+mf* 21,x+mf*  0,y+mf*  5)
            self.s_drawLineSegment(x+mf*  5,y+mf*  0)
            self.s_drawLineSegment(x+mf* 12,y+mf*  0)
            self.s_drawLineSegment(x+mf* 17,y+mf*  5)
            self.s_drawLineSegment(x+mf*  0,y+mf* 16)
            self.s_drawLineSegment(x+mf*  5,y+mf* 21)
            self.s_drawLineSegment(x+mf* 12,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 16)
            return
        if (ch=='{'):
            self.s_drawLine(x+mf* 11,y+mf*  0,x+mf*  9,y+mf*  2)
            self.s_drawLineSegment(x+mf*  9,y+mf*  9)
            self.s_drawLineSegment(x+mf*  7,y+mf* 11)
            self.s_drawLineSegment(x+mf*  9,y+mf* 13)
            self.s_drawLineSegment(x+mf*  9,y+mf* 19)
            self.s_drawLineSegment(x+mf* 11,y+mf* 21)
            return
        if (ch=='}'):
            self.s_drawLine(x+mf*  7,y+mf*  0,x+mf*  9,y+mf*  2)
            self.s_drawLineSegment(x+mf*  9,y+mf*  9)
            self.s_drawLineSegment(x+mf* 11,y+mf* 11)
            self.s_drawLineSegment(x+mf*  9,y+mf* 13)
            self.s_drawLineSegment(x+mf*  9,y+mf* 19)
            self.s_drawLineSegment(x+mf*  7,y+mf* 21)
            return
        if (ch=='@'):
            self.s_drawLine(x+mf* 13,y+mf* 13,x+mf* 13,y+mf*  4)
            self.s_drawLineSegment(x+mf*  7,y+mf*  4)
            self.s_drawLineSegment(x+mf*  7,y+mf* 13)
            self.s_drawLineSegment(x+mf* 17,y+mf* 13)
            self.s_drawLineSegment(x+mf* 17,y       )
            self.s_drawLineSegment(x       ,y       )
            self.s_drawLineSegment(x       ,y+mf* 21)
            self.s_drawLineSegment(x+mf* 17,y+mf* 21)
            return
        if (ch=='%'):
            self.s_drawLine(x+mf* 17,y,x,y+mf*21)
            self.s_drawRect(x,y,mf*8,mf*8)
            self.s_drawRect(x+mf*9,y+mf*13,mf*8,mf*8)
            return
        if (ch=='#'):
            self.s_drawLine(x+mf*  7,y+mf*  0,x+mf*  0,y+mf* 21)
            self.s_drawLine(x+mf*  9,y+mf* 21,x+mf* 16,y+mf*  0)
            self.s_drawLine(x+mf*  2,y+mf*  7,x+mf* 17,y+mf*  7)
            self.s_drawLine(x+mf*  0,y+mf* 13,x+mf* 15,y+mf* 13)
            return
        if (ch=='*'):
            self.s_drawLine(x+mf*  2,y+mf*  4,x+mf* 15,y+mf* 18)
            self.s_drawLine(x+mf* 15,y+mf*  4,x+mf*  2,y+mf* 18)
            self.s_drawLine(x+int(round(mf*8.5)),y+mf*18,int(round(x+mf*8.5)),y+mf*4)
            return
        if (ch=='+'):
            self.s_drawLine(x+int(round(mf*8.5)),y+mf*4,int(round(x+mf*8.5)),y+mf*18)
            self.s_drawLine(x+mf*  2,y+mf* 11,x+mf* 15,y+mf* 11)
            return
        if (ch=='='):
            self.s_drawLine(x+mf*  2,y+mf* 10,x+mf* 15,y+mf* 10)
            self.s_drawLine(x+mf*  2,y+mf* 15,x+mf* 15,y+mf* 15)
            return
        if (ch=='-'):
            self.s_drawLine(x+mf*  2,y+mf* 11,x+mf* 15,y+mf* 11)
            return
        if (ch==':'):
            self.s_drawRect(x+mf*  8,y+mf*  8,mf*  2,mf*  2)
            self.s_drawRect(x+mf*  8,y+mf* 19,mf*  2,mf*  2)
            return
        if (ch==';'):
            self.s_drawRect(x+mf*  8,y+mf*  8,mf*  2,mf*  2)
            self.s_drawRect(x+mf*  8,y+mf* 19,mf*  2,mf*  2)
            self.s_drawLine(x+mf* 10,y+mf* 21,x+mf* 10,y+mf* 23)
            self.s_drawLineSegment(x+mf* 7,y+mf* 23)
            return
        if (ch=='.'):
            self.s_drawRect(x+mf*  8,y+mf* 19,mf*  2,mf*  2)
            return
        if (ch==','):
            self.s_drawRect(x+mf*  8,y+mf* 19,mf*  2,mf*  2)
            self.s_drawLine(x+mf* 10,y+mf* 21,x+mf* 10,y+mf* 23)
            self.s_drawLineSegment(x+mf* 7,y+mf* 23)
            return
        if (ch=='"'):
            self.s_drawLine(x+mf*  9,y+mf*  0,x+mf*  7,y+mf*  5)
            self.s_drawLine(x+mf* 10,y+mf*  5,x+mf* 12,y+mf*  0)
            return
        if (ch=='\''):
            self.s_drawLine(x+mf* 10,y+mf*  5,x+mf* 12,y+mf*  0)
            return
        if (ch=='`'):
            self.s_drawLine(x+mf*  7,y+mf*  0,x+mf* 11,y+mf*  3)
            return
        if (ch=='^'):
            self.s_drawLine(x+mf*  4,y+mf*  5,x+mf*  9,y+mf*  0)
            self.s_drawLineSegment(x+mf* 14,y+mf*  5)
            return

