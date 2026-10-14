from Drivers.motor_driver import MotorDriver

class Drivetrain: 
    def __init__(self, config):
        dt_cfg = config['drivetrain']

        # Instantiate all motors (assuming 4 motors for a 4WD robot)
        self.fl = MotorDriver(**dt_cfg['front_left'])
        self.fr = MotorDriver(**dt_cfg['front_right'])
        self.bl = MotorDriver(**dt_cfg['back_left'])
        self.br = MotorDriver(**dt_cfg['back_right'])

    def tank_drive(self, left_speed, right_speed):
        """
        Tank drive control for the drivetrain.
        left_speed: Speed for the left motors (-65535 to 65534)
        right_speed: Speed for the right motors (-65535 to 65534)
        """
        self.fl.drive(left_speed)
        self.bl.drive(left_speed)
        self.fr.drive(right_speed)
        self.br.drive(right_speed)
                      
    def stop(self):
        self.tank_drive(0, 0)


    def get_encoder_counts(self):
        """
        Returns a dictionary with the encoder counts for each motor.
        """
        return {
            'front_left': self.fl.get_encoder_count(),
            'front_right': self.fr.get_encoder_count(),
            'back_left': self.bl.get_encoder_count(),
            'back_right': self.br.get_encoder_count()
        }