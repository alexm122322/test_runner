import os

from test_runner._test_runner.test_case_collector import TestCaseCollector
from test_runner import TestsConfig

test_dir = 'test/'


def _init_test_case_collector() -> TestCaseCollector:
    """Initialize TestCaseCollector by default"""
    
    config = TestsConfig(enable_print_to_file=False)
    return TestCaseCollector(config)


def _create_test_dir():
    """Creates a test dir, test_file.py, and test_file1.py
    inside the test dir. Create test_* and check_* and fetch_*
    functions inside files.
    """

    os.mkdir(test_dir)

    with open(f'{test_dir}test_file.py', "w") as f:
        f.write('''
def test_func1():
    assert 1 == 1
                
def test_func2():
    assert 2 == 2
    
def check_func():
    assert 3 == 3
    
def fetch_func():
    assert 3 == 3''')

    with open(f'{test_dir}test_file1.py', "w") as f:
        f.write('''
from src.test_runner import should_raise_exception, TestsConfig


class CustomException(Exception):
    pass             
 
@should_raise_exception(CustomException)
def test_func1():
    assert 1 == 1
                
def test_func2():
    assert 2 == 2''')


def _remove_test_dir():
    """Removes test_file.py and test_file1.py, and test dir."""

    os.remove(f'{test_dir}test_file.py')
    os.remove(f'{test_dir}test_file1.py')
    os.rmdir(test_dir)
    
def test_collector():
    """Test TestCaseCollector collect all test cases from test dir"""
    
    _create_test_dir()
    collector = _init_test_case_collector()
    result = collector.collect(test_dir)
    _remove_test_dir()
    
    assert result.count == 2
    assert result.items[0].file_path == f'{test_dir}test_file.py'
    assert result.items[1].file_path == f'{test_dir}test_file1.py'
    assert len(result.items[0].test_cases) == 2
    assert len(result.items[1].test_cases) == 2
    assert result.items[0].test_cases[0].exception is None
    assert result.items[1].test_cases[0].exception is not None
    
    
    