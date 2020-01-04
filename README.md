# Plotter - A0 size - Self made: 3D printed parts + Software

Content
* Manual (PDF) describing the components and build instructions
* Ploter / img / ASCII directory: Contains Python application + examples to plot
* Plotter_firmware directory: Contains Arduino source code for ATMEGA2560+RAMPS to control the plotter
* Plotter_3D_Components directory: Contains STL files of the plotter parts

The manual should explain how all parts fit together. It also describes which additional rods, supply, etc. is used.
The software contains out of two parts: 

Part1:
One part does the low level control of the stepper motors. This part accepts commands as input, such as "Draw a line", 
or "Goto that position". This part uses an ATMEGA2560 board with the RAMPS board as extension.

Part 2:
The second part runs on the PC, it is responsible for 'converting an idea' into commands. These commands are send to 
the plotter over USB. This part is written in Python. Several examples are included. Also a 'simulator' is included which
mimics the plotter by generating a drawing based on the commands it receives. 

The information can also be found on Pinshape:
https://pinshape.com/items/46225-3d-printed-a0-flexible-sized-plotter-including-software

For pictures: See the manual, or see Pinshape.
![plotter](https://github.com/HenkBeekhof/Plotter/images/3d-plotter.png "When ready it looks like this")

![Darth Vader Plot](https://github.com/HenkBeekhof/Plotter/images/DV_plot.png "Darth Vader Plot")

![Starbucks Plot](https://github.com/HenkBeekhof/Plotter/images/Starbucks_plot.png "Starbucks Plot") 
