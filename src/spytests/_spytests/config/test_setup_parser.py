import os

from inspect import isfunction
from runpy import run_path
from typing import List, Dict, Tuple
from types import FunctionType

from ..decorators import END_SESSION_ATTRIBUTE_NAME, START_SESSION_ATTRIBUTE_NAME

from .test_config import TestsConfig

TEST_SETUP_FILE = 'setup.py'


class TestSetupParser:
    """Class for parsing TEST_SETUP_FILE.

    Attrs:
        session_start_callbacks (List[FunctionType]): Functions that must run before
         the session starts.
        session_end_callbacks (List[FunctionType]): Functions that must run after
         the session ends.
    """

    def __init__(self, test_dir: str):
        self._test_dir = test_dir

    def parse(self) -> Tuple:
        """Endpoint to TEST_SETUP_FILE parsing.
        Try to find TEST_SETUP_FILE in the _test_dir.
        If TEST_SETUP_FILE is not exist, configure by default.

        Configure by default:
            session_start_callbacks: an empty list.
            session_start_callbacks: an empty list.
            self.test_config: TestsConfig without changes.

        Return:
            Tuple(TestsConfig, List, List): user config, start_callbacks, end_callbacks.
        """
        files = [f for f in os.listdir(self._test_dir) if f == TEST_SETUP_FILE]
        if not files:
            return (TestsConfig(), [], [])

        setup_file = self._test_dir + files[0]
        members = run_path(setup_file)

        session_start_callbacks = self._find_session_start_functions(members)
        session_end_callbacks = self._find_session_end_functions(members)
        test_config = self._find_test_config(members)
        return (test_config, session_start_callbacks, session_end_callbacks)

    def _find_test_config(self, members: Dict[str, any]) -> TestsConfig:
        """Try to find TestsConfig instanse.

        Args:
            members: The members of TEST_SETUP_FILE.

        Returns:
            TestsConfig: TestsConfig instanse from TEST_SETUP_FILE.
             If the instance is not present, return the default TestsConfig.
        """
        for _, member in members.items():
            if isinstance(member, TestsConfig):
                return member

        return TestsConfig()

    def _find_session_start_functions(self, members: Dict[str, any]) -> List[FunctionType]:
        """Search a start session functions in members.

        Args:
            members: Members in which the search for suitable methods
             is carried out.

        Returns:
            List[FunctionType]: A list of sutable functions.
        """
        return list(self._find_all_by_attribute(START_SESSION_ATTRIBUTE_NAME, members))

    def _find_session_end_functions(self, members: Dict[str, any]) -> List[FunctionType]:
        """Search an end session functions in members.

        Args:
            members: Members in which the search for suitable methods
             is carried out.

        Returns:
            List[FunctionType]: A list of sutable functions.
        """
        return list(self._find_all_by_attribute(END_SESSION_ATTRIBUTE_NAME, members))

    def _find_all_by_attribute(self, attr_name: str, members: Dict[str, any]):
        """Function generator of suitable members.
        A suitable member is a function that has an attribute with attr_name.

        Args:
            attr_name: Suitable name of attrubite.
            members: Members in which the search for suitable methods
             is carried out.

        Yields:
            FunctionType: A suitable function.
        """
        for _, member in members.items():
            if not isfunction(member):
                continue
            if hasattr(member, attr_name):
                yield member
