from typing import List
from types import FunctionType

from ..events.events import Events, SESSION_START, SESSION_END


class Session:
    """Session of test runner.
    
    Attrs:
        events: The object that triggers events.
        session_start_callbacks: List of start callbacks.
        session_end_callbacks: List of end callbacks.
    """
    
    def __init__(self, events: Events,
                 session_start_callbacks: List[FunctionType] = [],
                 session_end_callbacks: List[FunctionType] = []):
        self.events = events
        self.session_start_callbacks = session_start_callbacks
        self.session_end_callbacks = session_end_callbacks

    def start(self):
        """Starts session. Call all start callbacks. 
        Fire SESSION_START event. 
        """
        
        self.events.fire_event(SESSION_START)
        self._call_all(self.session_start_callbacks)

    def end(self):
        """Ends session. Call all end callbacks. 
        Fire SESSION_END event. 
        """
        
        self._call_all(self.session_end_callbacks)
        self.events.fire_event(SESSION_END)

    def _call_all(self, funcs: List[FunctionType]):
        """Util function which helps call all functions.

        Args:
            funcs: Functions which will be called.
        """
        
        for func in funcs:
            func()
