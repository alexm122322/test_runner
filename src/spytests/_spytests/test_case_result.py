from dataclasses import dataclass
from traceback import StackSummary
from typing import List, Optional, final

from .test_case import TestCase, ModuleTestCase


@dataclass
class TestCaseResult:
    """Data class which collects all information about test function result.

    Args:
        test_case: TestCase object.
        exception: Caught exception while running test case.
        assertion_error: Caught Assert Error while running test case.
        stack_summary: Stack summary of exception or Assert Error.
    """

    test_case: TestCase
    exception: Optional[Exception] = None
    assertion_error: Optional[AssertionError] = None
    stack_summary: Optional[StackSummary] = None


@final
class ModuleTestCaseResult:
    """Data class which collects all information about 
    test function results in the module.

    Args:
        module_test_case: ModuleTestCase object.
        passed_results: List of passed test results.
        failure_results: List of failed test results.
        passed_count: Count of passed test results.
        failure_count: Count of failured test results.
        test_count: Count of test results.
    """

    def __init__(self, module_test_case: ModuleTestCase,
                 passed_results: List[TestCaseResult],
                 failure_results: List[TestCaseResult]):
        self.module_test_case = module_test_case
        self.passed_results = passed_results
        self.failure_results = failure_results

        self.passed_count = len(self.passed_results)
        self.failure_count = len(self.failure_results)
        self.test_count = self.passed_count + self.failure_count
