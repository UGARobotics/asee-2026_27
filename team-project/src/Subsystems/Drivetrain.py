from ..Drivers.Motor import Motor
from pathlib import Path
import json

"""
Note: Without IMU specification, the robot will not be able to rotate.
I will not implement rotation functionality in this class until the IMU is specified.
"""
class Drivetrain: 
    def __init__(self):
        config_path = Path(__file__).resolve().parents[2] / "config" / "config.json"
        with config_path.open("r", encoding="utf-8") as file:
            self.config = json.load(file)
        
        dt_cfg = self.config['drivetrain']
        circumference = dt_cfg['WHEEL_CIRCUMFERENCE']
        pulses_per_revolution = dt_cfg['PULSES_PER_REVOLUTION']

        # Instantiate all motors (assuming 2 motors for a 2WD robot)
        self.l = Motor(
            dt_cfg['MOTOR_L_IN_1'], 
            dt_cfg['MOTOR_L_IN_2'], 
            dt_cfg['MOTOR_L_PHASE_A'], 
            dt_cfg['MOTOR_L_PHASE_B'],  
            dt_cfg['MAX_SPEED'],
            dt_cfg['FREQUENCY']
        )
        self.r = Motor(
            dt_cfg['MOTOR_R_IN_1'], 
            dt_cfg['MOTOR_R_IN_2'], 
            dt_cfg['MOTOR_R_PHASE_A'], 
            dt_cfg['MOTOR_R_PHASE_B'],  
            dt_cfg['MAX_SPEED'],
            dt_cfg['FREQUENCY']
        )

    def set_speed(self, left_speed, right_speed):
        """
        Set the speed of the left and right motors.
        left_speed: Speed for the left motor (positive for forward, negative for backward).
        right_speed: Speed for the right motor (positive for forward, negative for backward).
        """
        self.l.set_speed(left_speed)
        self.r.set_speed(right_speed)

    def stop(self):
        """
        Stop both motors.
        """
        self.set_speed(0, 0)
    
    def move_distance(self, distance, speed):
        """
        Drive the robot forward or backward a certain distance at a specified speed.
        speed: The speed at which to drive (positive only, in m/s).
        distance: The distance to drive (positive or negative, in meters).
        """
        pulses_needed = int((distance / self.circumference) * self.pulses_per_revolution)
        
        # resets the encoder position to 0 before starting the movement.
        self.l.encoder.position = 0
        self.r.encoder.position = 0

        if pulses_needed < 0:
            speed = -speed  # Reverse direction if distance is negative
        
        # sets the motor speed.
        self.set_speed(speed, speed)

        # if this is terminated, the motors will stop.
        try:
            # Move the motors until the desired number of pulses is reached.
            while abs(self.l.get_encoder_position()) < abs(pulses_needed) and abs(self.r.get_encoder_position()) < abs(pulses_needed):
                yield # This allows other tasks to run while waiting for the motors to reach the desired distance.
        finally:
            # Once the desired distance is reached, stop the motors.
            self.stop()