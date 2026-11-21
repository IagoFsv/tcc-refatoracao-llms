"""Cache whose values expire after a maximum age, with a readable repr.

Public entry point: run(entries, now). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""

import time
from contextlib import contextmanager


class _ExpiringDict(dict):
    """Dict-like cache for Hub API requests

    Values will expire after max_age seconds.

    A monotonic timer is used (time.monotonic).

    A max_age of 0 means cache forever.
    """

    max_age = 0
    purge_interval = 0

    def __init__(self, max_age=0, purge_interval="max_age"):
        self.max_age = max_age
        if purge_interval == "max_age":
            # default behavior: use max_age
            purge_interval = max_age
        self.purge_interval = purge_interval
        self.timestamps = {}
        self.values = {}
        self._last_purge = time.monotonic()

    def __len__(self):
        return len(self.values)

    def __setitem__(self, key, value):
        """Store key and record timestamp"""
        self._maybe_purge()
        self.timestamps[key] = time.monotonic()
        self.values[key] = value

    def __repr__(self):
        """include values and timestamps in repr"""
        now = time.monotonic()
        report = {}
        for key, value in self.values.items():
            report[key] = '{value} (age={age:.0f}s)'.format(
                value=repr(value)[:16] + '...', age=now - self.timestamps[key]
            )
        return repr(report)

    def __delitem__(self, key):
        del self.values[key]
        del self.timestamps[key]

    def _maybe_purge(self):
        """purge expired values _if_ it's been purge_interval since the last purge

        Called on every get/set, to keep the expired values clear.
        """
        if not self.purge_interval > 0:
            return
        now = time.monotonic()
        if self._last_purge < (now - self.purge_interval):
            self.purge_expired()

    def purge_expired(self):
        """Purge all expired values"""
        if not self.max_age > 0:
            return
        now = self._last_purge = time.monotonic()
        cutoff = now - self.max_age
        for key in list(self.timestamps):
            timestamp = self.timestamps[key]
            if timestamp < cutoff:
                del self[key]


@contextmanager
def _clock(reading):
    """Makes time.monotonic() return the given reading inside the block."""
    original = time.monotonic
    time.monotonic = lambda: reading
    try:
        yield
    finally:
        time.monotonic = original


def run(entries, now):
    """entries is a list of (key, value, stored_at): each value is stored when
    the monotonic clock reads stored_at. Returns the repr of the cache when the
    clock reads now. Public entry point of this unit."""
    cache = _ExpiringDict()
    for key, value, stored_at in entries:
        with _clock(stored_at):
            cache[key] = value
    with _clock(now):
        return repr(cache)
