#--------------------------------------------------------------------------------------------------
# Module  : plotter
# Contains: Main program
# Created : HW Beekhof 2018 http://www.hwbbox.com
#--------------------------------------------------------------------------------------------------
from proj_settings import *
from func_applications import *
from func_spiro import main_spiro
from func_koch_model import main_koch_model
from func_koch import print_koch
from func_abstract_img import plot_img_to_lines

application=3

if (application==0):
    test_distances(3)

if (application==1):
    test_charset()

if (application==2):
    img_to_ascii()

if (application==3):
    random_diagram()

if (application==4):
    print_ascii_art_file()

if (application==6):
    main_koch_model()

if (application==7):
    print_koch()

if (application==8):
    plot_img_to_lines()

while (1):
    pass






