from test_runner._test_runner.test_case_runner import TestCaseRunner
from test_runner._test_runner.test_case import TestCase, ModuleTestCase
from test_runner._test_runner.test_cases import TestCases
from test_runner import should_raise_exception


runner = TestCaseRunner()


def test_run_passed_test_case():
    """Test the test case which should pass."""
    
    def test_func():
        assert 1 == 1
        
    test_case = TestCase(test_func, None, 'test_func')
    result = runner.run_test_case(test_case)
    assert not result.assertion_error and not result.exception
    assert test_case == result.test_case
    assert not result.stack_summary


def test_run_assertion_test_case():
    """Test the test case which should raise AssertionError."""
    
    def test_func():
        assert 1 == 2
        
    test_case = TestCase(test_func, None, 'test_func')
    result = runner.run_test_case(test_case)
    assert not result.exception and result.assertion_error
    assert isinstance(result.assertion_error, AssertionError)
    assert test_case == result.test_case
    assert result.stack_summary


def test_run_exception_test_case():
    """Test the test case which should raise Exception."""
    
    def test_func():
        raise Exception
    
    test_case = TestCase(test_func, None, 'test_func')
    result = runner.run_test_case(test_case)
    assert result.exception and not result.assertion_error
    assert isinstance(result.exception, Exception)
    assert test_case == result.test_case
    assert result.stack_summary


class SpecificException(Exception):
    """The specific implementation of Exception."""
    pass


def test_run_specific_exception_test_case():
    """Test the test case which should raise SpecificException."""
    
    def test_func():
        raise SpecificException
    
    test_case = TestCase(test_func, None, 'test_func')
    result = runner.run_test_case(test_case)
    assert result.exception and not result.assertion_error
    assert isinstance(result.exception, SpecificException)
    assert test_case == result.test_case
    assert result.stack_summary


def test_run_test_cases():
    """Test the test cases.
    In this test presented all possible test cases.
    TestCaseRunner.run_test_cases should return TestCaseResults
    which should contain all passed and failed test case results.
    """

    def test_func1():
        assert 1 == 1

    def test_func2():
        assert 1 == 2

    def test_func3():
        raise Exception

    def test_func4():
        raise SpecificException

    @should_raise_exception(SpecificException)
    def test_func5():
        raise SpecificException

    @should_raise_exception(SpecificException)
    def test_func6():
        assert 1 == 1

    test_cases = TestCases(items=[
        ModuleTestCase('test_dir/test_file1.py', [
            TestCase(test_func1, None, 'test_func1'),
            TestCase(test_func2, None, 'test_func2'),]),
        ModuleTestCase('test_dir/test_file2.py', [
            TestCase(test_func3, None, 'test_func3'),
            TestCase(test_func4, None, 'test_func4'),]),
        ModuleTestCase('test_dir/test_file3.py', [
            TestCase(test_func5, SpecificException, 'test_func5'),
            TestCase(test_func6, SpecificException, 'test_func6')]),
    ])

    result = runner.run_test_cases(test_cases)
    assert len(result.items) == 3
    
    assert result.items[0].test_count == 2
    assert result.items[0].module_test_case.file_path == 'test_dir/test_file1.py'
    assert result.items[0].failure_count == 1
    assert result.items[0].passed_count == 1
    
    assert result.items[1].test_count == 2
    assert result.items[1].module_test_case.file_path == 'test_dir/test_file2.py'
    assert result.items[1].failure_count == 2
    assert result.items[1].passed_count == 0
    
    assert result.items[2].test_count == 2
    assert result.items[2].module_test_case.file_path == 'test_dir/test_file3.py'
    assert result.items[2].failure_count == 1
    assert result.items[2].passed_count == 1
