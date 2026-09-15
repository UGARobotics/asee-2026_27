#asee-2026_27
This is the program for ASEE competition robot 2026-2027
should be updated to include the following: 
->Robot's name and summary of what it does
->hardware requirements
-> the process requried to run the robot

What needs to be researched: 
What Python Libraries are needed for running a physical robot?



Current information:

Config is for the constants requried for calculation in regards to the robot.

currently includes (none of these are set in stone and can be removed or changed): 
-> Name of the robot
-> wheel_diameter_mm
-> max_speed_mps
-> sensor_pins

Drivers are meant for individual parts (I.E a motor, or a sensor)
Subsystems are meant for a group of parts (like an arm, or a drivetrain)


utils will likely be replaced by something else, as of now it is a placeholder for algorithm classes, etc.
the data folder is supposed to be for storing telemetry, and other data that we might need to collect through testing.
Config manager provides an easier way to edit the configs on the fly (like during a match potentially)

__init__.py is something that I am not completely sure is necessary, but from my research is it required for the use of packaging (and importing) throughout the program. 