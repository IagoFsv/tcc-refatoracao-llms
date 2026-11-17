"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_nested_lists(self, nested_lists):
        return ",".join(map(self.join_nested_lists, nested_lists)) if isinstance(nested_lists, list) else str(nested_lists)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = self.join_nested_lists(value)
        self.logger.info("Config: " + str(self.config))


def run(value):
    """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {}
    config.set_config_dict_dict_dict_list("world", "regions", value)
    return config.config["world"]["regions"]
