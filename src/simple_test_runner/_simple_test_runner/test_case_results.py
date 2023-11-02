from typing import List, final

from .test_case_result import ModuleTestCaseResult


@final
class TestCaseResults:
    """Contain module test case result.

    Args:
        items (List[ModuleTestCaseResult]): Module test case results.
        all_passed (bool):True if all test passed.
    """

    def __init__(self, items: List[ModuleTestCaseResult]):
        self.items = items
        self.all_passed = True
        for item in items:
            if item.failure_count > 0:
                self.all_passed = False
