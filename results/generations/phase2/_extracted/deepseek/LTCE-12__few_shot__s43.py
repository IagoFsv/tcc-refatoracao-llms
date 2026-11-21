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
        """Generate a logger name for the given `logged_class`.

        By default, this function returns the `class_logger_name` as logger name. If it is not provided,
        the  {class.__module__}.{class.__name__} is returned instead. When a `parent_logger_name` is provided,
        it will prefix the logger name with a separating dot.
        """
        if class_logger_name is not None:
            logger_name = class_logger_name
        else:
            logger_name = f"{logged_class.__module__}.{logged_class.__name__}"

        if log_config_logger_name:
            return f"{log_config_logger_name}.{logger_name}" if logger_name else log_config_logger_name
        return logger_name


def run(logged_class, config_logger_name=None, class_logger_name=None):
    """Returns the logger name for the class. Public entry point of this unit."""
    return LoggingMixin._create_logger_name(logged_class, config_logger_name, class_logger_name)
