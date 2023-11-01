from test_runner import should_raise_exception, start_session, end_session
from test_runner._test_runner.decorators import END_SESSION_ATTRIBUTE_NAME, START_SESSION_ATTRIBUTE_NAME, EXCEPTION_ATTRIBUTE_NAME

def test_should_raise_exception():
    """Test should_raise_exception decorator.
    The decorator should add EXCEPTION_ATTRIBUTE_NAME attribute.
    The _exception attribute shouldn't exist by default.
    """
    
    def test_func():
        assert 1 == 1
    
    assert not hasattr(test_func, EXCEPTION_ATTRIBUTE_NAME)
    
    @should_raise_exception(Exception)
    def test_func():
        assert 1 == 1
    
    assert hasattr(test_func, EXCEPTION_ATTRIBUTE_NAME)
    

def test_start_session():
    """Test start_session decorator.
    The decorator should add START_SESSION_ATTRIBUTE_NAME attribute.
    The START_SESSION_ATTRIBUTE_NAME attribute shouldn't exist by default.
    """
    def test_func():
        assert 1 == 1
    
    assert not hasattr(test_func, START_SESSION_ATTRIBUTE_NAME)
    
    @start_session
    def test_func():
        pass
    
    assert hasattr(test_func, START_SESSION_ATTRIBUTE_NAME)
    
def test_end_session():
    """Test end_session decorator.
    The decorator should add END_SESSION_ATTRIBUTE_NAME attribute.
    The END_SESSION_ATTRIBUTE_NAME attribute shouldn't exist by default.
    """
    def test_func():
        assert 1 == 1
    
    assert not hasattr(test_func, END_SESSION_ATTRIBUTE_NAME)
    
    @end_session
    def test_func():
        pass
    
    assert hasattr(test_func, END_SESSION_ATTRIBUTE_NAME)