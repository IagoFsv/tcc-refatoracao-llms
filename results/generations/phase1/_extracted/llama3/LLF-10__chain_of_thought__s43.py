"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        values = self.config[section][key].split(",")
        processed_values = list(map(self.process_config_value, values))
        return list(map(bool, processed_values))

    def process_config_value(self, value):
        return bool(value.strip(","))

    def _materialize(self, value):
        """Converts nested sequences (including iterators) into lists."""
        if isinstance(value, str):
            return value
        try:
            items = iter(value)
        except TypeError:
            return value
        return list(map(self._materialize, items))

    def run(self, text):
        """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
        self.config["world"] = {"regions": text}
        return self._materialize(self.get_config_section_key_dict_dict_dict_bool("world", "regions"))
