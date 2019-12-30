//-----------------------------------------------------------------------------------------------------------------
// Module  : plotter_firmware
// Contains: setup and loop, both are standard Arduino functions which are called automatically after reset
//           setup() is responsible for initializations
//           loop()  is called after setup is finished, this is equivalent to main()
//
//           ------------------------------------------------------------------------------------------------------
//           Supported commands:
//           ------------------------------------------------------------------------------------------------------
//           TURN_OFF              Set the hardware to a safe state
//           HOMEX                 Home X and set the zero postion 
//           HOMEY                 Home Y and set the zero postion
//           HOMEXY                Home X and Y and set the zero postion   
//           PU                    Pen Up
//           PD                    Pen Down
//           FAN mode              Turn the fan on or off, 1=on
//           MT x0 y0              Move To coordinate (x0,y0)
//           DL x0 y0 x1 y1        Draw Line from (x0,y0) to (x1,y1)
//           DS x1 y1              Draw Line Segment from current position to (x1,y1)
//           DR x0 y0 dx dy        Draw Rectangle, upper left corner is (x0,y0)
//           SSX speed             Set Speed X motor
//           SSY speed             Set Speed Y motor
//           SPUP position         Set Pen Up Position
//           SPDP position         Set Pen Down Position
//
// Created : HW Beekhof 2018 http://www.hwbbox.com
//-----------------------------------------------------------------------------------------------------------------
#include "command_interface.h"
#include "plotter_control.h"
#include "plotter_firmware.h"

//-----------------------------------------------------------------------------------------------------------------
// Initialization, called by the standard bootloader of the ATMEGA CPU
//-----------------------------------------------------------------------------------------------------------------
void setup() {
  init_plotter();
}

//-----------------------------------------------------------------------------------------------------------------
// main, called by the standard bootloader of the ATMEGA CPU
//-----------------------------------------------------------------------------------------------------------------
void loop() {
  cmd_info ci;
  char command[COMMAND_LENGTH];
  
  while (1) {
    
    // Fetch a command + optional parameters from the serial interface
    get_command(command);
    
    // Decode the command to an instruction and optional parameters
    interprete_command(command, &ci);

    // Execute the instruction
    if (execute_command(&ci)) {
      Serial.println("Ok");
    } else {
      Serial.println("ERROR");
    }
  }
}


