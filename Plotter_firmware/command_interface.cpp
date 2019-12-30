//-----------------------------------------------------------------------------------------------------------------
// Module  : command_interface
// Contains: get_command()          Fetch a command from the serial interface
//           interprete_command()   Decode the command to an instruction and parameters
//           execute_command()      Calls the function which implements the instructions and passes the parameters
//
// Created : HW Beekhof 2018 http://hwbbox.com
//-----------------------------------------------------------------------------------------------------------------
#include <Arduino.h>
#include "plotter_firmware.h"
#include "plotter_control.h"

//-----------------------------------------------------------------------------------------------------------------
// Fetch a full command with parameters from the serial interface
// Full commmand = instruction [<parameter_1> [<parameter_2> ... [<parameter_N>]]]
//-----------------------------------------------------------------------------------------------------------------
void get_command(char *ptr) {
  char serial_char;

  while (1) {
    if (Serial.available() > 0) {
      serial_char = Serial.read();
      (*ptr++)=serial_char;
    }
    if (serial_char=='\n') {
      *ptr='\0';
      break;
    }
  }
}

//-----------------------------------------------------------------------------------------------------------------
// Check if a character is part of a command
//-----------------------------------------------------------------------------------------------------------------
int valid_char(char ch) {
  return ((ch!='\0') && (ch!=',') && (ch!=' ') && (ch!=':') && (ch!='\n') && (ch!='\r')); 
}

//-----------------------------------------------------------------------------------------------------------------
// Check if a character represents a number or minus sign
//-----------------------------------------------------------------------------------------------------------------
int is_number_or_minus(char ch) {
  return ( ((ch>='0') && (ch<='9')) || (ch=='-') );
}

//-----------------------------------------------------------------------------------------------------------------
// Check if a character represents a number
//-----------------------------------------------------------------------------------------------------------------
int is_number(char ch) {
  return ((ch>='0') && (ch<='9'));
}

//-----------------------------------------------------------------------------------------------------------------
// Separate the full command into the instruction and parameters
//-----------------------------------------------------------------------------------------------------------------
void interprete_command(char *command, cmd_info *ci) {
  int i,j;
  long getnr;
  bool negative_value;
  
  // Clear parameters
  for (i=0; i<NR_OF_PARAMETERS; i++) ci->nr[i]=0;
  ci->nr_cnt=0;

  // Extract the instruction from full command
  i=0;
  while (valid_char(command[i]) && (i<COMMAND_LENGTH)) {  
    ci->instruction[i]=command[i];
    i++;
  }
  ci->instruction[i]='\0';

  // Fetch the numerical parameters in the command, maximum is set to four
  j=1;
  while (j<=NR_OF_PARAMETERS) {
    
    // Skip not valid characters in the full command
    while (!is_number_or_minus(command[i])) { 
      
      // Exit if the end of the full command is reached
      if (command[i]=='\0') return;
      
      i++;
    }

    // Fetch the numerical parameter
    getnr=0;
    negative_value=false;
    if (command[i]=='-') {
      negative_value=true;
      i++;
    }
    while (is_number(command[i])) {
      getnr=10*getnr+(command[i]-'0');
      i++;
    }
    if (negative_value) {
      getnr=-getnr;
    }
    
    // Store the parameter
    ci->nr[ci->nr_cnt]=getnr;
    ci->nr_cnt++;
    j++;
  }  
}

//-----------------------------------------------------------------------------------------------------------------
// Execute the instruction
//-----------------------------------------------------------------------------------------------------------------
bool execute_command(cmd_info *ci) {

  // Command: TURN_OFF - Set the hardware to a safe state
  if (strcmp(ci->instruction, "TURN_OFF")==0) { 
    turnOff();
    return OK;
  }
  
  // Command: HOMEX - Home X and set the zero postion
  if (strcmp(ci->instruction, "HOMEX")==0) {
    homeX();
    return OK;
  }

  // Command: HOMEY - Home Y and set the zero postion
  if (strcmp(ci->instruction, "HOMEY")==0) { 
    homeY();
    return OK;
  }

  // Command: HOMEXY - Home X and Y and set the zero postion
  if (strcmp(ci->instruction, "HOMEXY")==0) { 
    homeXY();
    return OK;
  }

  // Command: PU - Pen Up
  if (strcmp(ci->instruction, "PU")==0) { 
    penUp();
    return OK;
  }

  // Command: PD - Pen Down
  if (strcmp(ci->instruction, "PD")==0) { 
    penDown();
    return OK;
  }

  // Command: FAN - Fan on/off
  if (strcmp(ci->instruction, "FAN")==0) { 
    if (ci->nr_cnt<1) return ERROR;
    fanOnOff(ci->nr[0]);
    return OK;
  }
  
  // Command: MT x0 y0  - Move To coordinate (x0,y0)
  if (strcmp(ci->instruction, "MT")==0) { 
    if (ci->nr_cnt<2) return ERROR;
    moveToXY(ci->nr[0], ci->nr[1]);
    return OK;
  }

  // Command: DL x0 y0 x1 y1 - Draw Line from (x0,y0) to (x1,y1)
  if (strcmp(ci->instruction, "DL")==0) { 
    if (ci->nr_cnt<4) return ERROR;
    drawLine(ci->nr[0], ci->nr[1], ci->nr[2], ci->nr[3]);
    return OK;
  }

  // Command: DS x1 y1 - Draw Line Segment from current position to (x1,y1)
  if (strcmp(ci->instruction, "DS")==0) { 
    if (ci->nr_cnt<2) return ERROR;
    drawLineSegment(ci->nr[0], ci->nr[1]);
    return OK;
  }

  // Command: DR x0 y0 dx dy - Draw Rectangle, upper left corner is (x0,y0)
  if (strcmp(ci->instruction, "DR")==0) { 
    if (ci->nr_cnt<4) return ERROR;
    drawRectangle(ci->nr[0], ci->nr[1], ci->nr[2], ci->nr[3]);
    return OK;
  }
  
  // Command: SSX speed - Set Speed X motor
  if (strcmp(ci->instruction, "SSX")==0) { 
    if (ci->nr_cnt<1) return ERROR;
    setSpeedX(ci->nr[0]);
    return OK;
  }

  // Command: SSY speed - Set Speed Y motor
  if (strcmp(ci->instruction, "SSY")==0) { 
    if (ci->nr_cnt<1) return ERROR;
    setSpeedY(ci->nr[0]);
    return OK;
  }

  // Command: SPUP position - Set Pen Up Position
  if (strcmp(ci->instruction, "SPUP")==0) { 
    if (ci->nr_cnt<1) return ERROR;
    setPenUpPosition(ci->nr[0]);
    return OK;
  }

  // Command: SPDP position - Set Pen Down Position
  if (strcmp(ci->instruction, "SPDP")==0) { 
    if (ci->nr_cnt<1) return ERROR;
    setPenDownPosition(ci->nr[0]);
    return OK;
  } 
  
  // Unrecognized command
  return ERROR;
}

