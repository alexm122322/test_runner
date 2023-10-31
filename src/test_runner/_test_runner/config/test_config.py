from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List
from ..logger.formatters import TextFormatter, FileFormatter
from ..logger.loggers import TestsLogger, SessionLogger


DEFAULT_PRINT_PATH = 'print.txt'
DEFAULT_PYTHONPATHS = tuple(['.'])
DEFAULT_TEST_FILES_PATTERN = tuple(['test_.*.py'])
DEFAULT_TEST_FUNCS_PATTERN = tuple(['test_.*'])


@dataclass
class TestsConfig:
    pythonpaths: List[str] = DEFAULT_PYTHONPATHS

    test_files_pattern: List[str] = DEFAULT_TEST_FILES_PATTERN
    test_funcs_pattern: List[str] = DEFAULT_TEST_FUNCS_PATTERN

    enable_print_to_file: bool = True
    print_file_name: str = 'test_report'
    print_file_format: str = '{name}_{datetime}.txt'
    print_file_datetime: datetime = datetime.now()

    text_formatter: TextFormatter = TextFormatter()
    file_formatter: FileFormatter = FileFormatter()
    tests_logger: Optional[TestsLogger] = None
    session_logger: Optional[SessionLogger] = None
