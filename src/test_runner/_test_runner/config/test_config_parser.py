import os

from inspect import isfunction
from runpy import run_path
from typing import List, Dict
from types import FunctionType

from .exceptions import UsageError
from .test_config import TestsConfig

TEST_SETUP_FILE = 'setup.py'

class TestConfigParser:
    def __init__(self, test_dir: str) -> None:
        self.test_dir = test_dir
        self._parse_setup_file()

    def _parse_setup_file(self):
        files = [f for f in os.listdir(self.test_dir) if f == TEST_SETUP_FILE]
        if not files:
            raise UsageError(f"Setup file '{TEST_SETUP_FILE}'' is not exist!")
        setup_file = self.test_dir + files[0]
        members = run_path(setup_file)
        self.session_start_callbacks = self._find_session_start_functions(
            members)
        self.session_end_callbacks = self._find_session_end_functions(members)
        self.test_config = self._find_test_config(members)
        
    def _find_test_config(self, members: Dict[str, any]) -> TestsConfig:
        for _, member in members.items():
            if not isinstance(member, TestsConfig):
                continue
            return member

    def _find_session_start_functions(self, members: Dict[str, any]) -> List[FunctionType]:
        return list(self._find_all_by_attribute('start_session', members))

    def _find_session_end_functions(self, members: Dict[str, any]) -> List[FunctionType]:
        return list(self._find_all_by_attribute('end_session', members))

    def _find_all_by_attribute(self, attr_name: str, members: Dict[str, any],) -> List[FunctionType]:
        for _, member in members.items():
            if not isfunction(member):
                continue
            if hasattr(member, attr_name):
                yield member