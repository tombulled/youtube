import functools
import pydantic

def parse(parser):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return parser(func(*args, **kwargs))

        return wrapper

    return decorator

def objectify(type):
    return parse(functools.partial(pydantic.parse_obj_as, type))

def imitate(wrapped):
    def decorator(func):
        return_annotation = getattr(func, '__annotations__', {}).get('return')

        wrapper = functools.wraps(wrapped)(func)

        getattr(wrapper, '__annotations__', {})['return'] = return_annotation

        return wrapper

    return decorator

def method(source = None, parser = None):
    def decorator(func):
        return_annotation = getattr(func, '__annotations__', {}).get('return')

        if source:            func = imitate(source)(func)
        if parser:            func = parse(parser)(func)
        if return_annotation: func = objectify(return_annotation)(func)

        return func

    return decorator
