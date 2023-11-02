import functools

EXCEPTION_ATTRIBUTE_NAME = '_exception'
START_SESSION_ATTRIBUTE_NAME = '_start_session'
END_SESSION_ATTRIBUTE_NAME = '_end_session'


def raise_exception(exception: type(Exception)):
    """Decorator which mark function like should raise an exception.

    Args:
        exception: The type of exception.
    """
    def decorator(func):
        func._exception = exception

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


def start_session(func):
    """The decorator which mark function like should be 
    called before the session starts.

    Args:
        func (Function): The decorated function.
    """
    func._start_session = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def end_session(func):
    """The decorator which mark function like should be 
    called after the session ends.

    Args:
        func (Function): The decorated function.
    """
    func._end_session = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
