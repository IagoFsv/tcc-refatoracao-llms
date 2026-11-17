"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def _split_pairs(self, pairs):
        return list(map(lambda x: list(map(lambda y: y.split(","), x.split(","))), pairs))

    def _get_config_section_key_dict_dict_dict_list(self, section, key):
        return self._split_pairs(self.config[section][key].split(","))

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
        config = self
        config.config["world"] = {"regions": text}
        return self._materialize(self._get_config_section_key_dict_dict_dict_list("world", "regions"))
