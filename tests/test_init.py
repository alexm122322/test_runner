import os

from spytests._spytests import main
from spytests._spytests.exit_code import ExitCode
from spytests._spytests.config import TEST_SETUP_FILE

from tests.consts import TEST_DIR

start_session_name = 'custom_start_session'
end_session_name = 'custom_end_session'
config_name = 'test_config'


def _create_test_dir(creat_failse: bool = False):
    os.rmdir(TEST_DIR)
    os.mkdir(TEST_DIR)

    with open(f'{TEST_DIR}test_file.py', "w") as f:
        f.write('''
def test_func1():
    assert 1 == 1
                
def test_func2():
    assert 2 == 2
    
def check_func():
    assert 3 == 3
    
def fetch_func():
    assert 3 == 3''')
    print('f =', f)
    if creat_failse:
        with open(f'{TEST_DIR}test_file1.py', "w") as f:
            f.write('''
from src.spytests import raise_exception, TestsConfig


class CustomError(Exception):
    pass             
 
@raise_exception(CustomError)
def test_func1():
    assert 1 == 1
                
def test_func2():
    assert 2 == 2''')

    with open(f'{TEST_DIR}{TEST_SETUP_FILE}', "w") as f:
        f.write(f'''
from spytests import TestsConfig, start_session, end_session

@start_session
def {start_session_name}():
    pass

@end_session
def {end_session_name}():
    pass
    
{config_name} = TestsConfig()
''')


def _remove_test_dir(f: bool = False):
    os.remove(f'{TEST_DIR}test_file.py')
    os.remove(f'{TEST_DIR}{TEST_SETUP_FILE}')

    if f:
        os.remove(f'{TEST_DIR}test_file1.py')


def test_start_ok():
    """Test package return OK"""
    _create_test_dir()
    exit_code = main(TEST_DIR)
    _remove_test_dir()
    assert exit_code == ExitCode.OK


def test_start_tests_failed():
    """Test package return TESTS_FAILED"""
    _create_test_dir(True)
    exit_code = main(TEST_DIR)
    _remove_test_dir()
    assert exit_code == ExitCode.TESTS_FAILED


def test_start_usage_error():
    """Test package return USAGE_ERROR"""
    exit_code = main('unknown_path/')
    assert exit_code == ExitCode.USAGE_ERROR
