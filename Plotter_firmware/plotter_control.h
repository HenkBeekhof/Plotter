#ifndef PLOTTER_CONTROL
#define PLOTTER_CONTROL

#define XPOS               0          // Index of the X position in the XY-position array for multistepper library
#define YPOS               1          // Index of the Y position in the XY-position array for multistepper library

void init_plotter();
void setSpeedX(long);
void setSpeedY(long);
void setPenUpPosition(long);
void setPenDownPosition(long);
void turnOff(void);
void penUp(void);
void penDown(void);
void fanOnOff(long);
void homeX(void);
void homeY(void);
void homeXY(void);
void moveToXY(long, long);
void drawLine(long, long, long, long);
void drawLineSegment(long, long);
void drawRectangle(long, long, long, long);

#endif

