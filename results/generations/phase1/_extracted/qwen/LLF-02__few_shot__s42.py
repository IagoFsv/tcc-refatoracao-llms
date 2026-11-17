"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = self._join_lists(value)
        self.logger.info("Config: " + str(self.config))

    def _join_lists(self, value):
        return ",".join(map(self._join_pairs, value))

    def _join_pairs(self, pair):
        return ",".join(map(self._join_items, pair))

    def _join_items(self, item):
        return ",".join(item)


def run(value):
    """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {}
    config.set_config_dict_dict_dict_list("world", "regions", value)
    return config.config["world"]["regions"]
