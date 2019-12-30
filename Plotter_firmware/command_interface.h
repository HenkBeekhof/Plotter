#ifndef COMMAND_INTERFACE
#define COMMAND_INTERFACE

#include "plotter_firmware.h"
void get_command(char *ptr);
void interprete_command(char *command, cmd_info* ci);
bool execute_command(cmd_info *ci);

#endif

