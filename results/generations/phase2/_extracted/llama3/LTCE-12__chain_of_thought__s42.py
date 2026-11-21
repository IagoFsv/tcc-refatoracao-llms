"""Name of the logger used by a class.

Public entry point: run(logged_class, config_logger_name=None,
class_logger_name=None). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

from __future__ import annotations

from typing import TypeVar

_T = TypeVar("_T")


class LoggingMixin:
    """Convenience super-class to have a logger configured with the class name."""

    @staticmethod
    def _create_logger_name(
        logged_class: type[_T],
        log_config_logger_name: str | None = None,
        class_logger_name: str | None = None,
    ) -> str:
        """Generate a logger name for the given `logged_class`."""
        logger_name: str = (
            class_logger_name
            if class_logger_name is not None
            else f"{logged_class.__module__}.{logged_class.__name__}"
        )

        if log_config_logger_name:
            if logger_name:
                logger_name = f"{log_config_logger_name}.{logger_name}"
            else:
                logger_name = log_config_logger_name
        return logger_name


def run(logged_class, config_logger_name=None, class_logger_name=None):
    """Returns the logger name for the class. Public entry point of this unit."""
    return LoggingMixin._create_logger_name(logged_class, config_logger_name, class_logger_name)
