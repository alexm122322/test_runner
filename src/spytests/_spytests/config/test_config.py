from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from ..logger import TextFormatter, FileFormatter, TestsLogger, SessionLogger


DEFAULT_PRINT_PATH = 'print.txt'
DEFAULT_PYTHONPATHS = tuple(['.'])
DEFAULT_TEST_FILES_PATTERN = tuple(['test_.*.py'])
DEFAULT_TEST_FUNCS_PATTERN = tuple(['test_.*'])


@dataclass
class TestsConfig:
    """User spytests configuration.

    Attrs:
        pythonpaths: Python pathes.
        test_files_pattern: Pattern for finding test files in directory.
        test_funcs_pattern: Pattern for finding test functions in directory.
        enable_print_to_file: Enable print report to file.
        print_file_name: Print file name.
        print_file_format: Print file format. {name} and {datetime} are necessary.
        text_formatter: TextFormatter object for castomization logger format.
        text_formatter: FileFormatter object for castomization file logger format.
        tests_logger: TestsLogger object for printing castomization.
        session_logger: SessionLogger object for printing castomization.
    """

    pythonpaths: List[str] = DEFAULT_PYTHONPATHS

    test_files_pattern: List[str] = DEFAULT_TEST_FILES_PATTERN
    test_funcs_pattern: List[str] = DEFAULT_TEST_FUNCS_PATTERN

    enable_print_to_file: bool = False
    print_file_name: str = 'test_report'
    print_file_format: str = '{name}_{datetime}.txt'
    print_file_datetime: datetime = datetime.now()

    text_formatter: TextFormatter = TextFormatter()
    file_formatter: FileFormatter = FileFormatter()
    tests_logger: Optional[TestsLogger] = None
    session_logger: Optional[SessionLogger] = None
