import yaml


class Config:
    PROPERTIES = {}

    @staticmethod
    def load_config(config_file):
        with open(config_file, "r") as stream:
            Config.PROPERTIES = yaml.safe_load(stream)
    
    def get(*args):
        value_to_return = Config.PROPERTIES
        for arg in args:
            value_to_return = value_to_return[arg]
        return value_to_return

