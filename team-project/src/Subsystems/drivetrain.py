from Drivers.motor_driver import MotorDriver

class Drivetrain: 
    def __init__(self, config):
        dt_cfg = config['drivetrain']

        # Instantiate all motors (assuming 4 motors for a 4WD robot)
        self.l = MotorDriver(**dt_cfg['left'])
        self.r = MotorDriver(**dt_cfg['right'])

    def tank_drive(self, left_speed, right_speed):
        """
        Tank drive control for the drivetrain.
        left_speed: Speed for the left motors (-65535 to 65534)
        right_speed: Speed for the right motors (-65535 to 65534)
        """
        self.l.drive(left_speed)
        self.r.drive(right_speed)

    def stop(self):
        self.tank_drive(0, 0)


    def get_encoder_counts(self):
        """
        Returns a dictionary with the encoder counts for each motor.
        """
        return {
            'front_left': self.l.get_encoder_count(),
            'front_right': self.r.get_encoder_count()
        }