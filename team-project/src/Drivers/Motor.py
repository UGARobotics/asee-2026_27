import board
import pwmio
import digitalio
import rotaryio

class Motor:
    def __init__(
        self, 
        pin1, 
        pin2, 
        enc_phase1, 
        enc_phase2,
        max_speed,
        freq
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
        
        # initializes the maximum speed of the motor. This value is used to scale the speed input to the PWM duty cycle.
        self.max_speed = max_speed

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

    def get_encoder_position(self):
        # returns the current position of the encoder. This value can be used to determine how far the motor has moved.
        return self.encoder.position