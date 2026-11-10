import board
import pwmio
import digitalio
import rotaryio

class motor:
    def __init__(
        self, 
        pin1, 
        pin2, 
        enc_phase1, 
        enc_phase2,
        circumference, 
        max_speed,
        pulses_per_revolution=224.4,
        freq=20000,
    ):
        # initializes the motor driver with frequency.
        self.freq = freq
        
        # initializes the motor driver with the specified pins and frequency.
        # freq is 20000 Hz by default, which is a common frequency for PWM control of motors.
        self.pin_1 = pwmio.PWMOut(pin1, frequency=freq)
        self.pin_2 = pwmio.PWMOut(pin2, frequency=freq)
        
        # initializes the encoder pins.
        self.encoder = rotaryio.IncrementalEncoder(enc_phase2, enc_phase1)
        self.encoder.divisor = 1  # Set the encoder divider to 1 for full resolution

        # initializes the circumference of the wheel.
        self.circumference = circumference
        
        # initializes the maximum speed of the motor. This value is used to scale the speed input to the PWM duty cycle.
        self.max_speed = max_speed

        # initializes the number of pulses per revolution of the motor. This value is used to calculate the number of pulses needed to move a certain distance.
        self.pulses_per_revolution = pulses_per_revolution

    def set_speed(self, speed):
        # sets the speed of the motor. The speed parameter should be a float between -negative max_speed and positive max_speed. A positive speed value will rotate the motor in one direction, while a negative speed value will rotate it in the opposite direction. A speed of 0 will stop the motor.
        # realistically, this is only called directly to stop the motor.
        # most of the time, the motor is controlled by move_distance, which uses the encoder to determine when to stop.
        # in metric units.
        if speed > 0:
            self.pin_1.duty_cycle = int(speed / self.max_speed * 65535)
            self.pin_2.duty_cycle = 0
        elif speed < 0:
            self.pin_1.duty_cycle = 0
            self.pin_2.duty_cycle = int(-speed / self.max_speed * 65535)
        else:
            self.pin_1.duty_cycle = 65535
            self.pin_2.duty_cycle = 65535

    def get_sleep_state(self):
        # returns the current state of the sleep pin. True means the motor is asleep (off), and False means the motor is awake (on).
        return self.sleep.value

    def get_encoder_position(self):
        # returns the current position of the encoder. This value can be used to determine how far the motor has moved.
        return self.encoder.position

    def move_distance(self, distance, speed):
        # This function moves the motor a specified distance in meters (can be negative).
        # speed is a magnitude value that determines how fast the motor should move. The speed parameter should be a float between 0 and max_speed. (m/s)
        pulses_needed = int((distance / self.circumference) * self.pulses_per_revolution)
        
        # resets the encoder position to 0 before starting the movement.
        self.encoder.position = 0

        if pulses_needed < 0:
            speed = -speed  # Reverse direction if distance is negative
        
        # sets the motor speed.
        self.set_speed(speed)

        # if this is terminated, the motor will stop and the encoder interrupt will be disabled.
        try:
            # Move the motor until the desired number of pulses is reached.
            while abs(self.get_encoder_position()) < abs(pulses_needed):
                yield # This allows other tasks to run while waiting for the motor to reach the desired distance.
        finally:
            # Once the desired distance is reached, disable the encoder interrupt and stop the motor.
            self.set_speed(0)  # Stop the motor after reaching the desired distance