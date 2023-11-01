from typing import List, final

from .test_case import ModuleTestCase


@final
class TestCases:
    """Data class which collects all TestCases.

    Attributes:
        items: A list of TestCase.
        count: Count of test cases.
    """

    def __init__(self, items: List[ModuleTestCase]):
        """Initializes the instance of TestCases class

        Args:
            items: A list of TestCase.
        """
        self.items = items
        self.count = len(items)
