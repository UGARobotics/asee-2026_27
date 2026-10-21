from Drivers.motor import motor

class Drivetrain: 
    def __init__(self, config):
        dt_cfg = config['drivetrain']

        # Instantiate all motors (assuming 2 motors for a 2WD robot)
        self.l = motor(
            dt_cfg['Motor_1_Pin_1'], 
            dt_cfg['Motor_1_Pin_2'], 
            dt_cfg['Motor_1_Enc_Phase1'], 
            dt_cfg['Motor_1_Enc_Phase2'], 
            dt_cfg['Motor_1_Sleep'], 
            dt_cfg['Wheel_Circumference'], 
            dt_cfg['Max_Speed']
        )
        self.r = motor(
            dt_cfg['Motor_2_Pin_1'], 
            dt_cfg['Motor_2_Pin_2'], 
            dt_cfg['Motor_2_Enc_Phase1'], 
            dt_cfg['Motor_2_Enc_Phase2'], 
            dt_cfg['Motor_2_Sleep'], 
            dt_cfg['Wheel_Circumference'], 
            dt_cfg['Max_Speed']
        )

    def tank_drive(self, left_speed, right_speed, distance):
        """
        Tank drive control for the drivetrain.
        left_speed: Speed for the left motors (-65535 to 65534)
        right_speed: Speed for the right motors (-65535 to 65534)
        """
        self.l.move_distance(-distance, left_speed)
        self.r.move_distance(distance, right_speed)

    def stop(self):
        self.tank_drive(0, 0, 0)  # Stop both motors


    def get_encoder_counts(self):
        """
        Returns a dictionary with the encoder counts for each motor.
        """
        return {
            'front_left': self.l.get_encoder_count(),
            'front_right': self.r.get_encoder_count()
        }