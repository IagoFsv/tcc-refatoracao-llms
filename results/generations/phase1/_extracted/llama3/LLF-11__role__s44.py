"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        def parse_value(pairs):
            return [pair.split(",") for pair in pairs]

        return map(lambda x: map(parse_value, map(lambda y: parse_value(y.split(",")), x.split(","))), self.config[section][key].split(","))

    def _materialize(self, value):
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
        return self._materialize(self.get_config_section_key_dict_dict_dict_list("world", "regions"))
