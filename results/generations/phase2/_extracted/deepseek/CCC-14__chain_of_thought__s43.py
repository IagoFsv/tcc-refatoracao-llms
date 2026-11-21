def __repr__(self):
    """include values and timestamps in repr"""
    now = time.monotonic()
    values_and_ages = {}
    for key, value in self.values.items():
        age = now - self.timestamps[key]
        values_and_ages[key] = '{value} (age={age:.0f}s)'.format(
            value=repr(value)[:16] + '...', age=age
        )
    return repr(values_and_ages)
