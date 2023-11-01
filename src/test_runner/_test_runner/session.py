from typing import List
from types import FunctionType

from .events.events import SESSION_START, SESSION_END
from .events.events import TEST_CASES_COLLECTED, TEST_CASES_FINISHED

from .main import run_tests

from .exit_code import ExitCode
from .test_case_results import TestCaseResults
from .test_cases import TestCases
from .events.events import Events
from .config.test_config import TestsConfig


class Session:
    """Session of test runner.

    Attrs:
        events: The object that triggers events.
        session_start_callbacks: List of start callbacks.
        session_end_callbacks: List of end callbacks.
    """

    def __init__(self,
                 events: Events,
                 config: TestsConfig,
                 dir_path: str,
                 session_start_callbacks: List[FunctionType] = [],
                 session_end_callbacks: List[FunctionType] = []):
        self._events = events
        self._config = config
        self._dir_path = dir_path
        self._session_start_callbacks = session_start_callbacks
        self._session_end_callbacks = session_end_callbacks

    def start(self) -> ExitCode:
        """Starts session."""

        self._start()
        exit_code = run_tests(self._config,
                              self._dir_path,
                              self._collected,
                              self._finished)
        self._end()
        return exit_code

    def _collected(self, test_cases: TestCases):
        self._events.fire_event(TEST_CASES_COLLECTED, test_cases)

    def _finished(self, results: TestCaseResults):
        self._events.fire_event(TEST_CASES_FINISHED, results)

    def _start(self):
        """Call all start callbacks. 
        Fire SESSION_START event. 
        """

        self._events.fire_event(SESSION_START)
        self._call_all(self._session_start_callbacks)

    def _end(self):
        """Ends session. Call all end callbacks. 
        Fire SESSION_END event. 
        """

        self._call_all(self._session_end_callbacks)
        self._events.fire_event(SESSION_END)

    def _call_all(self, funcs: List[FunctionType]):
        """Util function which helps call all functions.

        Args:
            funcs: Functions which will be called.
        """

        for func in funcs:
            func()
