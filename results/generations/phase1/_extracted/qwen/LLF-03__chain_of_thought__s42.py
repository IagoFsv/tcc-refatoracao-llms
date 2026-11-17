"""Stores nested values in the game configuration, as text.

Public entry point: run(value). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def flatten_and_join(self, nested_list):
        """Flattens a nested list and joins elements with commas."""
        def flatten(sublist):
            for item in sublist:
                if isinstance(item, list):
                    yield from flatten(item)
                else:
                    yield item
        
        return ",".join(map(str, flatten(nested_list)))

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self.flatten_and_join(value)
        self.logger.info("Config: " + str(self.config))


def run(value):
    """Stores value in the configuration and returns the stored text. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {}
    config.set_config_dict_dict_dict_dict("world", "regions", value)
    return config.config["world"]["regions"]
