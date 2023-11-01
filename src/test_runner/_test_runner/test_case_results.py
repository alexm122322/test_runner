from typing import List

from .logger.formatters import ColorArgs

from .test_case_result import ModuleTestCaseResult


class TestCaseResults:
    """Contain module test case result.
    
    Args:
        items (List[ModuleTestCaseResult]): module test case results.
        all_passed (bool): Flag that show us all test passed.
    """
    
    def __init__(self, items: List[ModuleTestCaseResult]):
        self.items = items
        self.all_passed = True
        for item in items:
            if item.failure_count > 0:
                 self.all_passed = False
        
