#ifndef PLOTTER_FIRMWARE
#define PLOTTER_FIRMWARE

#define COMMAND_LENGTH     64               // Length of instruction and parameters N > 8 + 4*6 digit + 4 spaces: N=64 is ok
#define INSTRUCTION_LENGTH 8                // Length of the instruction
#define NR_OF_PARAMETERS   4                // Define the number of parameters of a command
#define OK                 true
#define ERROR              false

typedef struct {
  char instruction[INSTRUCTION_LENGTH+1];   // Instruction
  long nr[NR_OF_PARAMETERS];                // Array of intruction related parameters
  int  nr_cnt;                              // Number of applicable parameters
} cmd_info;

#endif

