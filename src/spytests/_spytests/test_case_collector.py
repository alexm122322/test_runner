import os

from inspect import isfunction
import re
from runpy import run_path
from typing import List, Optional
from types import FunctionType

from .decorators import EXCEPTION_ATTRIBUTE_NAME
from .test_cases import TestCases
from .test_case import TestCase, ModuleTestCase
from .config.test_config import TestsConfig


class TestCaseCollector:
    """Collects all test cases in a directory or file."""

    def __init__(self, config: TestsConfig, path: str):
        self._path = path
        self._test_files_patterns = config.test_files_pattern
        self._test_funcs_pattern = config.test_funcs_pattern

    def collect(self) -> TestCases:
        """Collects all test cases in a destination.

        Returns:
            TestCases: All test cases in a destination.
        """
        return TestCases(self._collect(self._path))

    def _collect(self, path: str) -> List[ModuleTestCase]:
        """Collects all module test cases in a destination.

        Args:
            path: A path to the destination. It should be a directory.

        Returns:
            List[ModuleTestCase]: A list of module test cases.
        """
        test_cases = []
        if os.path.isdir(path):
            for file in os.listdir(path):
                module_test_case = self._collect(f'{path}{file}')
                if module_test_case:
                    test_cases.extend(module_test_case)
        elif os.path.isfile(path):
            module_test_case = self._collect_test_cases_in_file(path)
            if module_test_case is not None:
                test_cases.append(module_test_case)
        test_cases.reverse()
        return test_cases

    def _collect_test_cases_in_file(self, path: str) -> Optional[ModuleTestCase]:
        """Collects all test cases in a file.

        Args:
            path: A path to the file.

        Returns:
            List[TestCase]: All test cases at a file.
        """
        if not self._is_test_file(path):
            return None

        members = run_path(path).items()
        members = [e for e in members if self._is_test_case(e[0], e[1])]

        test_cases = [
            TestCase(e[1], self._retrieve_exception(e[1]), e[0]) for e in members]

        return ModuleTestCase(path, test_cases) if test_cases else None

    def _retrieve_exception(self, func: FunctionType) -> Optional[Exception]:
        """Retrieve expected an exception from a function.

        Args:
            func: The function.

        Returns:
            Optional[Exception]: Exception if an exception is expected.
        """
        return func._exception if hasattr(func, EXCEPTION_ATTRIBUTE_NAME) else None

    def _is_test_file(self, path: str) -> bool:
        """Check if path is a test file.

        Args:
            path: Path to the file.

        Returns:
            bool: True if file match with the patterns.
        """
        filename = path.split('/').pop()

        return self._match_pattens(filename, self._test_files_patterns)

    def _is_test_case(self, name: str, member: any) -> bool:
        """Check if a member is the test case.

        Args:
            name: A name of a function.
            member: Chcking member.

        Returns:
            bool: True if the member is a function and 
                is a match to the patterns.
        """
        return isfunction(member) and self._match_pattens(name, self._test_funcs_pattern)

    def _match_pattens(self, name: str, patterns: List[str]) -> bool:
        """Check if name match with patterns.

        Args:
            name: Checking name.
            patterns: Matching patterns.

        Returns:
            bool: True if the name matches with one of the patterns.
        """
        for pattern in patterns:
            pattern = re.compile(pattern)
            match = pattern.match(name)
            if match and len(match.string) == len(name):
                return True
        return False
