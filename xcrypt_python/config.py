import yaml

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.read_config()

    def read_config(self):
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def write_config(self, data):
        with open(self.config_file, 'w') as file:
            yaml.safe_dump(data, file)

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self.write_config(self.config_data)
