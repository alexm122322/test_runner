from typing import List

from .logger.formatters import ColorArgs

from .test_case_result import ModuleTestCaseResult


class TestCaseResults:
    def __init__(self, items: List[ModuleTestCaseResult]) -> None:
        self.items = items
        
