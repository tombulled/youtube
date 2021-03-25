import functools

def parse(parser):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return parser(func(*args, **kwargs))

        return wrapper

    return decorator

def proxy(wrapped):
    def decorator(func):
        return_annotation = getattr(func, '__annotations__', {}).get('return')

        wrapper = functools.wraps(wrapped)(func)

        getattr(wrapper, '__annotations__', {})['return'] = return_annotation

        return wrapper

    return decorator
