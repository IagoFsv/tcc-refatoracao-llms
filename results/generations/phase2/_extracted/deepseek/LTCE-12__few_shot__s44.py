from __future__ import annotations
from typing import TypeVar

_T = TypeVar("_T")


class LoggingMixin:
    @staticmethod
    def _create_logger_name(
        logged_class: type[_T],
        log_config_logger_name: str | None = None,
        class_logger_name: str | None = None,
    ) -> str:
        logger_name: str
        if class_logger_name is not None:
            logger_name = class_logger_name
        else:
            logger_name = f"{logged_class.__module__}.{logged_class.__name__}"

        if log_config_logger_name:
            return (
                f"{log_config_logger_name}.{logger_name}" if logger_name else log_config_logger_name
            )
        return logger_name


def run(logged_class, config_logger_name=None, class_logger_name=None):
    return LoggingMixin._create_logger_name(logged_class, config_logger_name, class_logger_name)
