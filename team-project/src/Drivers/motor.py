from machine import Pin, PWM

class motor:
    # defines the pins for the motor driver and encoder.
    # One full rotation is 224.4 pulses (see motor specs).
    # all of this values are going to be in config.py, but for now, they are hardcoded here.
    def __init__(
        self, 
        pin1, 
        pin2, 
        enc_phase1, 
        enc_phase2, 
        sleep, 
        circumference, 
        max_speed,
        pulses_per_revolution=224.4,
        freq=20000,
        enc_counter=0
    ):
        # initializes the motor driver with frequency.
        self.freq = freq
        
        # initializes the motor driver with the specified pins and frequency.
        # freq is 20000 Hz by default, which is a common frequency for PWM control of motors.
        self.pin_1 = PWM(Pin(pin1), freq=freq)
        self.pin_2 = PWM(Pin(pin2), freq=freq)
        
        # initializes the encoder pins.
        self.enc_phase1 = Pin(enc_phase1, Pin.IN)
        self.enc_phase2 = Pin(enc_phase2, Pin.IN)
        
        # initializes the sleep pin.
        self.sleep = Pin(sleep, Pin.OUT)
        
        # initializes the encoder counter.
        self.enc_counter = enc_counter

        # initializes the circumference of the motor.
        self.circumference = circumference
        
        # initializes the number of pulses per revolution of the motor.
        self.max_speed = max_speed

        # initializes the number of pulses per revolution of the motor. This value is used to calculate the number of pulses needed to move a certain distance.
        self.pulses_per_revolution = pulses_per_revolution

    # speed is from -max_speed to max_speed
    # realistically, this is only called directly to stop the motor.
    # most of the time, the motor is controlled by move_distance, which uses the encoder to determine when to stop.
    # in metric units.
    def set_speed(self, speed):
        # sets the speed of the motor. The speed parameter should be a float between -negative max_speed and positive max_speed. A positive speed value will rotate the motor in one direction, while a negative speed value will rotate it in the opposite direction. A speed of 0 will stop the motor.
        if speed > 0:
            self.pin_1.duty_u16(int(speed / self.max_speed * 65535))
            self.pin_2.duty_u16(0)
        elif speed < 0:
            self.pin_1.duty_u16(0)
            self.pin_2.duty_u16(int(-speed / self.max_speed * 65535))
        else:
            self.pin_1.duty_u16(65535)
            self.pin_2.duty_u16(65535)

    # sleeps the motor driver and takes inputs 0 (off) of 1 (on)
    # sleep must be 1 for the motor to run.
    def sleep_motor(self, value):
        self.sleep.value(value)

    def get_sleep_state(self):
        # returns the current state of the sleep pin. A value of 1 indicates that the motor driver is active, while a value of 0 indicates that it is in sleep mode.
        return self.sleep.value()

    def encoder_callback(self, pin):
        # This function is called whenever the encoder detects a change in position.
        # It updates the encoder counter based on the direction of rotation.
        if self.enc_phase2.value() == 0:
            self.enc_counter += 1
        else:
            self.enc_counter -= 1

    # mag speed is from 0 to max_speed, and distance is in meters.
    def move_distance(self, distance, mag_speed):
        # This function moves the motor a specified distance in meters.
        # It calculates the number of pulses required to move the specified distance based on the circumference of the motor and the number of pulses per revolution.
        pulses_needed = int((distance / self.circumference) * self.pulses_per_revolution)
        self.enc_counter = 0  # Reset encoder counters

        if pulses_needed < 0:
            mag_speed = -mag_speed  # Reverse direction if distance is negative
        
        # Set up the encoder interrupt to call the encoder_callback function whenever a rising edge is detected on enc_phase1.
        self.enc_phase1.irq(trigger=Pin.IRQ_RISING, handler=self.encoder_callback)

        # Set the motor speed to the specified magnitude. The motor will continue to move until the desired number of pulses is reached.
        self.set_speed(mag_speed)  # Set a constant speed for movement
        
        # if this is terminated, the motor will stop and the encoder interrupt will be disabled.
        try:
            # Move the motor until the desired number of pulses is reached.
            while abs(self.enc_counter) < abs(pulses_needed):
                yield # This allows other tasks to run while waiting for the motor to reach the desired distance.
        finally:
            # Once the desired distance is reached, disable the encoder interrupt and stop the motor.
            self.enc_phase1.irq(trigger=Pin.IRQ_RISING, handler=None)  # Disable the encoder interrupt
            self.set_speed(0)  # Stop the motor after reaching the desired distance