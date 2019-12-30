#--------------------------------------------------------------------------------------------------
# Module  : func_applications
# Contains: Different applications to plot
# Created : HW Beekhof 2018 http://www.hwbbox.com
#--------------------------------------------------------------------------------------------------
from proj_settings import *
import random
from PIL import Image
from func_plot import *
from func_communication import *
from func_ascii_art import *


#--------------------------------------------------------------------------------------------------
# Output an ascii-art generated text file
#--------------------------------------------------------------------------------------------------
def print_ascii_art_file():
    plotter.drawFrame()

    x_start=40

    x=x_start
    y=40
   
    # which input file
    inFile = '..\\..\\ASCII\\boeddha_12.txt'
    
    # set cols
    cols = 170
    plotter.setCharSize(12)

    # open input file
    fi = open(inFile, 'r')

    line_nr=0
    for cur_line in fi:
        txtline=cur_line.rstrip('\n')

        #plotter.s_moveTo(x,y)
        for cur_char in txtline:
            if (cur_char!=' '):
                plotter.s_drawChar(x,y,cur_char)
            x+=plotter.getCharOffset()
    
        x=x_start
        y+=plotter.getLineOffset()

        line_nr+=1
        print(line_nr)

    if (ps.plotmode==ps.PLOT):
        sc.penUp()
        sc.turnOff()
    else:
        plotter.show_image()
   
def draw_mark(x,y,delta):
    plotter.s_drawLine(x-delta,y-delta,x+delta,y+delta)
    plotter.s_drawLine(x-delta,y+delta,x+delta,y-delta)
    plotter.s_drawRect(x-delta,y-delta,2*delta,2*delta)

#--------------------------------------------------------------------------------------------------
# Test
#--------------------------------------------------------------------------------------------------
def test_distances(mode):
    if (mode==1):
        #draw horizontal lines and vertical lines to determine the distance between adjacent lines
        x=3600
        y=100
        dx=500
        dy=0
        distance=70

        for i in range (0,5):
            dy=i*distance
            x=x+200
            plotter.s_drawLine(x,y+dy,x+dx,y+dy)

        x=3600
        y=100
        dx=0
        dy=500
        for i in range (0,5):
            dx=i*distance
            y=y+200
            plotter.s_drawLine(x+dx,y,x+dx,y+dy)

    if (mode==2):
        delta=300
        x=400
        y=400
        draw_mark(x,y,delta)

        x=40000
        y=400
        draw_mark(x,y,delta)

        x=40000
        y=40000
        draw_mark(x,y,delta)

        x=400
        y=40000
        draw_mark(x,y,delta)

        x=20000
        y=20000
        draw_mark(x,y,delta)

    if (mode==3):
        sc.penUp()
        while (1):
            pass

    if (ps.plotmode==ps.PLOT):
        sc.penUp()
        sc.turnOff()
    else:
        plotter.drawFrame()
        plotter.show_image()

#--------------------------------------------------------------------------------------------------
# Output the known characters
#--------------------------------------------------------------------------------------------------
def test_charset():
    plotter.drawFrame()

    plotter.setCharSize(10)
    d=plotter.getCharOffset()

    print(plotter.getCharSize())
    print(plotter.getCharOffset())
    print(plotter.getCharsPerLine())
    print(plotter.getLinesPerSheet())

    x=100
    y=100
    plotter.s_moveTo(x,y)
    plotter.s_drawChar(x,y,'@')
    x+=d
    plotter.s_drawChar(x,y,'%')
    x+=d
    plotter.s_drawChar(x,y,'#')
    x+=d
    plotter.s_drawChar(x,y,'*')
    x+=d
    plotter.s_drawChar(x,y,'+')
    x+=d
    plotter.s_drawChar(x,y,'=')
    x+=d
    plotter.s_drawChar(x,y,'-')
    x+=d

    plotter.s_drawChar(x,y,' ')
    x+=d
    plotter.s_drawChar(x,y,'$')
    x+=d
    plotter.s_drawChar(x,y,'/')
    x+=d
    plotter.s_drawChar(x,y,'\\')
    x+=d
    plotter.s_drawChar(x,y,'|')
    x+=d
    plotter.s_drawChar(x,y,'(')
    x+=d
    plotter.s_drawChar(x,y,')')
    x+=d
    plotter.s_drawChar(x,y,'[')
    x+=d
    plotter.s_drawChar(x,y,']')
    x+=d
    plotter.s_drawChar(x,y,'<')
    x+=d
    plotter.s_drawChar(x,y,'>')
    x+=d
    plotter.s_drawChar(x,y,'?')
    x+=d
    plotter.s_drawChar(x,y,'!')
    x+=d
    plotter.s_drawChar(x,y,'~')
    x+=d
    plotter.s_drawChar(x,y,'&')
    x+=d
    plotter.s_drawChar(x,y,'{')
    x+=d
    plotter.s_drawChar(x,y,'}')
    x+=d
    plotter.s_drawChar(x,y,':')
    x+=d
    plotter.s_drawChar(x,y,';')
    x+=d
    plotter.s_drawChar(x,y,'.')
    x+=d
    plotter.s_drawChar(x,y,',')
    x+=d
    plotter.s_drawChar(x,y,'"')
    x+=d
    plotter.s_drawChar(x,y,'\'')
    x+=d
    plotter.s_drawChar(x,y,'`')
    x+=d
    plotter.s_drawChar(x,y,'^')

    x=100
    y=y + plotter.getLineOffset()
    for i in range (ord('a'),ord('z')+1):
        plotter.s_drawChar(x,y,chr(i))
        x+=d

    x=100
    y=y + plotter.getLineOffset()
    for i in range (ord('A'),ord('Z')+1):
        plotter.s_drawChar(x,y,chr(i))
        x+=d

    x=100
    y=y + plotter.getLineOffset()
    for i in range (ord('0'),ord('9')+1):
        plotter.s_drawChar(x,y,chr(i))
        x+=d

    if (ps.plotmode==ps.PLOT):
        sc.penUp()
        sc.turnOff()
    else:
        plotter.show_image()

#--------------------------------------------------------------------------------------------------
# Output a random pattern (test)
#--------------------------------------------------------------------------------------------------
def random_diagram():
    x0=30000
    y0=30000
    x=30000
    y=30000
    cnt=0;
    while cnt<10:
        #s_moveTo(x,y)
        #x=500+random.randint(100,39500)
        #y=500+random.randint(100,39500)
        if (random.randint(1,2)>1):
            if x<29000:
                x+=2000*random.randint(1,5)
            else:
                if x>13000:
                    x-=6000*random.randint(1,5)
        else:
            if (x>13000):
                x-=2000*random.randint(1,5)
            else:
                if x<29000:
                    x+=2000*random.randint(1,5)

        if (random.randint(1,2)>1):
            if y<29000:
                y+=2000*random.randint(1,5)
            else:
                if y>13000:
                    y-=2000*random.randint(1,5)
        else:
            if (y>13000):
                y-=2000*random.randint(1,5)
            else:
                if y<29000:
                    y+=2000*random.randint(1,5)
        if cnt>0:
            plotter.s_drawLine(x0,y0,x,y)
        plotter.s_drawLine(x-400,y-400,x+400,y+400)
        plotter.s_drawLine(x-400,y+400,x+400,y-400)
    
        plotter.s_drawRect(x+400,y+200,800,500)
        plotter.s_drawRect(x-400,y-400,300,600)
        plotter.s_drawRect(x-700,y+600,600,400)
        plotter.s_drawRect(x+300,y-100,400,500)
    
        x0=x
        y0=y

        cnt+=1

    if (ps.plotmode==ps.PLOT):
        sc.penUp()
        sc.turnOff()
    else:
        plotter.drawFrame()
        plotter.show_image()


