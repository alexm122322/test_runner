import sys
from typing import Optional
from ..events.events import Events
from ..logger.loggers import SessionLogger, TestsLogger
from ..logger.init import init_logger
from ..events.events_handlers import SessionLoggerEventHandler
from .session import Session
from .test_setup_parser import TestSetupParser
from .test_config import TestsConfig


class Config:
    def __init__(self, dir_path: Optional[str], test_config: Optional[TestsConfig]):
        self.dir_path = dir_path
        self.events = Events()
        self.config_test_parser = TestSetupParser(dir_path)
        if not test_config:
            self.test_config = self.config_test_parser.test_config
        else:
            self.test_config = test_config
            
        self.session = Session(self.events, self.config_test_parser.session_start_callbacks,
                               self.config_test_parser.session_end_callbacks)

        logger = init_logger(self.test_config, 'Test Runner')
        self.register_session_logger(
            self.test_config.session_logger or SessionLogger(logger))
        self.register_test_results_logger(
            self.test_config.tests_logger or TestsLogger(logger))
        self.logger_event_handler = SessionLoggerEventHandler(
            self.session_logger, self.events)
        
        if self.test_config.pythonpaths:
            for path in self.test_config.pythonpaths:
                sys.path.insert(0, str(path))

    def register_test_results_logger(self, logger: TestsLogger):
        self.test_results_logger = logger

    def register_session_logger(self, logger: SessionLogger):
        self.session_logger = logger

    @property
    def get_session(self) -> Session:
        return self.session
