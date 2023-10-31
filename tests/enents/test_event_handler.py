from test_runner._test_runner.events.events_handlers import SessionLoggerEventHandler
from test_runner._test_runner.events.events import SESSION_START, SESSION_END
from test_runner._test_runner.logger.loggers import SessionLogger
from test_runner._test_runner.logger.init import init_logger
from test_runner._test_runner.events.events import Events

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
