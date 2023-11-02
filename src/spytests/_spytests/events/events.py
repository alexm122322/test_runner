from types import FunctionType, MethodType
from typing import List

SESSION_START = 'session_start'
SESSION_END = 'session_end'
TEST_CASES_COLLECTED = 'test_caseses_collected'
TEST_CASES_FINISHED = 'test_caseses_finished'


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

    def fire_event(self, *args, **kwargs):
        """Trigger all callbacks with event. 
        Checks count of args before trigger.

        Args:
            event: Event that will be transmitted to the callbacks.
        """
        for callback in self._callbacks:
            args_count = len(args) + len(kwargs)
            if callback.__code__.co_varnames and callback.__code__.co_varnames[0] == 'self':
                args_count += 1
                
            if callback.__code__.co_argcount != args_count:
                continue
            
            callback(*args, **kwargs)
        
