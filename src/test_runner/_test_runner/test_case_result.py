from dataclasses import dataclass
from traceback import StackSummary
from typing import List, Optional, final
from .test_case import TestCase, ModuleTestCase


@dataclass
class TestCaseResult:
    test_case: TestCase
    exception: Optional[Exception] = None
    assertion_error: Optional[AssertionError] = None
    stack_summary: Optional[StackSummary] = None


@final
class ModuleTestCaseResult:
    def __init__(self, module_test_case: ModuleTestCase,
                 passed_results: List[TestCaseResult],
                 failure_results: List[TestCaseResult]):
        self.module_test_case = module_test_case
        self.passed_results = passed_results
        self.failure_results = failure_results

        self.passed_count = len(self.passed_results)
        self.failure_count = len(self.failure_results)
        self.test_count = self.passed_count + self.failure_count
