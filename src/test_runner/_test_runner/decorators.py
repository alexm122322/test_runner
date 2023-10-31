import functools


def should_raise_exception(exception: type(Exception)):
    def decorator(func):
        func._exception = exception
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator



def start_session(func):
    func.start_session = True
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper



def end_session(func):
    func.end_session = True
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

