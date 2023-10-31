from typing import List
from types import FunctionType

from ..events.events import Events, SESSION_START, SESSION_END


class Session:
    def __init__(self, events: Events,
                 session_start_callbacks=List[FunctionType],
                 session_end_callbacks=List[FunctionType]) -> None:
        self.events = events
        self.session_start_callbacks = session_start_callbacks
        self.session_end_callbacks = session_end_callbacks

    def start(self):
        self.events.fire_event(SESSION_START)
        self._call_all(self.session_start_callbacks)

    def end(self):
        self._call_all(self.session_end_callbacks)
        self.events.fire_event(SESSION_END)

    def _call_all(self, funcs: List[FunctionType]):
        for func in funcs:
            func()
