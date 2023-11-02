from src.simple_test_runner import should_raise_exception, main


class CustomException(Exception):
    pass


@should_raise_exception(exception=CustomException)
def test_method():
    raise CustomException('some error')
    

def test_method2():
    assert 2 == 1
    print('test_method')


