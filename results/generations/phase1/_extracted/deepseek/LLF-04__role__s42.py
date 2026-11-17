"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        self.config[section][key] = self.join_values(value)
        self.logger.info("Config: " + str(self.config))

    def join_values(self, value):
        return ",".join(self.map_values(value))

    def map_values(self, value):
        return map(self.join_values_2, value)

    def join_values_2(self, value):
        return ",".join(map(self.join_values_3, value))

    def join_values_3(self, value):
        return ",".join(map(self.join_values_4, value))

    def join_values_4(self, value):
        return ",".join(map(str, value))


def run(value):
    """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {}
    config.set_config_dict_dict_dict_dict_int("world", "regions", value)
    return config.config["world"]["regions"]
