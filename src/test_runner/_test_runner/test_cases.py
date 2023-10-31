from typing import List

from .test_case import ModuleTestCase



class TestCases:
    """Class which collects all TestCases.

    Attributes:
        items: A list of TestCase.
    """

    def __init__(self, items: List[ModuleTestCase]):
        """Initializes the instance of TestCases class

        Args:
            items: A list of TestCase.
        """
        self.items = items
        self.count = len(items)
