from functools import wraps


def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1.Code to execute BEFORE calling the decorated function.

        # 2. Calling decorating function and return results from it
        return func(*args, **kwargs)
        
        # 3.Code to run instead of calling the decorated function

    return wrapper
