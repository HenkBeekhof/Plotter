#--------------------------------------------------------------------------------------------------
# Module  : proj_settings
# Contains: Project settigns and Configuration
# Created : HW Beekhof 2018 http://www.hwbbox.com
#--------------------------------------------------------------------------------------------------
from func_communication import *


class Settings:
    def __init__(self, plotmode=1):
        self.set_plotmode(plotmode)

    def set_plotmode(self,pm):
        self.plotmode=pm

    SIMU=1
    PLOT=2

# Initialize Project Settings
ps=Settings()

# Initialize Project Settings
#ps.set_plotmode(ps.PLOT)

# Initialize Serial Communication if the mode is PLOT-mode
if (ps.plotmode==ps.PLOT):
    sc=SerialCommunication()
    sc.home_xy()

# func_plot uses the above defined project settings class named ps, therefor this import is put here, after
# the creation of ps
from func_plot import *

# Instantiate the plotter
plotter=Plot()
