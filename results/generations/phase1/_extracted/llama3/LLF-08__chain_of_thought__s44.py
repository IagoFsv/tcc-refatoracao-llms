"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return process_config_data(self, section, key)

    def process_config_data(self, section, key):
        """
        Processes the configuration data for the given section and key.
        Returns a list of integers.
        """
        return [
            [map(int, z.split(",")) for z in y.split(",")]
            for y in x.split(",")
        ] for x in self.config[section][key].split(",")


def _materialize(value):
    """Converts nested sequences (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items = iter(value)
    except TypeError:
        return value
    return [_materialize(item) for item in items]


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_int("world", "regions"))
