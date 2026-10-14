import json
import os
from config_manager import configManager
from Subsystems.drivetrain import Drivetrain
import time

# This is the main class for the robot. 
# It will handle the main loop and call the appropriate functions from other classes.
def main():
    #load configuration from config.json
    cfg_manager = configManager("config/config.json") #string is path to the manager
    config = cfg_manager.load_config() if hasattr(cfg_manager, 'load_config') else cfg_manager  # Load the configuration

    # Initialize the drivetrain subsystem
    drivetrain = Drivetrain(config)

    print("DriveTrain initialized. Starting main loop...")

    # % speed of 65536 is roughly 32768. This will be used to test the motors at half speed.
    test_speed = 32768

    try: 
        drivetrain.tank_drive(test_speed, test_speed)  # Drive forward at half speed
        time.sleep(2)  # Drive for 2 seconds
        drivetrain.stop()  # Stop the robot

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Stopping the robot.")
        drivetrain.stop()  # Ensure the robot stops if interrupted

if __name__ == "__main__":
    main()

