from types import FunctionType, MethodType
from typing import List

SESSION_START = 'session_start'
SESSION_END = 'session_end'


class Events:
    def __init__(self):
        self._callbacks: List[FunctionType] = []

    def add_callback(self, func: FunctionType):
        if (isinstance(func, (FunctionType, MethodType))):
            self._callbacks.append(func)

    def remove_callback(self, func: FunctionType):
        if (isinstance(func, (FunctionType, MethodType))):
            self._callbacks.remove(func)

    def fire_event(self, event: str):
        for callback in self._callbacks:
            callback(event)
