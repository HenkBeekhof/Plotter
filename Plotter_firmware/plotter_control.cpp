//-----------------------------------------------------------------------------------------------------------------
// Module  : plotter_control
// Contains: the functions which do the real work, low level interface with the hardware
//           the move and draw functions take care of the pen position, meaning it is logical that the pen should
//           be in the up position when a move is requested and in the down position during drawing
//
// Created : HW Beekhof 2018 http://hwbbox.com
//-----------------------------------------------------------------------------------------------------------------
#include <Arduino.h>
#include <Servo.h>
#include <AccelStepper.h>
#include <MultiStepper.h>
#include "plotter_control.h"
#include "pins.h"

AccelStepper sX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);   // X motor is connected to the X port
AccelStepper sY(AccelStepper::DRIVER, Z_STEP_PIN, Z_DIR_PIN);   // Y motor is connected to the Z port
MultiStepper steppers;                                          // Array of stepper motors

Servo penA;             // Controls the position of the pen
bool penIsUp;           // Identifies the position of the pen
long XY_Pos[2];         // Array for X position and Y position used in the multistepper library
long maxSpeedX;         // Defines the maximum speed of the X motor
long maxSpeedY;         // Defines the maximum speed of the Y motor
long penUpPosition;     // Defines the up position (in us) of the pen servo
long penDownPosition;   // Defines the down position (in us) of the pen servo

//-----------------------------------------------------------------------------------------------------------------
// Initialization of the interface, steppper motors, servo, emergency stop button, ....
//-----------------------------------------------------------------------------------------------------------------
void init_plotter() {
  // Serial interface
  Serial.begin(9600);
  while (1) {
    if (Serial) break;
  }

  // Setup the emergency stop button, button is connected to SCL, when pressed SCL becomes low, call turnOff()
  attachInterrupt(digitalPinToInterrupt(SCL), turnOff, LOW);

  // Configuration of the stepper motors interface signals
  pinMode(X_STEP_PIN,OUTPUT);
  pinMode(X_DIR_PIN,OUTPUT);
  pinMode(X_ENABLE_PIN,OUTPUT);
  pinMode(Z_STEP_PIN,OUTPUT);
  pinMode(Z_DIR_PIN,OUTPUT);
  pinMode(Z_ENABLE_PIN,OUTPUT);
  
  digitalWrite(X_ENABLE_PIN, LOW);  // Enable motor driver X
  digitalWrite(Z_ENABLE_PIN, LOW);  // Enable motor driver Y

  maxSpeedX=1200;
  maxSpeedY=1200;
  sX.setMaxSpeed(maxSpeedX);
  sX.setSpeed(maxSpeedX);
  sY.setMaxSpeed(maxSpeedY);
  sY.setSpeed(maxSpeedY);

  // To leave the position not uninitialized set this position to (0,0)
  sX.setCurrentPosition(0);
  sY.setCurrentPosition(0);

  // Add the stepper motors to the array controlled by the multistepper library
  steppers.addStepper(sX);
  steppers.addStepper(sY);

  // Servo
  penUpPosition=1520;
  penDownPosition=1250;
  penA.attach(SERVO_1);
  penUp();

  // Fan
  pinMode(FAN,OUTPUT);
  fanOnOff(0);
  
  // End stops
  pinMode(X_MIN_PIN,INPUT);
  pinMode(Z_MIN_PIN,INPUT);
}

//-----------------------------------------------------------------------------------------------------------------
// Set speed for the X motor
//-----------------------------------------------------------------------------------------------------------------
void setSpeedX(long speed) {
  maxSpeedX=speed;
  sX.setMaxSpeed(maxSpeedX);
  sX.setSpeed(maxSpeedX);
}

//-----------------------------------------------------------------------------------------------------------------
// Set speed for the Y motor
//-----------------------------------------------------------------------------------------------------------------
void setSpeedY(long speed) {
  maxSpeedY=speed;
  sY.setMaxSpeed(maxSpeedY);
  sY.setSpeed(maxSpeedY);
}

//-----------------------------------------------------------------------------------------------------------------
// Set the pen up position in microseconds
//-----------------------------------------------------------------------------------------------------------------
void setPenUpPosition(long position) {
  penUpPosition=position;
}

//-----------------------------------------------------------------------------------------------------------------
// Set the pen down position in microseconds
//-----------------------------------------------------------------------------------------------------------------
void setPenDownPosition(long position) {
  penDownPosition=position;
}

//-----------------------------------------------------------------------------------------------------------------
// Set state to a safe mode: Diable motors, put pen up, turn fan off
//-----------------------------------------------------------------------------------------------------------------
void turnOff(void){
  // Disable the stepper motor drivers
  digitalWrite(X_ENABLE_PIN, HIGH);  // Disable motor driver
  digitalWrite(Z_ENABLE_PIN, HIGH);  // Disable motor driver
  
  // Put the pen in the up position (disable might put it on the plot-paper-bed)
  penUp();

  // Turn the fan off
  fanOnOff(0);

  // Disable the serial interface, this to prevent new commands which could for instance put the pen up or down
  Serial.end();
}

//-----------------------------------------------------------------------------------------------------------------
// Pen up      the delay is required to not move before the pen is retracted
//-----------------------------------------------------------------------------------------------------------------
void penUp() {
  penA.writeMicroseconds(penUpPosition);
  penIsUp=true;
  delay(300);
}

//-----------------------------------------------------------------------------------------------------------------
//Pen down     the delay is required to not start drawing before the pen is down
//-----------------------------------------------------------------------------------------------------------------
void penDown() {
  penA.writeMicroseconds(penDownPosition);
  penIsUp=false;
  delay(300);
}

//-----------------------------------------------------------------------------------------------------------------
// Fan on/off (1=on, anything else = off)
//-----------------------------------------------------------------------------------------------------------------
void fanOnOff(long mode) {
  if (mode==1) {
    digitalWrite(FAN,HIGH);
  } else {
    digitalWrite(FAN,LOW);
  }
}

//-----------------------------------------------------------------------------------------------------------------
// Go to x=0, set zero position
//-----------------------------------------------------------------------------------------------------------------
void homeX(void) {
  // Move fast towards the zero point, then move slowly back until the end-stop switch opens
  while (digitalRead(X_MIN_PIN)) {    // 0=End switch closed   
    digitalWrite(X_DIR_PIN, LOW);     // 0=Move towards coordinate (0,0)
    digitalWrite(X_STEP_PIN, HIGH);
    delayMicroseconds(200);                       
    digitalWrite(X_STEP_PIN, LOW);
    delayMicroseconds(200);   
  }
  while (!digitalRead(X_MIN_PIN)) {   // 0=End switch closed   
    digitalWrite(X_DIR_PIN, HIGH);    // 1=Move away from coordinate (0,0)
    digitalWrite(X_STEP_PIN, HIGH);
    delay(20);                       
    digitalWrite(X_STEP_PIN, LOW);
    delay(20);   
  }

  // Set this position as the zero position for the X axis
  sX.setCurrentPosition(0);  
}

//-----------------------------------------------------------------------------------------------------------------
// Go to y=0, set zero position
//-----------------------------------------------------------------------------------------------------------------
void homeY(void) {
  // Move fast towards the zero point, then move slowly back until the end-stop switch opens
  while (digitalRead(Z_MIN_PIN)) {    // 0=End switch closed   
    digitalWrite(Z_DIR_PIN, LOW);     // 0=Move towards coordinate (0,0)
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(200);                       
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(200);   
  }
  while (!digitalRead(Z_MIN_PIN)) {   // 0=End switch closed   
    digitalWrite(Z_DIR_PIN, HIGH);    // 1=Move away from coordinate (0,0)
    digitalWrite(Z_STEP_PIN, HIGH);
    delay(20);                       
    digitalWrite(Z_STEP_PIN, LOW);
    delay(20);   
  }

  // Set this position as the zero position for the Y axis
  sY.setCurrentPosition(0);  
}

//-----------------------------------------------------------------------------------------------------------------
// Go to (0,0) and set this as zero position
//-----------------------------------------------------------------------------------------------------------------
void homeXY(void) {
  homeX();
  homeY();
}

//-----------------------------------------------------------------------------------------------------------------
// Move to (x0,y0)
//-----------------------------------------------------------------------------------------------------------------
void moveToXY(long x0, long y0) {
  // First pull the pen up
  if (!penIsUp) {
    penUp();
  }

  XY_Pos[XPOS]=x0;
  XY_Pos[YPOS]=y0;
  steppers.moveTo(XY_Pos);
  steppers.runSpeedToPosition();
}

//-----------------------------------------------------------------------------------------------------------------
// Draw a line from (x0,y0) to (x1,y1)
//-----------------------------------------------------------------------------------------------------------------
void drawLine(long x0, long y0, long x1, long y1) {
  // Check if (x0,y0) is equal to the current postion - if so, continue drawing, else move to (x0,y0)
  if ((sX.currentPosition()!=x0) || ((sY.currentPosition()!=y0))) {
    moveToXY(x0,y0);  
  }
  
  // First pull the pen down
  if (penIsUp) {
    penDown();
  }

  XY_Pos[XPOS]=x1;
  XY_Pos[YPOS]=y1;
  steppers.moveTo(XY_Pos);
  steppers.runSpeedToPosition();  
}

//-----------------------------------------------------------------------------------------------------------------
// Draw a line segment from the current position to (x1,y1)
//-----------------------------------------------------------------------------------------------------------------
void drawLineSegment(long x1, long y1) {
  // First pull the pen down
  if (penIsUp) {
    penDown();
  }

  XY_Pos[XPOS]=x1;
  XY_Pos[YPOS]=y1;
  steppers.moveTo(XY_Pos);
  steppers.runSpeedToPosition();     
}

//-----------------------------------------------------------------------------------------------------------------
// Draw a rectangle, startcoordinate is (x0,y0) with sides dx,dy  (x0,y0) is the upper left corner of the rectangle
//-----------------------------------------------------------------------------------------------------------------
void drawRectangle(long x0, long y0, long dx, long dy) {
  drawLine(x0   ,y0   ,x0+dx,y0   );
  drawLine(x0+dx,y0   ,x0+dx,y0+dy); 
  drawLine(x0+dx,y0+dy,x0   ,y0+dy);  
  drawLine(x0   ,y0+dy,x0   ,y0   );  
}






















