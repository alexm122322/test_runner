from dataclasses import dataclass
from typing import List

from .test_case import ModuleTestCase


@dataclass
class TestCases:
    """Data class which collects all TestCases.

    Attributes:
        items: A list of TestCase.
        count: Count of test cases.
    """
    items: List[ModuleTestCase]

    @property
    def count(self):
        return len(self.items)
