from Drivers import motor
import time
import board
import pwmio

def main():
    my_motor = motor.Motor(31, 32, None, None, None, 251)
   
    while true:
        my_motor.set_speed(100)  # Set motor speed to 50%
        time.sleep(2)  # Run motor for 2 seconds
        my_motor.set_speed(0)  # Stop the motor
        time.sleep(1)  # Wait for 1 second
        my_motor.set_speed(-100)  # Set motor speed to -50% (reverse)
        time.sleep(2)  # Run motor in reverse for 2 seconds
        my_motor.set_speed(0)  # Stop the motor
        time.sleep(1)  # Wait for 1 second

if __name__ == "__main__":
    main()