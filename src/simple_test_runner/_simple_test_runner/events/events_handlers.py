from ..logger import SessionLogger, TestsLogger
from .events import Events, SESSION_START, SESSION_END
from .events import TEST_CASES_COLLECTED, TEST_CASES_FINISHED


class SessionLoggerEventHandler:
    """Event handler for Session Logger.

    Attrs:
        logger: Session Logger.
    """

    def __init__(self, logger: SessionLogger, events: Events):
        self.logger = logger
        events.add_callback(self.handle_event)
    
    def handle_event(self, event: str):
        """The function that handles events.  

        Args:
            event: Event.
        """

        if event == SESSION_START:
            self.logger.log_session_start()
        elif event == SESSION_END:
            self.logger.log_session_end()
            

class TestsEventHandler:
    """Event handler for Tests Logger.

    Attrs:
        logger: Tests Logger.
    """

    def __init__(self, logger: TestsLogger, events: Events):
        self.logger = logger
        events.add_callback(self.handle_event)

    def handle_event(self, event: str, info: any):
        """The function that handles events.  

        Args:
            event: Event.
        """
        
        if event == TEST_CASES_COLLECTED:
            self.logger.log_test_cases_info(info)
        elif event == TEST_CASES_FINISHED:
            self.logger.log_results(info)
