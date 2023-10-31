import sys
import traceback

from .test_case import TestCase
from .test_case_result import TestCaseResult, ModuleTestCaseResult
from .test_cases import TestCases
from .test_case_results import TestCaseResults


class TestCaseRunner:
    """Test case runner."""

    def run_test_cases(self, test_cases: TestCases) -> TestCaseResults:
        """Runs all test cases and collect passed and failed results.

        Args:
            test_cases: The test cases which need runs.

        Returns:
            TestCaseResults: The test cases result.
        """
        
        module_results = []
        for module_test_case in test_cases.items:
            passed = []
            unpassed = []

            for test_case in module_test_case.test_cases:
                result = self.run_test_case(test_case)
                if self._passed_result(result):
                    passed.append(result)
                else:
                    unpassed.append(result)

            module_results.append(ModuleTestCaseResult(module_test_case,
                                                       passed, unpassed))
        return TestCaseResults(module_results)

    def run_test_case(self, test_case: TestCase) -> TestCaseResult:
        """Runs a test case. Catch all Exceptions.

        Args:
            test_case: The test case which need run.
            
        Returns:
            TestCaseResult: The result of the test case.
        """
        
        try:
            test_case.func()
            return TestCaseResult(test_case=test_case)
        except AssertionError as e:
            _, _, tb = sys.exc_info()
            stack_summary = traceback.extract_tb(tb)[-1]
            
            return TestCaseResult(test_case=test_case,
                                  assertion_error=e,
                                  stack_summary=stack_summary)
        except Exception as e:
            _, _, tb = sys.exc_info()
            stack_summary = traceback.extract_tb(tb)[-1]
            return TestCaseResult(test_case=test_case,
                                  exception=e,
                                  stack_summary=stack_summary)

    def _passed_result(self, result: TestCaseResult) -> bool:
        """Detect if test case passed or failed

        Args:
            result: The test case result.

        Returns:
            bool: True if test case passed. False if test case failed
        """
        
        if result.test_case.exception:
            return isinstance(result.exception, result.test_case.exception)
        else:
            return not result.exception and not result.assertion_error
