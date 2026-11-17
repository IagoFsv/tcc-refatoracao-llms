"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, value):
        return ",".join(map(self.join_values_helper, value))

    def join_values_helper(self, value):
        return ",".join(map(self.join_values_helper_inner, value))

    def join_values_helper_inner(self, value):
        return ",".join(map(str, value))

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.join_values(value)
        self.logger.info("Config: " + str(self.config))


def run(value):
    """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {}
    config.set_config_dict_dict_dict_dict_float("world", "regions", value)
    return config.config["world"]["regions"]
