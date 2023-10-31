from types import FunctionType, MethodType
from typing import List

SESSION_START = 'session_start'
SESSION_END = 'session_end'


class Events:
    """Events implementation"""

    def __init__(self):
        self._callbacks: List[FunctionType] = []

    def add_callback(self, func: FunctionType):
        """Add callback if it is a function or method.

        Args:
            func: The function which should add to _callbacks.
        """

        if (isinstance(func, (FunctionType, MethodType))):
            self._callbacks.append(func)

    def remove_callback(self, func: FunctionType):
        """Remove callback if it is a function or method.

        Args:
            func: The function which should remove from _callbacks.
        """

        if (isinstance(func, (FunctionType, MethodType))):
            self._callbacks.remove(func)

    def fire_event(self, event: str):
        """Trigger all callbacks with event.

        Args:
            event: Event that will be transmitted to the callbacks.
        """

        for callback in self._callbacks:
            callback(event)
