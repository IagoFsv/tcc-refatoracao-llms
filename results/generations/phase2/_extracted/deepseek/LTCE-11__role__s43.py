"""Context manager that checks that a block raises one of the expected errors.

Public entry point: run(expected_exc_type, match=None, error=None,
may_pass=False, err_msg=None). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

import contextlib
import re
from collections.abc import Iterable


class _Raises(contextlib.AbstractContextManager):
    # see raises() for parameters
    def __init__(self, expected_exc_type, match, may_pass, err_msg):
        self.expected_exc_types = (
            expected_exc_type
            if isinstance(expected_exc_type, Iterable)
            else [expected_exc_type]
        )
        self.matches = [match] if isinstance(match, str) else match
        self.may_pass = may_pass
        self.err_msg = err_msg
        self.raised_and_matched = False

    def __exit__(self, exc_type, exc_value, _):
        # see
        # https://docs.python.org/2.5/whatsnew/pep-343.html#SECTION0009100000000000000000

        if exc_type is None:   # No exception was raised in the block
            if self.may_pass:
                return True   # CM is happy
            else:
                err_msg = self.err_msg or f"Did not raise: {self.expected_exc_types}"
                raise AssertionError(err_msg)

        if not any(
            issubclass(exc_type, expected_type)
            for expected_type in self.expected_exc_types
        ):
            if self.err_msg is not None:
                raise AssertionError(self.err_msg) from exc_value
            else:
                return False   # will re-raise the original exception

        if self.matches is not None:
            err_msg = self.err_msg or (
                "The error message should contain one of the following "
                "patterns:\n{}\nGot  {}".format("\n".join(self.matches), str(exc_value))
            )
            if not any(re.search(match, str(exc_value)) for match in self.matches):
                raise AssertionError(err_msg) from exc_value
            self.raised_and_matched = True

        return True


def run(expected_exc_type, match=None, error=None, may_pass=False, err_msg=None):
    """Runs a block that raises error (or nothing, if error is None) inside the
    context manager and returns whether the error was raised and matched.
    Public entry point of this unit."""
    checker = _Raises(expected_exc_type, match, may_pass, err_msg)
    with checker:
        if error is not None:
            raise error
    return checker.raised_and_matched
