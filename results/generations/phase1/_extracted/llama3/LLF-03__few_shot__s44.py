"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self._format_value(value)
        self.logger.info("Config: " + str(self.config))

    def _format_value(self, value):
        return ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), x)), value))

    def run(self, value):
        """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
        config = self
        config.config["world"] = {}
        config.set_config_dict_dict_dict_dict("world", "regions", value)
        return config.config["world"]["regions"]
