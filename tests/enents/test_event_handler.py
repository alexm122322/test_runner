from test_runner._test_runner.events.events_handlers import SessionLoggerEventHandler, TestsEventHandler
from test_runner._test_runner.events.events import SESSION_START, SESSION_END, TEST_CASES_COLLECTED, TEST_CASES_FINISHED
from test_runner._test_runner.logger.loggers import SessionLogger, TestsLogger
from test_runner._test_runner.logger.init import init_logger
from test_runner._test_runner.events.events import Events
from test_runner._test_runner.test_cases import TestCases
from test_runner._test_runner.test_case_results import TestCaseResults

from test_runner import TestsConfig


class CustomSessionLogger(SessionLogger):
    pass


def test_logger_event_handler_session_start(mocker):
    """Test handle SESSION_START event."""

    mock = mocker.patch(
        f'{__name__}.{CustomSessionLogger.__name__}.log_session_start')

    logger = init_logger(TestsConfig(), 'test')
    logger = CustomSessionLogger(logger)
    events = Events()
    SessionLoggerEventHandler(logger, events)
    events.fire_event(SESSION_START)
    mock.assert_called_once()


def test_logger_event_handler_session_end(mocker):
    """Test handle SESSION_END event."""

    mock = mocker.patch(
        f'{__name__}.{CustomSessionLogger.__name__}.log_session_end')

    logger = init_logger(TestsConfig(), 'test')
    logger = CustomSessionLogger(logger)
    events = Events()
    SessionLoggerEventHandler(logger, events)
    events.fire_event(SESSION_END)
    mock.assert_called_once()


class CustomTestsLogger(TestsLogger):
    pass


def test_tests_event_handler_collected(mocker):
    """Test handle TEST_CASES_COLLECTED event."""

    mock = mocker.patch(
        f'{__name__}.{CustomTestsLogger.__name__}.log_test_cases_info')

    logger = init_logger(TestsConfig(), 'test')
    logger = CustomTestsLogger(logger)
    events = Events()
    TestsEventHandler(logger, events)
    events.fire_event(TEST_CASES_COLLECTED, TestCases([]))
    mock.assert_called_once()


def test_tests_event_handler_finished(mocker):
    """Test handle TEST_CASES_FINISHED event."""

    mock = mocker.patch(
        f'{__name__}.{CustomTestsLogger.__name__}.log_results')

    logger = init_logger(TestsConfig(), 'test')
    logger = CustomTestsLogger(logger)
    events = Events()
    TestsEventHandler(logger, events)
    events.fire_event(TEST_CASES_FINISHED, TestCaseResults([]))
    mock.assert_called_once()
