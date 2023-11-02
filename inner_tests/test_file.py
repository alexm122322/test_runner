import time
from src.simple_test_runner import should_raise_exception, TestsConfig


class CustomException(Exception):
    pass


@should_raise_exception(exception=CustomException)
def test_method():
    assert 2 == 1
    print('test_method')
    

def test_method2():
    time.sleep(2)  # import time
    raise CustomException('some error')
    print('test_method')


