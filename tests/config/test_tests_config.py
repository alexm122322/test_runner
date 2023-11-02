import os

from datetime import datetime
from logging import Logger
from spytests._spytests.config.test_config import TestsConfig
from spytests._spytests.config import Config

from spytests._spytests.logger.loggers import TestsLogger, SessionLogger
from spytests._spytests.logger.init import init_logger
from spytests._spytests.logger.formatters import TextFormatter, FileFormatter

from spytests._spytests.test_cases import TestCases
from spytests._spytests.test_case_collector import TestCaseCollector

from spytests._spytests.logger.init import _create_file_name

from unittest.mock import patch, mock_open

from tests.consts import TEST_DIR


def init_session_logger(config: TestsConfig) -> SessionLogger:
    """Creating SessionLogger

    Args:
        config: Testing configuration.

    Returns:
        SessionLogger: Configured logger for session.
    """

    logger = init_logger(config, "Test Runner")
    return SessionLogger(logger)


def test_should_print_to_file():
    """Test TestConfig.enable_print_to_file option True.
    Should print to file.
    """

    test_config = TestsConfig(enable_print_to_file=True)
    print_file = _create_file_name(test_config)

    logger = init_session_logger(test_config)
    logger.log_session_start()

    assert os.path.exists(print_file)

    with open(print_file, "r") as f:
        file_data = f.read()
        assert file_data != ""


def test_not_should_print_to_file():
    """Test TestConfig.enable_print_to_file option False.
    Shouldn't print to file.
    """

    test_config = TestsConfig(enable_print_to_file=False)
    print_file = _create_file_name(test_config)

    with open(print_file, "w") as f:
        file_data = f.write('')

    logger = init_session_logger(test_config)
    logger.log_session_start()

    assert os.path.exists(print_file)

    with open(print_file, "r") as f:
        file_data = f.read()
        assert file_data == ""


def test_custom_file_path():
    """Test TestConfig.print_file_path option.
    Should create custom file and print there.
    """
    
    custom_file = 'custom'
    custom_date = datetime.now()
    test_config = TestsConfig(print_file_format="{datetime}_{name}.txt",
                              print_file_name=custom_file,
                              print_file_datetime=custom_date)
    
    print_file = _create_file_name(test_config)
    time_str = custom_date.strftime("%d.%m.%Y_%H:%M:%S")
    expected = f'{time_str}_{custom_file}.txt'
    assert print_file == expected


class CustomTextFormatter(TextFormatter):
    """Simple FileFormatter realization for test."""

    def format(self, record):
        return super().format(record)


@patch(f"{__name__}.{CustomTextFormatter.__name__}.format", new_callable=mock_open, read_data="data")
def test_text_formatter_castomization(mock_open_obj):
    """Test custom TestsConfig.text_formatter.
    Should call TextFormatterChild.format().
    """

    test_config = TestsConfig(text_formatter=CustomTextFormatter())

    logger = init_session_logger(test_config)
    logger.log_session_start()
    mock_open_obj.assert_called()


class CustomFileFormatter(FileFormatter):
    """Simple FileFormatter realization for test."""

    def format(self, record):
        return super().format(record)


@patch(f"{__name__}.{CustomFileFormatter.__name__}.format", new_callable=mock_open, read_data="data")
def test_file_formatter_customization(mock_open_obj):
    """Test custom TestsConfig.file_formatter.
    Should call CustomFileFormatter.format().
    """

    test_config = TestsConfig(enable_print_to_file=True, 
                              file_formatter=CustomFileFormatter())

    logger = init_session_logger(test_config)
    logger.log_session_start()
    mock_open_obj.assert_called()


class CustomTestsLogger(TestsLogger):
    """Simple TestsLogger realization for test."""
    pass


@patch(f"{__name__}.{CustomTestsLogger.__name__}.log_test_cases_info", new_callable=mock_open, read_data="data")
def test_tests_logger_castomization(mock_open_obj):
    """Test custom TestsConfig.tests_logger.
    Should call CustomTestsLogger.log_test_cases_info().
    """

    test_config = TestsConfig(tests_logger=CustomTestsLogger(Logger('')))

    config = Config('tests/', test_config)
    config.test_results_logger.log_test_cases_info(TestCases([]))
    mock_open_obj.assert_called()


class CustomSessionLogger(SessionLogger):
    """Simple SessionLogger realization for test."""
    pass


@patch(f"{__name__}.{CustomSessionLogger.__name__}.log_session_start", new_callable=mock_open, read_data="data")
def test_session_logger_customization(mock_open_obj):
    """Test custom TestsConfig.session_logger.
    Should call CustomSessionLogger.log_session_start().
    """
    
    session_logger = CustomSessionLogger(Logger(''))
    test_config = TestsConfig(session_logger=session_logger)

    config = Config('tests/', test_config)
    assert session_logger == config.session_logger
    config.session_logger.log_session_start()
    mock_open_obj.assert_called()




def _create_test_dir():
    """Creates a test dir, test_file.py, and check_file.py
    inside the test dir. Create test_* and check_* and fetch_*
    functions inside files.
    """

    with open(f'{TEST_DIR}test_file.py', "w") as f:
        f.write('''
def test_func1():
    assert 1 == 1
                
def test_func2():
    assert 2 == 2
    
def check_func():
    assert 3 == 3
    
def fetch_func():
    assert 3 == 3''')

    with open(f'{TEST_DIR}check_file.py', "w") as f:
        f.write('''
def test_func1():
    assert 1 == 1
                
def test_func2():
    assert 2 == 2''')


def _remove_test_dir():
    """Removes test_file.py and check_file.py, and test dir.
    """

    os.remove(f'{TEST_DIR}test_file.py')
    os.remove(f'{TEST_DIR}check_file.py')


def test_default_test_files_funcs_pattern():
    """Test TestsConfig.test_files_pattern customization.
    Should find all default files and default functions inside.
    """

    _create_test_dir()
    test_config = TestsConfig(pythonpaths=['.', 'tests'])
    collector = TestCaseCollector(test_config, TEST_DIR)
    result = collector.collect()
    _remove_test_dir()

    assert result.count == 1
    assert result.items[0].file_path == 'test/test_file.py'
    assert len(result.items[0].test_cases) == 2


def test_customized_test_files_pattern():
    """Test TestsConfig.test_files_pattern customization.
    Should find all 'check_.*.py' files and default functions inside.
    """

    _create_test_dir()
    test_config = TestsConfig(
        pythonpaths=['.', 'tests'], test_files_pattern=['check_.*.py'])
    collector = TestCaseCollector(test_config, TEST_DIR)
    result = collector.collect()
    _remove_test_dir()

    assert result.count == 1
    assert result.items[0].file_path == 'test/check_file.py'
    assert len(result.items[0].test_cases) == 2


def test_customized_test_funcs_pattern():
    """Test TestsConfig.test_funcs_pattern customization.
    Should find all 'test_.*', 'check_.*' functions.
    """

    _create_test_dir()
    test_config = TestsConfig(pythonpaths=['.', 'tests'], test_funcs_pattern=[
                              'test_.*', 'check_.*'])
    collector = TestCaseCollector(test_config, TEST_DIR)
    result = collector.collect()
    _remove_test_dir()

    assert result.count == 1
    assert result.items[0].file_path == 'test/test_file.py'
    assert len(result.items[0].test_cases) == 3
