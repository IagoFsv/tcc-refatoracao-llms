"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def _split_and_map(self, values):
        return map(lambda x: map(lambda y: y.split(","), x.split(",")), values)

    def _convert_to_float(self, values):
        return map(lambda x: list(map(float, x)), values)

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        values = self.config[section][key].split(",")
        return self._convert_to_float(self._split_and_map(values))

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
        config = Config()
        config.config["world"] = {"regions": text}
        return _materialize(config.get_config_section_key_dict_dict_dict_float("world", "regions"))
