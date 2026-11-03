# Megan
# 10/14/2026
# This file where I try to figure out how to receive inputs ...
# ... the (food, street, avenue) to then convert that to an (x1,y1)...
# ... coordinate to then convert that to a possible robot location ...
# ... (x2,y2) to then send to Kevin's Kool Algorithm (KKA) for KKA ...
# ... to convert that to a path for the robot to follow.....
# ... plus more stuff later. 

# Questions: 
# 1. How does the CPU receive the input from the outside?

# Inputs going in: food, street, avenue

# https://stackoverflow.com/questions/71095652/is-it-possible-to-get-user-input-with-micro-python

"""
import sys

print("What is the Answer to the Ultimate Question of Life, the Universe, and Everything?")
answer = sys.stdin.readline()
if answer == "42\n":
    print("correct!")
else:
    print("incorrect!");
"""

import sys

print("Food: ")
food = sys.stdin.readline()
print("Street: ")
street = sys.stdin.readline()
print("Avenue: ")
avenue = sys.stdin.readline()

# Variables 

# All bs numbers (in inches) that we'll change later once the rules are set
line_thickness = 1;
cup_diameter = 3;
cell_width = 10;

# Gets the address and assigns them to x and y coordinates
x_coord = 0;

if avenue == "Dufferin":
    x_coord = 1;
elif avenue == "Bathurst":
    x_coord = 2;
elif avenue == "Yonge":
    x_coord = 3;
elif avenue == "Parliament":
    x_coord = 4;
else:
    print("Bro, this ain't even a valid avenue fr :skull: or maybe it's a capitalization problem, try it with the first letter capitalized ig" );

y_coord = 0;

if street == "Bloor":
    y_coord = 1;
elif street == "College":
    y_coord = 2;
elif street == "Dundas":
    y_coord = 3;
elif street == "Queen":
    y_coord = 4;
elif street == "King":
    y_coord = 5;
elif street == "Front":
    y_coord = 6;
elif street == "Lakeshore":
    y_coord = 7;
elif street == "Starting":
    y_coord = 8;
else:
    print("Bro, this ain't even a valid street smh :skull: or maybe it's a capitalization problem, try it with the first letter capitalized ig" );

