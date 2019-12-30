#--------------------------------------------------------------------------------------------------
# Module  : func_communication
# Contains: Functions to communicate by using a serial interface
# Created : HW Beekhof 2018 http://www.hwbbox.com
#--------------------------------------------------------------------------------------------------
import time
import serial
from proj_settings import *

ser=None

class SerialCommunication:
    def __init__(self):
        self.serial_init()

    #--------------------------------------------------------------------------------------------------
    # serial_init: Setup the serial interface
    #--------------------------------------------------------------------------------------------------
    def serial_init(self):
        '''
        Initialize the serial interface
        Reset the in/out buffers
        Wait for an acknowledge that the hardware is alive'''
        global ser
        ser = serial.Serial('COM3', 9600, timeout=.1)

        # Mandatory wait time to setup the serial interface correctly
        time.sleep(1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()


        # Give the plotter time to boot and catch the startup message from the plotter
        time.sleep(4)
        acknowledge=''
        if ser.in_waiting > 0:
            acknowledge=ser.readline().decode()
            print(acknowledge)

    #--------------------------------------------------------------------------------------------------
    # sendCommand: Send a command
    #--------------------------------------------------------------------------------------------------
    def send_command(self,command_str):
        if (ser.is_open):
            # set this variable to true when the commands should only be displayed, without sending to HW
            sim_cmd=False

            # Concatenate a carriage return to end the command and send it
            cmd=command_str + '\r\n'

            if (not sim_cmd):
                ser.write(cmd.encode())
                print(command_str, end='')
            else:
                print(command_str)

            # Check acknowledge, Every command replies with an acknowledge
            acknowledge=''
            str=''
            if (not sim_cmd):
                while (acknowledge==''):
                    if ser.in_waiting > 0:
                        acknowledge=ser.readline().decode()
                        print('\t - ' + acknowledge)
                        
                        #print('\t - ' + acknowledge, end='')
                        #added
                        #str=acknowledge[5:len(acknowledge)-1]
                        #str=acknowledge + "\r"
                        #if (cmd==str):
                        #    print(" - Ok")
                        #else:
                        #    print(" - FAIL")




    #--------------------------------------------------------------------------------------------------
    # COMMAND: turn_off
    #--------------------------------------------------------------------------------------------------
    def turnOff(self):
        cmd='TURN_OFF'
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: home_x
    #--------------------------------------------------------------------------------------------------
    def home_x(self):
        cmd='HOMEX'
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: home_y
    #--------------------------------------------------------------------------------------------------
    def home_y(self):
        cmd='HOMEY'
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: home_xy
    #--------------------------------------------------------------------------------------------------
    def home_xy(self):
        cmd='HOMEXY'
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: PenUp
    #--------------------------------------------------------------------------------------------------
    def penUp(self):
        cmd='PU'
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: PenDown
    #--------------------------------------------------------------------------------------------------
    def penDown(self):
        cmd='PD'
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: MoveTo x1 y1
    #--------------------------------------------------------------------------------------------------
    def moveTo(self, x1, y1):
        cmd='MT ' + str(x1) + ' ' + str(y1)
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: drawLine x0 y0 x1 y1
    #--------------------------------------------------------------------------------------------------
    def drawLine(self, x0, y0, x1, y1):
        cmd='DL ' + str(x0) + ' ' + str(y0) + ' ' + str(x1) + ' ' + str(y1)
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: drawLineSegment x1 y1
    #--------------------------------------------------------------------------------------------------
    def drawLineSegment(self, x1, y1):
        cmd='DS ' + str(x1) + ' ' + str(y1)
        self.send_command(cmd)

    #--------------------------------------------------------------------------------------------------
    # COMMAND: drawRect x0 y0 dx dy
    #--------------------------------------------------------------------------------------------------
    def drawRect(self, x0, y0, dx, dy):
        cmd='DR ' + str(x0) + ' ' + str(y0) + ' ' + str(dx) + ' ' + str(dy)
        self.send_command(cmd)


