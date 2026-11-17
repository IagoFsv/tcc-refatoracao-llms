"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def _process_region(self, region):
        return ",".join(",".join(",".join(z) for z in y) for y in region)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = list(map(self._process_region, value))
        self.logger.info("Config: " + str(self.config))

    def run(self, value):
        """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
        self.config["world"] = {}
        self.set_config_dict_dict_dict_list("world", "regions", value)
        return self.config["world"]["regions"]
