import sys

from typing import Optional

from ..events.events import Events
from ..events.events_handlers import SessionLoggerEventHandler, TestsEventHandler

from ..logger.loggers import SessionLogger, TestsLogger
from ..logger.init import init_logger

from ..session import Session

from .test_setup_parser import TestSetupParser
from .test_config import TestsConfig


class Config:
    def __init__(self, dir_path: Optional[str], test_config: Optional[TestsConfig]):
        self.dir_path = dir_path
        self.events = Events()
        self._init_test_config(test_config)
        self._init_loggers()
        self.session = Session(self.events,
                               self.test_config,
                               self.dir_path,
                               self.config_test_parser.session_start_callbacks,
                               self.config_test_parser.session_end_callbacks)
        self._pythonpaths()

    def _pythonpaths(self):
        if self.test_config.pythonpaths:
            for path in self.test_config.pythonpaths:
                sys.path.insert(0, str(path))

    def _init_loggers(self):
        logger = init_logger(self.test_config, 'Test Runner')
        self.session_logger = self.test_config.session_logger or SessionLogger(
            logger)
        self.test_results_logger = self.test_config.tests_logger or TestsLogger(
            logger)
        self.logger_event_handler = SessionLoggerEventHandler(
            self.session_logger, self.events)
        self.tests_event_handler = TestsEventHandler(
            self.test_results_logger, self.events)

    def _init_test_config(self, test_config: Optional[TestsConfig]):
        self.config_test_parser = TestSetupParser(self.dir_path)
        if test_config is None:
            self.test_config = self.config_test_parser.test_config
        else:
            self.test_config = test_config
