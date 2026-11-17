"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def format_value(self, value):
        return ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(map(str, z)), y)), x)), value))

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.format_value(value)
        self.logger.info("Config: " + str(self.config))

    def run(self, value):
        """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
        config = Config()
        config.config["world"] = {}
        config.set_config_dict_dict_dict_dict_float("world", "regions", value)
        return config.config["world"]["regions"]
