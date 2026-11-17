"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def _split_and_map(self, s):
        return list(map(lambda x: map(lambda y: map(bool, y.split(",")), x.split(",")), s.split(",")))

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return self._split_and_map(self.config[section][key])

    def _materialize(value):
        """Converts nested sequences (including iterators) into lists."""
        if isinstance(value, str):
            return value
        try:
            items = iter(value)
        except TypeError:
            return value
        return [_materialize(item) for item in items]

    def run(self, text):
        """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
        self.config["world"] = {"regions": text}
        return _materialize(self.get_config_section_key_dict_dict_dict_bool("world", "regions"))
