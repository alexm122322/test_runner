

from logging import StreamHandler, FileHandler, DEBUG, Logger

from ..utils import DateTimeManager
from ..config.test_config import TestsConfig


def init_logger(config: TestsConfig, logger_name: str) -> Logger:
    logger = Logger(logger_name, DEBUG)
    if config.enable_print_to_file:

        file_handler = FileHandler(_create_file_name(config))
        file_handler.setFormatter(config.file_formatter)
        logger.addHandler(file_handler)

    text_handler = StreamHandler()
    text_handler.setFormatter(config.text_formatter)
    logger.addHandler(text_handler)
    return logger


def _create_file_name(config: TestsConfig) -> str:
    datatime_manager = DateTimeManager()
    file_name = str(config.print_file_format)
    file_name = file_name.replace('{datetime}', datatime_manager.now_str(config.print_file_datetime))
    file_name = file_name.replace('{name}', config.print_file_name)
    file_name = file_name.replace(' ', '_')
    return file_name
