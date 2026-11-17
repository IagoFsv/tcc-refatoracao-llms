"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def _split_comma(self, value):
        return [x.split(',') for x in value.split(',')]

    def _split_comma_iter(self, values):
        return [self._split_comma(x) for x in values]

    def _split_comma_map(self, values):
        return map(lambda x: self._split_comma_iter(x), values)

    def _split_comma_map_iter(self, values):
        return map(lambda x: self._split_comma_map(x), values)

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return self._split_comma_map_iter(self.config[section][key].split(','))

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
        return _materialize(config.get_config_section_key_dict_dict_dict_list("world", "regions"))
