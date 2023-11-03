import sys
import traceback
from src.spytests._spytests.logger.init import init_logger
from src.spytests._spytests.test_cases import TestCases
from src.spytests._spytests.test_case import ModuleTestCase, TestCase
from src.spytests._spytests.test_case_results import TestCaseResults
from src.spytests._spytests.test_case_result import TestCaseResult, ModuleTestCaseResult


from src.spytests import TestsLogger, TestsConfig, raise_exception


class SpecificException(Exception):
    pass


if __name__ == "__main__":
    logger = init_logger(TestsConfig(), 'Test Runner')
    logger = TestsLogger(logger)

    def test_func1():
        assert 1 == 1

    def test_func2():
        assert 1 == 2

    def test_func3():
        raise Exception()

    def test_func4():
        raise SpecificException()

    @raise_exception(SpecificException)
    def test_func5():
        raise SpecificException()

    @raise_exception(SpecificException)
    def test_func6():
        assert 1 == 1

    test_cases = TestCases(items=[
        ModuleTestCase('test_dir/test_file1.py', [
            TestCase(test_func1, None, 'test_func1'),
            TestCase(test_func2, None, 'test_func2'),
        ]),
        ModuleTestCase('test_dir/test_file2.py', [
            TestCase(test_func3, None, 'test_func3'),
            TestCase(test_func4, None, 'test_func4'),
        ]),
        ModuleTestCase('test_dir/test_file3.py', [
            TestCase(test_func5, SpecificException, 'test_func5'),
            TestCase(test_func6, SpecificException, 'test_func6'),
        ]),
    ])

    logger.log_test_cases_info(test_cases)

    test_case_results = TestCaseResults(items=[
        ModuleTestCaseResult(ModuleTestCase('test_dir/test_file1.py', [
            TestCase(test_func1, None, 'test_func1'),
            TestCase(test_func2, None, 'test_func2'),
        ]), passed_results=[
            TestCaseResult(TestCase(test_func1, None, 'test_func1')),
        ], failure_results=[
            TestCaseResult(TestCase(test_func2, None, 'test_func2'),
                           assertion_error=AssertionError()),
        ]),
        ModuleTestCaseResult(ModuleTestCase('test_dir/test_file1.py', [
            TestCase(test_func3, None, 'test_func3'),
            TestCase(test_func4, None, 'test_func4'),
        ]), passed_results=[],
            failure_results=[
                TestCaseResult(TestCase(test_func3, None,
                               'test_func3'), Exception()),
                TestCaseResult(TestCase(test_func4, None,
                               'test_func4'), SpecificException()),
        ]),
        ModuleTestCaseResult(ModuleTestCase('test_dir/test_file1.py', [
            TestCase(test_func5, SpecificException, 'test_func5'),
            TestCase(test_func4, None, 'test_func4'),
        ]), passed_results=[
            TestCaseResult(TestCase(test_func6, SpecificException, 'test_func6',), SpecificException()),
        ],
            failure_results=[TestCaseResult(TestCase(test_func5, SpecificException, 'test_func5')),
                             ]),
    ])

    logger.log_results(test_case_results)
