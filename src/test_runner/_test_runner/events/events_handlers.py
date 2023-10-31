from ..logger.loggers import SessionLogger
from .events import Events, SESSION_START, SESSION_END


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
