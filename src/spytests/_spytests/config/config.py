import sys

from typing import Optional

from ..events import Events
from ..events import SessionLoggerEventHandler, TestsEventHandler

from ..logger import SessionLogger, TestsLogger
from ..logger import init_logger

from ..session import Session

from .test_setup_parser import TestSetupParser
from .test_config import TestsConfig


class Config:
    """Configuration of the test_runner.

    Args:
        test_config: user test configuration.
        session: test_runner session.
    """

    def __init__(self, dir_path: Optional[str],
                 test_config: Optional[TestsConfig] = None):
        self._setup = TestSetupParser(dir_path).parse()
        self._events = Events()

        self._init_test_config(test_config)
        self._init_loggers()

        self.session = Session(self._events, self.test_config,
                               dir_path, self._setup[1], self._setup[2])

        self._pythonpaths()

    def _pythonpaths(self):
        """Setup python paths"""

        if self.test_config.pythonpaths:
            for path in self.test_config.pythonpaths:
                sys.path.insert(0, str(path))

    def _init_loggers(self):
        """Initializing loggers and event handlers."""

        logger = init_logger(self.test_config, 'Test Runner')
        self.session_logger = self.test_config.session_logger or SessionLogger(
            logger)
        self.test_results_logger = self.test_config.tests_logger or TestsLogger(
            logger)
        SessionLoggerEventHandler(self.session_logger, self._events)
        TestsEventHandler(self.test_results_logger, self._events)

    def _init_test_config(self, test_config: Optional[TestsConfig]):
        """Initializing user config."""

        if test_config is None:
            self.test_config = self._setup[0]
        else:
            self.test_config = test_config
