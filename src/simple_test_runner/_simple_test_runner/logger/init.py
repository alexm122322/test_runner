from logging import StreamHandler, FileHandler, DEBUG, Logger

from ..utils import DateTimeManager
from ..config.test_config import TestsConfig


def init_logger(config: TestsConfig, logger_name: str) -> Logger:
    """Logger initialization. Creates and sets up Logger.

    Args:
        config: User test config.
        logger_name: Name of Logger.

    Returns:
        Logger: Configured Logger.
    """

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
    """Utils function which helps to create a name for recording the file.
    config.print_file_format should contain {datetime} and {name}.
    
    Args:
        config: User test config.

    Returns:
        str: Name of file.
    """

    datatime_manager = DateTimeManager()
    now_str = datatime_manager.now_str(config.print_file_datetime)
    file_name = str(config.print_file_format)

    if '{datetime}' in file_name:
        file_name = file_name.replace('{datetime}', now_str)
    if '{name}' in file_name:
        file_name = file_name.replace('{name}', config.print_file_name)

    file_name = file_name.replace(' ', '_')
    return file_name
