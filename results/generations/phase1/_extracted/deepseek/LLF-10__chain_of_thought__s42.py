class Config(object):
    def  __init__(self):
        self.config  = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return map(self._split_and_convert, self.config[section][key].split(","))

    def _split_and_convert(self, value):
        return map(self._split_and_convert_2, value.split(","))

    def _split_and_convert_2(self, value):
        return map(self._split_and_convert_3, value.split(","))

    def _split_and_convert_3(self, value):
        return map(bool, value.split(","))


def _materialize(value):
    """Converts nested sequences  (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items  = iter(value)
    except TypeError:
        return value
    return [_materialize(item) for item in items]


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config  = Config()
    config.config["world"]  = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_bool("world", "regions"))


def test_run():
    text = "1,2,3"
    assert run(text) == [[[['1', '2', '3']]]]

test_run()
