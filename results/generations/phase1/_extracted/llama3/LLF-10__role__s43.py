"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def _get_config_section_key_dict_dict_dict_bool(self, section, key):
        config_value = self.config[section][key]
        return [
            [
                [
                    bool(z.split(","))
                    for z in y.split(",")
                ]
                for y in x.split(",")
            ]
            for x in config_value.split(",")
        ]

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
        return _materialize(self._get_config_section_key_dict_dict_dict_bool("world", "regions"))
