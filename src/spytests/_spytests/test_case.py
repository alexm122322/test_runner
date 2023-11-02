from dataclasses import dataclass
from types import FunctionType
from typing import Optional, List


@dataclass
class TestCase:
    """Data class which collects all information about test function.

    Attributes:
        func: A test function.
        exception: An optional exception. It contains an exception 
          that the test function must raise.
        file_path: The path to the file where the function exists.
        method_name: A name of the function.
    """

    func: FunctionType
    exception: Optional[Exception]
    method_name: str


@dataclass
class ModuleTestCase:
    """Data class which collects all information about test functions in a module.

    Attributes:
        file_path: A name of the function.
        test_cases: The test cases of a module.
    """

    file_path: str
    test_cases: List[TestCase]
