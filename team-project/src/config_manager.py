import json
import os

# this class is meant for writing to the config.json file
# in other words, updating the configuration of the robot
class configManager:
    def __init__(self, config_path):
        # initializes the configManager with the path to the configuration file.
        self.config_path = config_path

    def load_config(self):
        # loads the configuration from the specified JSON file.
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        return config

    def save_config(self, config):
        # saves the provided configuration to the specified JSON file.
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)