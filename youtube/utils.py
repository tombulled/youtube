import addict

import typing

import innertube.utils

def flatten(items):
    flat = addict.Dict()

    for item in items:
        for key, val in item.items():
            flat.setdefault(key, []).append(val)

    return flat

def is_empty_addict(value):
    return isinstance(value, addict.Dict) and not value

def parse(value, *parsers):
    if not is_empty_addict(value):
        for parser in parsers:
            value = parser(value)

    return value

def filter(function = None, **kwargs):
    return innertube.utils.filter \
    (
        function or \
        (
            lambda key, value: not is_empty_addict(value)
        ),
        **kwargs
    )

# TODO: Implement count
def lstrip(string: str, substring: str, count: typing.Optional[int] = None) -> str:
    return string[len(substring):] if string.startswith(substring) else string
